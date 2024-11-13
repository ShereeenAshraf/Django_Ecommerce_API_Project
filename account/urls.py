from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('userinfo/', views.current_user, name='userinfo'),
    path('userinfoupdate/', views.update_user, name='userinfoupdate'),
    path('forget_password/', views.forgot_password, name='forget_password'),
    path('rest_password/<str:token>', views.reset_password, name='reset_password'),
]
