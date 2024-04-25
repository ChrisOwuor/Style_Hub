from django.urls import path
from . import views

urlpatterns = [
    path('approvals/', views.AdminApprovalsListView.as_view(),
         name='admin-approvals-list'),
    path('approvals/<int:id>/<str:action>/',
         views.AdminApprovalsActionView.as_view(), name='admin-approval-action'),
]
