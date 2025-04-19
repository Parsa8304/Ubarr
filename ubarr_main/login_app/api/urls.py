from django.urls import path 
from .views import  UserLoginView, UserRegisterView, OTPSendView, OTPVerifyView


urlpatterns = [
    
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('otp/send/', OTPSendView.as_view(), name='send_otp'),
    path('otp/verify/', OTPVerifyView.as_view(), name='verify_otp'),

]

  
