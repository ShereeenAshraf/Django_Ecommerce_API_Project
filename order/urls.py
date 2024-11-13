from django.urls import path
from .import views

urlpatterns = [
    path('orders_new/', views.new_order, name='new_order'),
    path('orders/', views.get_orders, name='orders'),
    path('get_order/<str:pk>', views.get_order, name='get_order'),
    path('order/<str:pk>/update/', views.update_order, name='update_order'),
    path('order/<str:pk>/delete/', views.delete_order, name='delete_order'),


]
