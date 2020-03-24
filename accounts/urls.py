from django.urls import path
from .views import AccountCreateView, AccountDetailView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/signup/', AccountCreateView.as_view(), name='account_create'),
    path('api/auth/login/', obtain_auth_token, name='api_token_auth'),
    path('api/account_details/', AccountDetailView.as_view(), name='api_account_details'),
]
