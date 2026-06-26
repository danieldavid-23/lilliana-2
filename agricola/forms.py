from django import forms
from django.core.validators import RegexValidator
from .models import Producto, Categoria, Compra, Venta
import re

# Validador de nombre con regex: al menos 3 caracteres alfabéticos
nombre_validator = RegexValidator(
    regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{3,}$',
    message='El nombre debe tener al menos 3 caracteres y solo contener letras.'
)

# Validador de precio con regex: números positivos con hasta 2 decimales
precio_validator = RegexValidator(
    regex=r'^\d+(\.\d{1,2})?$',
    message='Ingrese un precio válido con hasta 2 decimales.'
)

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=200,
        validators=[nombre_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del producto (mínimo 3 caracteres)'
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[precio_validator],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio del producto',
            'step': '0.01'
        })
    )
    
    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad en stock'
        })
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=100,
        validators=[nombre_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de la categoría (mínimo 3 caracteres)'
        })
    )

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }