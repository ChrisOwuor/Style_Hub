from django.urls import path
from . import views

urlpatterns = [
    path('approvals/', views.StylistApprovalView.as_view(),
         name='stylist-approvals'),
    path('stylists/', views.StylistListView.as_view(), name='stylist-list'),
    path('stylists/<int:id>/', views.StylistDetailView.as_view(),
         name='stylist-detail'),
]
