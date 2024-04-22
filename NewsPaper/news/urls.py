from django.urls import path
from . import views
from .views import NewsList, NewsDetail

urlpatterns = [
    path('news/', views.NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsDetail.as_view(), name = 'post_detail'),
]