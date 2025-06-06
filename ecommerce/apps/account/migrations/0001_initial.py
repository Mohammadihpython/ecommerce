# Generated by Django 5.2.1 on 2025-06-06 06:07

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        error_messages={"unique": "کاربر با این شماره وجود دارد"},
                        max_length=14,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Invalid phone number.",
                                regex="^989\\d{2}\\s*?\\d{3}\\s*?\\d{4}$",
                            )
                        ],
                        verbose_name="شماره تلفن",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="نام "
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="نام خانوادگی ",
                    ),
                ),
                (
                    "two_step_password",
                    models.BooleanField(
                        default=False,
                        help_text="is active two step password?",
                        verbose_name="two step password",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="مشخص می کند که آیا کاربر می تواند به این سایت مدیریت وارد شود یا خیر.",
                        verbose_name="وضعیت کارکنان",
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text='\n           مشخص می کند که آیا این کاربر باید به عنوان فعال در نظر گرفته شود\n          .به جای حذف حساب\u200cها، این را لغو انتخاب کنید."\n            ',
                        verbose_name="فعال",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
