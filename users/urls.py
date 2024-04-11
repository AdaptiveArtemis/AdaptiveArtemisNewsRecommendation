from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.user_login, name='login'),
    path('user/profile/', views.get_user_profile, name='profile'),
    path('user/logs/', views.log_news, name='logNews'),
    path('user/update/', views.update_prefer_list, name='update')
]