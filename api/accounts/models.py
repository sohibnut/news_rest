from django.db import models
from api.base.models import BaseUserModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class User(AbstractUser, BaseUserModel):
    email = models.EmailField(blank = True, unique = True)
    photo = models.ImageField(
        upload_to="user_photo/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
            )
        ],
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
