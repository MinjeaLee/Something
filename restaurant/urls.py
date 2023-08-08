from django.urls import path, include
from .views import near_restaurant

urlpatterns = [
    path("get_good/", near_restaurant),
]