from django.urls import path
from .views import NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', NewsList.as_view()),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name = 'post_detail'),
    path('news/create', PostCreate.as_view(), name = 'post_create' ),
    path('news/<int:pk>/update', PostUpdate.as_view(), name = 'post_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name = 'post_delete'),
    path('articles/create', PostCreate.as_view(), name = 'article_create' ),
    path('articles/<int:pk>/update', PostUpdate.as_view(), name = 'article_update'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name = 'article_delete'),
]


