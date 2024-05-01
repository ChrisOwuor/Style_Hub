from django.urls import path
from . import views

urlpatterns = [
    path('approvals/', views.StylistApprovalRequestView.as_view(),
         name='stylist-approvals'),
    path('styles/', views.StylelListView.as_view(),
         name='view_create styles'),
    path('style/<str:u_id>/', views.StyleDetailView.as_view(),
         name='view_edit_delete style_detail'),
    path('bookings/', views.AllBookingsView.as_view(),
         name='view bookings'),
    path('booking/<str:u_id>/',
         views.BookingDetailView.as_view(), name='view booking_details'),
    path('booking/<str:u_id>/<str:action>/',
         views.BookingActionView.as_view(), name='accept_reject booking'),
    path('stylists/', views.StylistListView.as_view(), name='stylists-list'),
    path('stylists/<str:id>/', views.StylistDetailView.as_view(),
         name='stylist-detail'),
    path('approve-transaction/<str:u_id>/',
         views.ApproveTransactionAPIView.as_view(), name='approve_transaction'),

]
