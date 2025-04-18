from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views import  UserLoginView, UserRegisterView, OTPView


urlpatterns = [
    
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('otp/send/', OTPView.as_view(), name='send_otp'),
    path('otp/verify/', OTPView.as_view(), name='verify_otp'),

]

  
