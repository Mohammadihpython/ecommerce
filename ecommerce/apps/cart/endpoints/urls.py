from django.urls import path

from .views import AddCartView

app_name = "cart"
urlpatterns = [path("add", AddCartView.as_view(), name="add-cart")]
