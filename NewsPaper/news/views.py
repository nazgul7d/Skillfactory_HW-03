from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, 
                                  CreateView, UpdateView, 
                                  DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail

from .models import Post, Category
from .search import PostFilter
from .forms import PostForm

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class NewsList(PermissionRequiredMixin, ListView):
    permission_required = ('news.view_post', )
    model = Post
    ordering = 'title'
    template_name = 'news/post_list.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-created_at')
    paginate_by = 1


    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       return context
       
    
class NewsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('news.view_post', )
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = "новость" 
        result = super().form_valid(form)
        self.send_email_to_subscribers(form.instance)
        return result
    
    def send_email_to_subscribers(self, post):
        for category in post.category.all():
            for subscriber in category.subscribers.all():
                subject = post.title
                html_message = render_to_string('newsletter_email.html', {'post': post, 'subscriber': subscriber})
                text_content = strip_tags(html_message)
                email = EmailMultiAlternatives(subject, text_content, 'your_email@example.com', [subscriber.email])
                email.attach_alternative(html_message, "text/html")
                email.send()

class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post', )
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.user in category.subscribers.all():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
