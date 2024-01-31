from django.shortcuts import get_object_or_404
from .serializers import NewsSerializer, CategorySerializer, TagsSerializer
# from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import News, Tags, Category
from rest_framework.response import Response
from django.db.models import Q



# Create your views here.
#News CRUD
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
                "message" : 'link here'
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
        

#Tags CRUD
class ListTagsView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = TagsSerializer

    def get(self, request):
        try:
            tags = Tags.objects.all()
            serializer = self.serializer_class(instance=tags, many=True)
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

class CreateTagsView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TagsSerializer
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'status' : True,
                "message" : 'tag created'
            }
            return Response(data=data)
        data = {
            "status" : False
        }
        raise ValidationError(data)

class RetrieveTagsView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = TagsSerializer
    def get(self, request, uuid):
        tag = get_object_or_404(Tags, uuid = uuid)
        serializer = self.serializer_class(instance=tag)
        data = {
            'status': True,
            'data' : serializer.data
        }
        return Response(data)

class UpdateTagsView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TagsSerializer
    def patch(self, request, uuid):
        data = request.data
        tag = get_object_or_404(Tags, uuid=uuid)
        serilizer = self.serializer_class(instance=tag, data = data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            data = {
                'status' : True,
                'message' : 'tag updated',
                'data' : data
            }
            return Response(data=data)
        data = {
            "status" : False,
        }
        raise ValidationError(data)

class DeleteTagsView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, uuid):
        try:
            tag = Tags.objects.get(uuid=uuid)
            tag.delete()
            data = {
                'status' : True,
                'message' : 'tag successfully deleted!👍👍👍'
            }
            return Response(data)
        except Exception as ex:
            data = {
                "status" : False,
                'message' : f'{ex}'
            }
            raise ValidationError(data)
 


#category CRUD
class ListCategoryView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer

    def get(self, request):
        try:
            category = Category.objects.all()
            serializer = self.serializer_class(instance=category, many=True)
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

class CreateCategoryView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'status' : True,
                "message" : 'category created'
            }
            return Response(data=data)
        data = {
            "status" : False
        }
        raise ValidationError(data)

class RetrieveCategoryView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer
    def get(self, request, uuid):
        category = get_object_or_404(Category, uuid = uuid)
        serializer = self.serializer_class(instance=category)
        data = {
            'status': True,
            'data' : serializer.data
        }
        return Response(data)

class UpdateCategoryView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    def patch(self, request, uuid):
        data = request.data
        category = get_object_or_404(Category, uuid=uuid)
        serilizer = self.serializer_class(instance=category, data = data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            data = {
                'status' : True,
                'message' : 'category updated',
                'data' : data
            }
            return Response(data=data)
        data = {
            "status" : False,
        }
        raise ValidationError(data)

class DeleteCategoryView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, uuid):        
        try:
            category = Category.objects.get(uuid=uuid)
            category.delete()
            data = {
                'status' : True,
                'message' : 'category successfully deleted!👍👍👍'
            }
            return Response(data)
        except Exception as ex:
            data = {
                "status" : False,
                'message' : f'{ex}'
            }
            raise ValidationError(data)
 


#filter & search
class SearchFilterNewsView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = NewsSerializer

    def post(self, request):
        try:
            category = request.data['category']
            tags = request.data['tags']
            if category=="":
                news = News.objects.all()
            else:
                news = News.objects.filter(category=category)
            for x in tags:
                news = news.filter(tags=x)
            # news = news.filter(Q(tags = tags[0]) | Q(tags = tags[1]))
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
        
    def get(self, request):
        try:
            query = self.request.GET.get("search")
            news = News.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
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