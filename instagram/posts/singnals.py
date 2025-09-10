from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post

@receiver(m2m_changed ,sender=Post.user_like.through)
def user_likes_change(sender,instanc ,**kwargs):
    instanc.total_likes = instanc.user_like.count()
    instanc.save()