from django.db import models


class Source(models.Model):
    source_types = [
        ('site', 'сайт'),
        ('vk', 'ВК'),
        ('rss', ' RSS'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    url = models.URLField(unique=True, verbose_name="Ссылка / ID группы")
    source_type = models.CharField(max_length=10, choices=source_types, default='site', verbose_name="Тип", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен для парсинга")
    patterns = models.TextField(verbose_name="Регулярка", default="/", blank=True)
    rss = models.URLField(verbose_name="RSS", default="", blank=True)

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
        ordering = ['name']

    def __str__(self):
        return self.name


class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True, verbose_name="Ключевое слово")

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"
        ordering = ['word']

    def __str__(self):
        return self.word
