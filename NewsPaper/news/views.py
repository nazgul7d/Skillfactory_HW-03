from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, 
                                  CreateView, UpdateView, 
                                  DeleteView
)
from .models import Post
from .search import PostFilter
from .forms import PostForm

class NewsList(ListView):
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

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = "новость" 
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')





