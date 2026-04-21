from django.urls import path
from backend.view.login_view import login_api

urlpatterns = [
    path('', login_api, name='login'),
]