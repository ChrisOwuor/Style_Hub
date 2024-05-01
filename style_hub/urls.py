
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/admin/', include('administration.urls')),
    path('api/client/', include('client.urls')),
    path('api/stylist/', include('stylist.urls')),
    path('', include('Api.urls')),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
