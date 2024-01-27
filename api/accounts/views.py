from django.shortcuts import render
from .serializers import (
    SignUpSerilizer, 
    PersonalDataSerializer, 
    PasswordChangeSerializer,
    LoginSerializer,
    LogoutSerializer,
    )
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create your views here.

class SignUpView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SignUpSerilizer
    model = User

class PersonalDataView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PersonalDataSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            "status" : True,
            'message' : 'Personal data changed successfully',
        }

        return Response(data)
    
class PasswordChangeView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PasswordChangeSerializer
    http_method_names = ['put', 'patch']
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            "status" : True,
            'message' : 'Password changed successfully',
        }

        return Response(data)
    
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=self.request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        try:
            refresh_token = self.request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            data = {"status": True, "message": "Siz tizimdan chiqdingiz"}

            return Response(data=data, status=205)
        except Exception as e:
            data = {"status": False, "message": str(e)}
            return Response(data=data, status=405)





