from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    path("", views.UsersListView.as_view(), name="users-list"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("verify/", views.VerifyOtpView.as_view(), name="verify"),
    path(
        "verify-two=step-password/",
        views.VerifyTwoStepPasswordView.as_view(),
        name="verify-two-step-password",
    ),
    path(
        "change-two-step-password/",
        views.ChangeTwoStepPasswordView.as_view(),
        name="change-two-step-password",
    ),
    path(
        "create-two-step-password/",
        views.CreateTwoStepPasswordView.as_view(),
        name="create-two-step-password",
    ),
    path("delete-account/", views.DeleteAccountView.as_view(), name="delete-account"),
    path(
        "users/<int:pk>/",
        views.UsersDetailUpdateDeleteView.as_view(),
        name="users-detail",
    ),
]
