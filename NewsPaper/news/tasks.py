from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Post, Category
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_notifications(post_id):
    post = Post.objects.get(pk=post_id)
    for category in post.category.all():
            for subscriber in Category.subscribers.all():
                subject = post.title
                html_message = render_to_string('newsletter_email.html', {'post': post, 'subscriber': subscriber})
                text_content = strip_tags(html_message)
                email = EmailMultiAlternatives(subject, text_content, 'your_email@example.com', [subscriber.email])
                email.attach_alternative(html_message, "text/html")
                email.send()

@shared_task
def newsletter():
    last_week_start = timezone.now() - timedelta(days=7)
    latest_posts = Post.objects.filter(created_at__gte = last_week_start)

    subject = "Weekly Newsletter: Latest News"
    html_message = render_to_string('weekly_newsletter.html', {'latest_posts': latest_posts})
    text_content = strip_tags(html_message)

    subscribers = Category.subscribers.all()  
    for subscriber in subscribers:
        email = EmailMultiAlternatives(subject, text_content, 'your_email@example.com', [subscriber.email])
        email.attach_alternative(html_message, "text/html")
        email.send()
