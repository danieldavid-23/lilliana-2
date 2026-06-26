from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/create/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/edit/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/delete/', views.producto_delete, name='producto_delete'),
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/create/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/edit/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/delete/', views.categoria_delete, name='categoria_delete'),
    path('compras/', views.compra_list, name='compra_list'),
    path('compras/create/', views.compra_create, name='compra_create'),
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/create/', views.venta_create, name='venta_create'),
]