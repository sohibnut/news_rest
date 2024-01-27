from django.shortcuts import render, get_object_or_404
from .serializers import NewsSerializer
# from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import News, Tags
from rest_framework.response import Response



# Create your views here.

class ListNewsView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = NewsSerializer

    def get(self, request):
        try:
            news = News.objects.all()
            serializer = self.serializer_class(instance=news, many=True)
            data = {
                'data': serializer.data
            }
            return Response(data)
        except Exception as ex:
            data = {
                'status' : False,
                "message" : f'{ex}'
            }
            raise ValidationError(data)

class CreateNewsView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = NewsSerializer
    def post(self, request):
        data = request.data
        data['author']  = request.user.id
        serializer = self.serializer_class(data = data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'status' : True,
                "link" : 'link here'
            }
            return Response(data=data)
        data = {
            "status" : False
        }
        raise ValidationError(data)

class RetrieveNewsView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = NewsSerializer
    def get(self, request, uuid):
        new = get_object_or_404(News, uuid = uuid)
        serializer = self.serializer_class(instance=new)
        data = {
            'status': True,
            'data' : serializer.data
        }
        return Response(data)

class UpdateNewsView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = NewsSerializer
    def patch(self, request, uuid):
        data = request.data
        new = get_object_or_404(News, uuid=uuid)
        if new.author.id != request.user.id:
            data = {
                'status' : False,
                'message' : 'you cannot update article which you did not create!'
            }
            raise ValidationError(data)
        serilizer = self.serializer_class(instance=new, data = data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            data = {
                'status' : True,
                'message' : 'news updated',
                'data' : data
            }
            return Response(data=data)
        data = {
            "status" : False,
            'message' : 'invalid data'
        }
        raise ValidationError(data)

class DeleteNewsView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, uuid):
        new = get_object_or_404(News, uuid=uuid)
        if new.author.id != request.user.id:
            data = {
                'status' : False,
                'message' : 'you cannot delete article which you did not create!'
            }
            raise ValidationError(data)

        try:
            new = News.objects.get(uuid=uuid)
            new.delete()
            data = {
                'status' : True,
                'message' : 'article successfully deleted!👍👍👍'
            }
            return Response(data)
        except Exception as ex:
            data = {
                "status" : False,
                'message' : f'{ex}'
            }
            raise ValidationError(data)