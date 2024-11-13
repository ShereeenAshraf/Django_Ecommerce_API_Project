from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.get_all_products, name='products'),
    path('products/<str:pk>/', views.get_by_id_product, name='get_by_id_product'),
    path('productnew/', views.new_product, name='new_products'),
    path('productupdate/<str:pk>/', views.update_product, name='update_prodcut'),
    path('productdelete/<str:pk>/', views.delete_product, name='delete_prodcut'),
    # for review
    path('<str:pk>/reviews/', views.create_review, name='create_review'),
    path('<str:pk>/deletereview/', views.delete_review, name='delete_review'),


]
