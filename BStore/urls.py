from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),      # Landing Page
    path('admin/', admin.site.urls),
    path('bookadmin/', include('bookadmin.urls')),
    path('', include('userapp.urls')),      # Make user URLs available globally
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
