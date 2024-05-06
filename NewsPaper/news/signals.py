from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Post, Category

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.category.all().subscribers.all()
        subject = f'Новый пост в категории {instance.category.category}: {instance.title}'
        message = f'Краткая информация о посте: {instance.preview()}'
        for subscriber in subscribers:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [subscriber.email])

@receiver(post_save, sender=Post)
def check_post_limit(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        today = timezone.now().date()
        post_count = Post.objects.filter(author=user, created_at__date=today).count()
        if post_count > 3:
            raise Exception('Daily limit is exceeded!')
