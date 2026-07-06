# Source

Сейчас для двух типов сурсов (сайт и рсс) вполне нормально использовать под каждого свой столбец (для сайта - паттерн,
для рсс - ссылка). Но в будущем, когда появятся новые типы сурсов, будет, во-первых, неудобно добавлять новые столбцы, а
во-вторых, будет очень много пустых столбцов для других типов. Поэтому в планах убрать все зависимые от стратегии
столбцы, оставив вместо них `JSONField` в котором эти специфичные настройки будут храниться. 

```python
class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    sourceType = models.CharField(max_length=50) # 'site', 'rss', 'vk'
    
    # Для сайта: {"patterns": ".*/news/.*"}
    # Для ВК: {"token": "123", "group_id": "999"}
    strategy_config = models.JSONField(default=dict, blank=True)


