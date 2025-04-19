from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, OTPSendSerializer, OTPVerifySerializer
from rest_framework.permissions import AllowAny
from django.core.cache import cache
import random
from .utility import send_sms





class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        
        block_key =f"block {phone_number}"   
        if cache.get(block_key):
            return Response(
                {"error": "Sorry the user is blocked for One hour!"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            cache.delete(block_key)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        
        attempts_key = f"attempts_{phone_number}"
        attempts = cache.get(attempts_key, 0) + 1
        cache.set(attempts_key, attempts, timeout=3600)  # Store attempts for 1 hour
        if attempts >= 3:
            cache.set(block_key, True, timeout=3600)
            return Response(
                {"error": "User is blocked for 1 hour"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OTPSendView(generics.GenericAPIView):
    serializer_class = OTPSendSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = str(random.randint(100000, 999999))  
        send_sms(phone_number, code) 
        cache.set(f"otp_{phone_number}", code, timeout=300) 

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

    def verify(self, request):
        # Verifying OTP
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        cached_code = cache.get(f"otp_{phone_number}")

        if cached_code and cached_code == code:
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    
    def post(self, request):
        # Verifying OTP
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        cached_code = cache.get(f"otp_{phone_number}")

        if cached_code and cached_code == code:
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
    