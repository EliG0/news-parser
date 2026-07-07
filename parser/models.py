from django.db import models
from django.utils import timezone

from sources.models import Source


class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name="Источник", related_name="articles")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    words = models.CharField(verbose_name='Ключевые слова', default="")
    text = models.TextField(verbose_name="Текст статьи")
    url = models.URLField(unique=True, verbose_name="Ссылка на статью")
    published_at = models.DateTimeField(verbose_name="Дата публикации", null=True, blank=True)
    found_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата нахождения")

    def save(self, *args, **kwargs):
        # Если при создании/обновлении статьи поле published_at будет None, то приравниваем его к текущему времени.
        if not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-found_at']

    def __str__(self):
        return self.title