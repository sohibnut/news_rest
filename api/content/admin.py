from django.contrib import admin
from .models import News, Tags, Category
# Register your models here.
admin.site.register(News)
admin.site.register(Tags)
admin.site.register(Category)