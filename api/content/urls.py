from django.urls import path
from .views import (CreateNewsView, ListNewsView, RetrieveNewsView,
                    UpdateNewsView, DeleteNewsView, ListTagsView, CreateTagsView,
                    RetrieveTagsView, UpdateTagsView, DeleteTagsView, ListCategoryView,
                    CreateCategoryView, RetrieveCategoryView, UpdateCategoryView, 
                    DeleteCategoryView, SearchFilterNewsView, 
                    )

urlpatterns = [
    path('listall/', ListNewsView.as_view()),
    path('listall_tags/', ListTagsView.as_view()),
    path('listall_category/', ListCategoryView.as_view()),

    #news CRUD
    path('create/', CreateNewsView.as_view()),
    path('read/<uuid:uuid>/', RetrieveNewsView.as_view()),
    path('update/<uuid:uuid>', UpdateNewsView.as_view()),
    path('delete/<uuid:uuid>', DeleteNewsView.as_view()),

    #tags CRUD
    path('create_tags/', CreateTagsView.as_view()),
    path('read_tags/<uuid:uuid>', RetrieveTagsView.as_view()),
    path('update_tags/<uuid:uuid>', UpdateTagsView.as_view()),
    path('delete_tags/<uuid:uuid>', DeleteTagsView.as_view()),
    

    #category CRUD
    path('create_category/', CreateCategoryView.as_view()),
    path('read_category/<uuid:uuid>', RetrieveCategoryView.as_view()),
    path('update_category/<uuid:uuid>', UpdateCategoryView.as_view()),
    path('delete_category/<uuid:uuid>', DeleteCategoryView.as_view()),
    

    #filter & search
    path('filter/', SearchFilterNewsView.as_view()),
]