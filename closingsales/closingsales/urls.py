from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path('', include('frontend.urls')),
    path('accounts/', include('account.urls')),
    path('dashboard/', include('products.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)