from django.db import models
from api.base.models import BaseUserModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta, datetime
import random
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
    
    def create_verify_code(self):
        code = "".join([str(random.randint(0, 9)) for _ in range(10)])
        UserConfirmation.objects.create(code = code, user = self)
        return code

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

class UserConfirmation(BaseUserModel):
    CODE_LIFETIME = 3 #code lifetime in minutes
    code = models.CharField(max_length = 10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'verify_code')
    code_lifetime = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.code}"
    
    def save(self, *args, **kwargs):
        self.code_lifetime = datetime.now() + timedelta(minutes=self.CODE_LIFETIME)
        super(UserConfirmation, self).save(*args, **kwargs)