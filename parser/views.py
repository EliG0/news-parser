import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from parser.models import Article
from parser.tasks import celery_crawl_all_active_sources_task
from parser.permissions import IsStaffOrReadOnly
from parser.filters import ArticleFilter
from parser.serializers import ArticleSerializer

logger = logging.getLogger(__name__)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-id')
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'text', 'words']
    ordering_fields = ['foundAt', 'title']


def HomeView(request):
    if request.method == 'POST':
        logger.info("▶ Button pressed - Triggering Celery workflow")

        celery_crawl_all_active_sources_task.delay()

        messages.success(request, "Парсер запущен в фоновом режиме.")
        return redirect('home')

    return render(request, 'parser/home.html')
