from .models import User
from rest_framework import serializers
from api.base.utilitys import check_email
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login


class SignUpSerilizer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
        

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            data = {
                'status' : False,
                'message' : 'passwords are not equal!'
            }
            raise ValidationError(data)
        return attrs
    
    # def validate_username(self, username):
    #     if User.objects.filter(username = username).exists():
    #         data = {
    #             'status' : False,
    #             'message' : 'This username already exists!'
    #         }
    #         raise ValidationError(data)
    #     return username
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(instance.token())
        data['status'] = True
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password1'])
        user.save()
        return user

class PersonalDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only = True, required = True)
    last_name = serializers.CharField(write_only = True, required = True)
    photo = serializers.ImageField(validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    email = serializers.EmailField(write_only=True, required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        if User.objects.filter(email = data['email']).exists():
            data = {
                'status' : False,
                'message' : 'email already exists'
            }
            raise ValidationError(data)
        return data
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email')
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()

        return instance

class PasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True)
    old_password = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            data = {
                'status' : False,
                'message' : 'passwords are not equal!'
            }
            raise ValidationError(data)
        return attrs
    
    def update(self, instance, validated_data):
        if instance.check_password(validated_data['old_password']):
            instance.set_password(validated_data['password1'])
            instance.save()
            return instance
        
        data = {
                'status' : False,
                'message' : 'Wrong password!'
            }
        raise ValidationError(data)

class LoginSerializer(TokenObtainPairSerializer):  
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        auth_kwarg = {self.username_field: username, "password": password}
        user = authenticate(**auth_kwarg) 
        if user:
            self.user = user
        else:
            data = {
                "status": False,
                "message": "Username or password is wrong !!!",
            }
            raise ValidationError(data)
        
        data = self.to_representation(self.user)
        return data
    
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(instance.token())
        data['status'] = True
        data['message'] = "Login success"
        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class AccessRefreshSerializer(TokenRefreshSerializer):
    def validate(self, data):
        data = super().validate(data)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id = user_id)
        update_last_login(None, user)

        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only = True, required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if check_email(attrs['email']):
            if User.objects.filter(email = attrs['email']).exists():
                return attrs
            else:
                data = {
                    'status' : False,
                    'message' : 'There is not user via this email'
                } 
                raise ValidationError(data)
        data = {
            'status' : False,
            'message' : 'are you sure you typed email bro?'
        }
        raise ValidationError(data)

class PasswordResetViaCodeSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True)
    code = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            data = {
                'status' : False,
                'message' : 'passwords are not equal!'
            }
            raise ValidationError(data)
        return attrs
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


