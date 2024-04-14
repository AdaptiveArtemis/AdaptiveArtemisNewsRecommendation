from django.urls import path
from . import views



app_name = 'users'

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.user_login, name='login'),
    path('user/profile/', views.get_user_profile, name='profile'),     #   get
    path('user/logNews/', views.log_news, name='logNews'),
    path('user/update/', views.update_prefer_list, name='update')
]


# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('users/', include('users.urls')),
#     path('recommend/', include('recommend.urls')),
#     # 下面是添加的登录和登出路径
#     path('users/login/', auth_views.LoginView.as_view(), name='login'),
#     path('users/logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]



