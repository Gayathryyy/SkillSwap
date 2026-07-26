from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('login/', views.user_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', views.user_logout, name='logout'),

]