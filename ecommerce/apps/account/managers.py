from django.db.models import BaseManager


class UserManager(BaseManager):
    def create_user(self,phone_number:str,password:str,**extra_fields):
        if not phone_number:
            raise ValueError(_("شماره تلفن باید فرستاده شود"))
        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,phone_number,password,**extra_fields):
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        if extra_fields.get('is_superuser')is not True:
            raise ValueError(_(" is_superuser=True سوپرکاربر باید داشته باشد"))
        return self.create_user(phone_number=phone_number,password=password,**extra_fields)