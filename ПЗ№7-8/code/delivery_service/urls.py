from django.urls import path
from . import views

app_name = 'delivery_service'
urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stats, name='stats'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/',views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]