from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
     path('admin/', admin.site.urls),
    
    # API endpoints
     path('api/auth/', include('users.urls')),
    # Products and Orders URLs will be added in next steps
     path('api/', include('products.urls')),
     path('api/', include('orders.urls')),
]