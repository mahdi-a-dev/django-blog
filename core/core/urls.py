from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog.urls")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path("api/", include("blog.api.urls", namespace="api")),
    path('api-auth/', include("rest_framework.urls")),
]

# serving static and media for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)