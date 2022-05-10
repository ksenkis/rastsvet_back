from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import image_page, BookCreate

urlpatterns = [
    path('book/', BookCreate.as_view(), name='image_book'),
    path('', image_page),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
