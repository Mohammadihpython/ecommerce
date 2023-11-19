
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    phone_number = models.CharField(
        verbose_name = _("شماره تلفن"),
        max_length=14,
        unique=True,
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
    phone_verified = models.BooleanField(
        _("شماره تماس تایید شده؟"),
        default=False
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
    REQUIRED_FIELDS = ['phone_number',]
    objects = UserManager()

    def __str__(self):
        return self.phone_number








