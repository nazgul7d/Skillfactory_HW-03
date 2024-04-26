import django_filters
from django import forms
from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    author_name = django_filters.CharFilter(field_name='author_name', lookup_expr='icontains')


    class Meta:
        model = Post
        fields = ['title', 'author_name', 'created_at']
