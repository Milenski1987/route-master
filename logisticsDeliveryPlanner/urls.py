from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('driver/', include('drivers.urls')),
    path('vehicle/', include('vehicles.urls')),
    path('routes/', include('routes.urls')),
    path('accounts/', include('accounts.urls')),
]
