from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.register, name='register'),
    path('auth/login', views.login, name='login'),
    path('auth/refresh', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('assets/accounts', views.account_list, name='account-list'),
]
