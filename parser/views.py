import threading

from django.shortcuts import render, redirect
from django.contrib import messages
from parser.Crawler import ParserRun

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from parser.models import Article
from .serializers import ArticleSerializer
import logging

logger = logging.getLogger(__name__)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-id')
    serializer_class = ArticleSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source']
    search_fields = ['title', 'text', 'words']
    ordering_fields = ['foundAt', 'title']

def HomeView(request):
    if request.method == 'POST':
        logger.info("▶ Button pressed")

        threading.Thread(target=ParserRun, daemon=True).start()

        messages.success(request, "Парсер запущен в фоновом режиме.")
        return redirect('home')

    return render(request, 'parser/home.html')