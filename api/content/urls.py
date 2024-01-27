from django.urls import path
from .views import (CreateNewsView, ListNewsView, RetrieveNewsView,
                    UpdateNewsView, DeleteNewsView)

urlpatterns = [
    path('create/', CreateNewsView.as_view()),
    path('listall/', ListNewsView.as_view()),
    path('read/<uuid:uuid>/', RetrieveNewsView.as_view()),
    path('update/<uuid:uuid>', UpdateNewsView.as_view()),
    path('delete/<uuid:uuid>', DeleteNewsView.as_view()),
]