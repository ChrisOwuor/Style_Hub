from django.urls import path
from . import views

urlpatterns = [
    path('client/', views.ClientListView.as_view(), name='client-list'),
    path('client/<int:id>/', views.ClientDetailView.as_view(),
         name='client-detail'),
]
