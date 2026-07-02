from django.db import models
from sources.models import Source


class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name="Источник", related_name="articles")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    words = models.CharField(verbose_name='Ключевые слова', default="")
    text = models.TextField(verbose_name="Текст статьи")
    url = models.URLField(unique=True, verbose_name="Ссылка на статью")
    foundAt = models.DateTimeField(auto_now_add=True, verbose_name="Дата нахождения")


    def __str__(self):
        return self.title