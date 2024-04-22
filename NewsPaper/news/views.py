from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news/post_list.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-created_at')



class NewsDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'



