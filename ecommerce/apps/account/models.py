
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number."),
    )
    phone_number = models.CharField(
        verbose_name = _("شماره تلفن"),
        max_length=14,
        unique=True,
        validators=[phone_regex],
        error_messages = {
            'unique': _("کاربر با این شماره وجود دارد"),
        }
    )
    first_name = models.CharField(
        _("نام "),
        max_length=250,
        null = True,
        blank = True,
    )
    last_name = models.CharField(
        _("نام خانوادگی "),
        max_length=250,
        null = True,
        blank = True,
    )
    two_step_password = models.BooleanField(
        default=False, help_text=_("is active two step password?"),
        verbose_name=_("two step password"),
    )
    is_staff = models.BooleanField(
        _("وضعیت کارکنان"),
        default=False,
        help_text=_("مشخص می کند که آیا کاربر می تواند به این سایت مدیریت وارد شود یا خیر."),
    )
    is_active = models.BooleanField(
        _("فعال"),
        default=True,
        help_text=_(
            "  مشخص می کند که آیا این کاربر باید به عنوان فعال در نظر گرفته شود .به جای حذف حساب‌ها، این را لغو انتخاب کنید."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.phone_number








