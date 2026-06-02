from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Profile, Course


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver([post_save, post_delete], sender=Course)
def invalidate_course_cache(sender, instance, **kwargs):
    # Clear course list cache
    # django-redis allows delete_pattern, but we can also just clear common keys
    # or use a versioning strategy. For simplicity, we'll use a broad clear if possible
    # or just delete the main list and the specific detail.
    cache.delete_pattern("course_list_*")
    cache.delete(f"course_detail_{instance.id}")