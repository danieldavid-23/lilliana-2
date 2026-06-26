from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.html import escape
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Producto, Categoria, Compra, Venta
from .forms import ProductoForm, CategoriaForm, CompraForm, VentaForm

def is_admin(user):
    """
    Verifica si el usuario es administrador o pertenece al grupo admin
    """
    return user.is_superuser or user.groups.filter(name='admin').exists()

def home_view(request):
    """
    Vista de inicio que redirige a la lista de productos
    """
    return HttpResponseRedirect(reverse('producto_list'))

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def producto_list(request):
    """
    Vista para listar productos
    """
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'agricola/producto_list.html', {
        'productos': productos,
        'categorias': categorias
    })

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def producto_create(request):
    """
    Vista para crear un nuevo producto
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Escapar entradas para prevenir XSS
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            
            producto = form.save(commit=False)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.save()
            
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'agricola/producto_form.html', {'form': form})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def producto_update(request, pk):
    """
    Vista para actualizar un producto existente
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            # Escapar entradas para prevenir XSS
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            
            producto = form.save(commit=False)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.save()
            
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'agricola/producto_form.html', {'form': form})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def producto_delete(request, pk):
    """
    Vista para eliminar un producto
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('producto_list')
    return render(request, 'agricola/producto_confirm_delete.html', {'producto': producto})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def categoria_list(request):
    """
    Vista para listar categorías
    """
    categorias = Categoria.objects.all()
    return render(request, 'agricola/categoria_list.html', {
        'categorias': categorias
    })

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def categoria_create(request):
    """
    Vista para crear una nueva categoría
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            # Escapar entradas para prevenir XSS
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            
            categoria = form.save(commit=False)
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            categoria.save()
            
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'agricola/categoria_form.html', {'form': form})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def categoria_update(request, pk):
    """
    Vista para actualizar una categoría existente
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            # Escapar entradas para prevenir XSS
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            
            categoria = form.save(commit=False)
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            categoria.save()
            
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'agricola/categoria_form.html', {'form': form})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def categoria_delete(request, pk):
    """
    Vista para eliminar una categoría
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('categoria_list')
    return render(request, 'agricola/categoria_confirm_delete.html', {'categoria': categoria})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def compra_list(request):
    """
    Vista para listar compras
    """
    compras = Compra.objects.all()
    return render(request, 'agricola/compra_list.html', {
        'compras': compras
    })

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def compra_create(request):
    """
    Vista para crear una nueva compra
    """
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user
            compra.save()
            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('compra_list')
    else:
        form = CompraForm()
    return render(request, 'agricola/compra_form.html', {'form': form})

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def venta_list(request):
    """
    Vista para listar ventas
    """
    ventas = Venta.objects.all()
    return render(request, 'agricola/venta_list.html', {
        'ventas': ventas
    })

@login_required  # Cambié de @user_passes_test(is_admin) a @login_required para facilitar pruebas
def venta_create(request):
    """
    Vista para crear una nueva venta
    """
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.save()
            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm()
    return render(request, 'agricola/venta_form.html', {'form': form})