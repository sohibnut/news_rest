from django.shortcuts import render, get_object_or_404
from .serializers import (
    SignUpSerilizer, 
    PersonalDataSerializer, 
    PasswordChangeSerializer,
    LoginSerializer,
    LogoutSerializer,
    AccessRefreshSerializer,
    PasswordResetSerializer,
    PasswordResetViaCodeSerializer,
    ProfileSerializer
    )
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta, datetime
from rest_framework.response import Response
from .models import User, UserConfirmation
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.base.utilitys import sent_email

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
    
class PasswordResetView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        code = user.create_verify_code()

        data = {
            'status' : True,
            'message' : 'you get email via verify code'
        }
        sent_email(email, code)
        return Response(data)

class PasswordResetViaCodeView(APIView):
    serializer_class = PasswordResetViaCodeSerializer
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        password = serializer.validated_data.get('password1')
        verify_code = UserConfirmation.objects.filter(code_lifetime__gte = datetime.now(), code = code, is_confirmed=False)
        if verify_code.exists():
            user = verify_code.first().user
            user.set_password(password)
            user.save()
            verify_code.update(is_confirmed = True)
            data = {
                'status' : True,
                'message' : 'password reseted👍'
            }
            return Response(data)
        data = {
            'status' : False,
            'message' : 'we can not find this verification code'
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

class AccessRefreshView(TokenRefreshView):
    serializer_class = AccessRefreshSerializer

class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(instance=user)
        data = {
            'status' : True,
            'data' : serializer.data
        }
        return Response(data)


