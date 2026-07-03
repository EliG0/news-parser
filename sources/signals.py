# sources/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from sources.models import Keyword

@receiver([post_save, post_delete], sender=Keyword)
def clear_keywords_cache(sender, instance, **kwargs):
    cache.delete('crawler_keywords_list')