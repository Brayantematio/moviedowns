from django.urls import path
from .views import *

urlpatterns = [
    path('', download_video, name='download_video'),
    path('politiques', politique, name='politique'),
]