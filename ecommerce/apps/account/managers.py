from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, **extra_fields):
        if not phone_number:
            raise ValueError(_("شماره تلفن باید فرستاده شود"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_(" is_superuser=True سوپرکاربر باید داشته باشد"))
        return self.create_user(phone_number=phone_number, **extra_fields)
