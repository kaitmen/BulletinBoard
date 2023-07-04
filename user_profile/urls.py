from django.urls import path

from .views import *


urlpatterns = [
    path('profile', settings, name='settings'),
    path('register_code/<str:token>', register_code, name='register_code'),
]