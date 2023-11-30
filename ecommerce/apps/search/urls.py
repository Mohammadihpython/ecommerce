from django.urls import path

from . import views

app_name = "search"

urlpatterns = [
    path("product/", views.SearchProductInventoryView.as_view(), name="product"),
]
