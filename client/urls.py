from django.urls import path
from . import views

urlpatterns = [
    path('client/', views.ClientListView.as_view(), name='client-list'),
    path('client/<str:u_id>/', views.ClientDetailView.as_view(),
         name='client-detail'),
    path('styles/', views.StyleListView.as_view(),
         name='view styles'),
    path('styles/<str:category>/', views.StyleCategoryView.as_view(),
         name='view styles'),
    path('style/<str:u_id>/', views.StyleDetailView.as_view(),
         name='view style_detail'),
    path('style/category/', views.CategoryView.as_view(),
         name='view all_categories'),
    path('booking/', views.BookingView.as_view(),
         name='view_create booking'),
    path('booking/<str:u_id>/', views.BookingDetailView.as_view(),
         name='edit_delete booking'),

]
