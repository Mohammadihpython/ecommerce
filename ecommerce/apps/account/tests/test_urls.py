import pytest
from django.urls import resolve, reverse

from ecommerce.apps.account.endpoints import views


@pytest.mark.django_db
def test_users_list_url():
    url = reverse("account:users-list")
    assert resolve(url).func.view_class == views.UsersListView


@pytest.mark.django_db
def test_users_register_url():
    url = reverse("account:register")
    assert resolve(url).func.view_class == views.RegisterView


@pytest.mark.django_db
def test_users_login_url():
    url = reverse("account:login")
    assert resolve(url).func.view_class == views.LoginView


@pytest.mark.django_db
def test_users_logout_url():
    url = reverse("account:logout")
    assert resolve(url).func.view_class == views.LogoutView


@pytest.mark.django_db
def test_users_verify_url():
    url = reverse("account:verify")
    assert resolve(url).func.view_class == views.VerifyOtpView


@pytest.mark.django_db
def test_users_verify_two_step_password_url():
    url = reverse("account:verify-two-step-password")
    assert resolve(url).func.view_class == views.VerifyTwoStepPasswordView


@pytest.mark.django_db
def test_users_create_two_step_password_url():
    url = reverse("account:create-two-step-password")
    assert resolve(url).func.view_class == views.CreateTwoStepPasswordView


@pytest.mark.django_db
def test_users_change_two_step_password_url():
    url = reverse("account:change-two-step-password")
    assert resolve(url).func.view_class == views.ChangeTwoStepPasswordView


@pytest.mark.django_db
def test_users_delete_account_url():
    url = reverse("account:delete-account")
    assert resolve(url).func.view_class == views.DeleteAccountView


@pytest.mark.django_db
def test_users_detail_url(db, user_factory):
    user = user_factory.create()
    url = reverse("account:users-detail", kwargs={"pk": user.pk})
    assert resolve(url).func.view_class == views.UsersDetailUpdateDeleteView
