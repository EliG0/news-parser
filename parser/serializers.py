from rest_framework import serializers
from parser.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'url', 'source', 'words', 'foundAt']