from rest_framework import serializers
from .models import Tags, News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
       