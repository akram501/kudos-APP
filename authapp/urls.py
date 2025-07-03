from django.urls import path
from .api import LoginAPI


urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
]
