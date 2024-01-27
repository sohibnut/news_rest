from rest_framework import serializers
from .models import Tags, News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        # fields = (
        #     'title', 
        #     'image',
        #     'body',
        #     'tags',
        #     'author'
        # )

    # def create(self, validated_data):
    #     new = News.objects.create(
    #         title = validated_data['title'],
    #         image = validated_data['image'],
    #         body = validated_data['body'],
    #         author = validated_data['author']
            
    #     )   
    #     new.tags.set(validated_data['tags'])
    #     new.save()
    #     return new 
    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.body = validated_data.get('body', instance.body)
    #     instance.email = validated_data.get('email')
    #     instance.photo = validated_data.get('photo', instance.photo)
    #     instance.save()

    #     return instance