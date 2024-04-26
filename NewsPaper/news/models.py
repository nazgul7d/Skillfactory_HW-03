from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0) 

    def update_rating(self):
        post_rating = sum(post.rating * 3 for post in self.post_set.all())
        comment_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = post_rating + comment_rating
        self.save() 

class Category(models.Model):
    category = models.CharField(max_length = 100, unique = True)

class Post(models.Model):

    TYPE_CHOICES = (
        ('article','статья'),
        ('news', 'новость'))
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length = 10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author_name = models.CharField(max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.author_name = self.author.username
        super().save(*args, **kwargs)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def preview(self):
        return(self.text[:124] + + '...')

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()


