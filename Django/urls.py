from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from parser.views import ArticleViewSet
from parser.views import HomeView

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name='home'),
    path('api/', include(router.urls)),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
