import django_filters
from parser.models import Article

class ArticleFilter(django_filters.FilterSet):
    # Фильтр "начиная с даты" (foundAt >= значение)
    found_after = django_filters.DateTimeFilter(field_name='foundAt', lookup_expr='gte')
    # Фильтр "до даты" (foundAt <= значение)
    found_before = django_filters.DateTimeFilter(field_name='foundAt', lookup_expr='lte')
    # Фильтр для поиска по ключевым словам
    keyword = django_filters.CharFilter(field_name='words', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['source']