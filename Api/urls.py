from django.urls import path
from .views import AllAPIEndpointsView

urlpatterns = [
    path('', AllAPIEndpointsView.as_view(), name='api_endpoints'),
    # other URL patterns...
]
