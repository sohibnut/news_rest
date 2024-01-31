from django.db import models
from api.base.models import BaseContentModel
from api.accounts.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.

class Category(BaseContentModel):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name    
    
class Tags(BaseContentModel):
    name = models.CharField(max_length = 200)
    def __str__(self) -> str:
        return self.name

class News(BaseContentModel):
    title = models.CharField(max_length = 255)
    image = models.ImageField(
        upload_to="news/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
            )
        ],
    )
    body = models.TextField()
    tags = models.ManyToManyField(Tags, related_name='tag_news', blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_news', blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_news', blank = True, null=True)

    def __str__(self) -> str:
        return self.title

