from django.urls import path
from users.views import obtain_auth_token, logout
from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name='token_obtain_pair'),
    path('logout/',logout, name = 'logout'),
    path('users/create/', views.UserCreate.as_view(), name = 'user_create'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('profiles/', views.ProfileList.as_view(), name='profile_list'),
    path('profiles/<str:username>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('referrals/create/', views.ReferralCreate.as_view(), name='referral_create'),
]
