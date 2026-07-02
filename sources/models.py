from django.db import models


class Source(models.Model):
    sourceTypes = [
        ('site', 'сайт'),
        ('vk', 'ВК'),
        ('rss', ' RSS'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    url = models.URLField(unique=True, verbose_name="Ссылка / ID группы")
    sourceType = models.CharField(max_length=10, choices=sourceTypes, default='site', verbose_name="Тип", blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Активен для парсинга")
    patterns = models.TextField(verbose_name="Регулярка", default="/", blank=True)
    rss = models.URLField(verbose_name="RSS", default="", blank=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True, verbose_name="Ключевое слово")

    def __str__(self):
        return self.word
