from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('/', views.get_recommendations, name='recommendations'),
]