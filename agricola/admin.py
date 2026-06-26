from django.contrib import admin
from .models import Categoria, Producto, Compra, Venta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'created_at']
    search_fields = ['nombre']
    list_filter = ['created_at']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'categoria', 'created_at']
    search_fields = ['nombre']
    list_filter = ['categoria', 'created_at']

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'precio_unitario', 'total', 'usuario', 'fecha_compra']
    search_fields = ['producto__nombre', 'usuario__username']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'precio_unitario', 'total', 'usuario', 'fecha_venta']
    search_fields = ['producto__nombre', 'usuario__username']
