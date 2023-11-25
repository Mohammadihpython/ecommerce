from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ...utils.OTP import get_client_ip, send_otp
from .serializers import (
    AuthenticationSerializer,
    ChangeTwoStepPasswordSerializer,
    GetTwoStepPasswordSerializer,
    OtpSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    UsersListSerializer,
)


# from management.authentication import JWTAuthentication
class UsersListView(ListAPIView):
    """
    get:
        Returns a list of all existing users.
    """

    serializer_class = UsersListSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_queryset(self):
        return get_user_model().objects.values(
            "id",
            "phone_number",
            "first_name",
            "last_name",
        )


class UsersDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the detail of a user instance.

        parameters: [pk]

    put:
        Update the detail of a user instance

        parameters: exclude[password,]

    delete:
        Delete a user instance.

        parameters: [pk]
    """

    serializer_class = UserDetailUpdateDeleteSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(
            get_user_model().objects.defer(
                "password",
            ),
            pk=pk,
        )


class UserProfileView(RetrieveUpdateAPIView):
    """
    get:
        Returns the profile of user.

    put:
        Update the detail of a user instance

        parameters: [first_name, last_name,]
    """

    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


class LoginView(generics.GenericAPIView):
    """
    post:
        Send mobile number for Login.

        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]

    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        received_phone = serializer.validated_data.get("phone")

        if (
            get_user_model()
            .objects.filter(phone_number=received_phone)
            .values("phone_number")
            .exists()
        ):
            return send_otp(
                request,
                phone=received_phone,
            )
        else:
            return Response(
                {
                    "No User exists.": "Please enter another phone number.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RegisterView(generics.GenericAPIView):
    """
    post:
        Send mobile number for Register.

        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        received_phone = serializer.data.get("phone")  # type: ignore

        user_is_exists: bool = (
            get_user_model()
            .objects.filter(phone_number=received_phone)
            .values("phone_number")
            .exists()
        )
        if user_is_exists:
            return Response(
                {
                    "User exists.": "Please enter a different phone number.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # The otp code is sent to the user's phone number for authentication
        return send_otp(
            request,
            phone=received_phone,
        )


class VerifyOtpView(generics.GenericAPIView):
    """
    post:
        Send otp code to verify mobile number and complete authentication.

        parameters: [otp,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "verify_authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]
    serializer_class = OtpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        received_code = serializer.data.get("code")  # type: ignore
        ip = get_client_ip(request)
        phone = cache.get(f"{ip}-for-authentication")
        otp = cache.get(phone)

        if otp is not None:
            return (
                self._check_otp(phone, ip)
                if otp == received_code
                else Response(
                    {
                        "Incorrect code.": "The code entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            )
        else:
            return Response(
                {
                    "Code expired.": "The entered code has expired.",
                },
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )

    def _check_otp(self, phone, ip):
        user, created = get_user_model().objects.get_or_create(phone_number=phone)
        if user.two_step_password:  # type: ignore
            cache.set(f"{ip}-for-two-step-password", user, 250)
            return Response(
                {
                    "Thanks": "Please enter your two-step password",
                },
                status=status.HTTP_200_OK,
            )

        refresh = RefreshToken.for_user(user)
        cache.delete(phone)
        cache.delete(f"{ip}-for-authentication")

        context = {
            "created": created,
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # type: ignore
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )


class VerifyTwoStepPasswordView(generics.GenericAPIView):
    """
    post:
        Send two-step-password to verify and complete authentication.

        parameters: [password, confirm_password,]
    """

    permission_classes = [
        AllowAny,
    ]
    serializer_class = GetTwoStepPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        ip = get_client_ip(request)
        user = cache.get(f"{ip}-for-two-step-password")

        if user is not None:
            return self._check_two_password(serializer, user, ip)
        return Response(
            {
                "User expired": "The two-step-password entry time has elapsed",
            },
            status=status.HTTP_408_REQUEST_TIMEOUT,
        )

    def _check_two_password(self, serializer, user, ip):
        password = serializer.data.get("password")
        check_password: bool = user.check_password(password)

        if not check_password:
            return Response(
                {
                    "Error!": "The password entered is incorrect",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        refresh = RefreshToken.for_user(user)
        cache.delete(f"{ip}-for-two-step-password")

        context = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # type: ignore
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )


class CreateTwoStepPasswordView(generics.GenericAPIView):
    """
    post:
        Send a password to create a two-step-password.

        parameters: [new_password, confirm_new_password]
    """

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = GetTwoStepPasswordSerializer

    def post(self, request):
        if request.user.two_step_password:
            return Response(
                {
                    "Error!": "Your request could not be approved.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get("password")  # type: ignore

        try:
            _: None = validate_password(new_password)  # type: ignore
        except ValidationError as err:
            return Response(
                {"errors": err},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = get_object_or_404(
            get_user_model(),
            pk=request.user.pk,
        )
        user.set_password(new_password)
        user.two_step_password = True  # type: ignore
        user.save(update_fields=["password", "two_step_password"])
        return Response(
            {
                "Successful.": "Your password was changed successfully.",
            },
            status=status.HTTP_200_OK,
        )


class ChangeTwoStepPasswordView(generics.GenericAPIView):
    """
    post:
        Send a password to change a two-step-password.

        parameters: [old_password, new_password, confirm_new_password,]
    """

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ChangeTwoStepPasswordSerializer

    def post(self, request):
        if request.user.two_step_password:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_password = serializer.data.get("password")  # type: ignore

            try:
                _: None = validate_password(new_password)  # type: ignore
            except ValidationError as err:
                return Response(
                    {"errors": err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            old_password = serializer.data.get("old_password")  # type: ignore
            user = get_object_or_404(
                get_user_model(),
                pk=request.user.pk,
            )
            check_password: bool = user.check_password(old_password)  # type: ignore

            if check_password:
                user.set_password(new_password)
                user.save(update_fields=["password"])

                return Response(
                    {
                        "Successful.": "Your password was changed successfully.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Error!": "The password entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        return Response(
            {
                "Error!": "Your request could not be approved.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class DeleteAccountView(generics.GenericAPIView):
    """
    delete:
        Delete an existing User instance.
    """

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = GetTwoStepPasswordSerializer

    def delete(self, request):
        user = get_user_model().objects.get(pk=request.user.pk)
        if request.user.two_step_password:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.data.get("password")  # type: ignore
            check_password: bool = user.check_password(password)  # type: ignore

            if not check_password:
                return Response(
                    {
                        "Error!": "The password entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        user.delete()
        return Response(
            {
                "Removed successfully.": "Your account has been successfully deleted.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data["refresh"]
        access_token = request.data["access"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                "کابر با موفقیت از حساب کاربری خارج شد", status=status.HTTP_200_OK
            )
        except Exception:
            refresh_token = access_token
            return Response({"msg : invalid token"}, status=status.HTTP_400_BAD_REQUEST)
