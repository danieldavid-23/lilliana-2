import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.html import escape
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from .models import Producto, Categoria, Compra, Venta
from .forms import ProductoForm, CategoriaForm, CompraForm, VentaForm, RegistroUsuarioForm
from .decorators import admin_required, vendedor_required, comprador_required, superadmin_required

def home_view(request):
    return HttpResponseRedirect(reverse('producto_list'))

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_comprador, _ = Group.objects.get_or_create(name='Comprador')
            user.groups.add(grupo_comprador)
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}, tu cuenta ha sido creada.')
            return redirect('producto_list')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def producto_list(request):
    productos_list = Producto.objects.all().order_by('-created_at')
    paginator = Paginator(productos_list, 10)
    page = request.GET.get('page', 1)
    productos = paginator.get_page(page)
    categorias = Categoria.objects.all()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/producto_list_content.html', {
            'productos': productos, 'categorias': categorias
        })
    return render(request, 'agricola/producto_list.html', {
        'productos': productos, 'categorias': categorias
    })

@vendedor_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            producto = form.save(commit=False)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.save()
            messages.success(request, 'Producto creado exitosamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('producto_list')})
            return redirect('producto_list')
        elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'agricola/producto_form.html', {'form': form})
    else:
        form = ProductoForm()
    return render(request, 'agricola/producto_form.html', {'form': form})

@vendedor_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            producto = form.save(commit=False)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('producto_list')})
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'agricola/producto_form.html', {'form': form})

@admin_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('producto_list')})
        return redirect('producto_list')
    return render(request, 'agricola/producto_confirm_delete.html', {'producto': producto})

@login_required
def categoria_list(request):
    from django.db.models import Count
    categorias_list = Categoria.objects.annotate(total_productos=Count('productos')).order_by('-created_at')
    paginator = Paginator(categorias_list, 12)
    page = request.GET.get('page', 1)
    categorias = paginator.get_page(page)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/categoria_list_content.html', {'categorias': categorias})
    return render(request, 'agricola/categoria_list.html', {'categorias': categorias})

@admin_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            categoria = form.save(commit=False)
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            categoria.save()
            messages.success(request, 'Categoría creada exitosamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('categoria_list')})
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'agricola/categoria_form.html', {'form': form})

@admin_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            nombre = escape(form.cleaned_data['nombre'])
            descripcion = escape(form.cleaned_data['descripcion'])
            categoria = form.save(commit=False)
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            categoria.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('categoria_list')})
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'agricola/categoria_form.html', {'form': form})

@admin_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('categoria_list')})
        return redirect('categoria_list')
    return render(request, 'agricola/categoria_confirm_delete.html', {'categoria': categoria})

@login_required
def compra_list(request):
    es_comprador = not request.user.is_superuser and request.user.groups.filter(name='Comprador').exists() and not request.user.groups.filter(name__in=['Admin', 'Vendedor']).exists()
    if es_comprador:
        compras_list = Compra.objects.filter(usuario=request.user).order_by('-fecha_compra')
    else:
        compras_list = Compra.objects.all().order_by('-fecha_compra')
    paginator = Paginator(compras_list, 15)
    page = request.GET.get('page', 1)
    compras = paginator.get_page(page)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/compra_list_content.html', {'compras': compras})
    return render(request, 'agricola/compra_list.html', {'compras': compras})

@comprador_required
def compra_create(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user
            compra.save()
            compra.producto.stock += compra.cantidad
            compra.producto.save()
            messages.success(request, 'Compra registrada exitosamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('compra_list')})
            return redirect('compra_list')
    else:
        form = CompraForm()
    return render(request, 'agricola/compra_form.html', {'form': form})

@vendedor_required
def venta_list(request):
    ventas_list = Venta.objects.all().order_by('-fecha_venta')
    paginator = Paginator(ventas_list, 15)
    page = request.GET.get('page', 1)
    ventas = paginator.get_page(page)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/venta_list_content.html', {'ventas': ventas})
    return render(request, 'agricola/venta_list.html', {'ventas': ventas})

@vendedor_required
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            if venta.producto.stock < venta.cantidad:
                messages.error(request, f'Stock insuficiente. Disponible: {venta.producto.stock}')
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return render(request, 'agricola/venta_form.html', {'form': form})
                return render(request, 'agricola/venta_form.html', {'form': form})
            venta.save()
            venta.producto.stock -= venta.cantidad
            venta.producto.save()
            messages.success(request, 'Venta registrada exitosamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('venta_list')})
            return redirect('venta_list')
    else:
        form = VentaForm()
    return render(request, 'agricola/venta_form.html', {'form': form})

@admin_required
def categoria_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categorias.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Descripcion', 'Fecha Creacion'])
    for cat in Categoria.objects.all():
        writer.writerow([cat.id, cat.nombre, cat.descripcion, cat.created_at])
    return response

@admin_required
def producto_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Precio', 'Stock', 'Categoria', 'Fecha Creacion'])
    for prod in Producto.objects.all():
        writer.writerow([prod.id, prod.nombre, prod.precio, prod.stock, prod.categoria.nombre, prod.created_at])
    return response

@admin_required
def compra_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="compras.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Producto', 'Cantidad', 'Precio Unitario', 'Total', 'Usuario', 'Fecha'])
    for compra in Compra.objects.all():
        writer.writerow([compra.id, compra.producto.nombre, compra.cantidad, compra.precio_unitario, compra.total, compra.usuario.username, compra.fecha_compra])
    return response

@admin_required
def venta_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventas.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Producto', 'Cantidad', 'Precio Unitario', 'Total', 'Usuario', 'Fecha'])
    for venta in Venta.objects.all():
        writer.writerow([venta.id, venta.producto.nombre, venta.cantidad, venta.precio_unitario, venta.total, venta.usuario.username, venta.fecha_venta])
    return response

@admin_required
def usuario_list(request):
    usuarios_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(usuarios_list, 15)
    page = request.GET.get('page', 1)
    usuarios = paginator.get_page(page)
    grupos = Group.objects.all()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/usuario_list_content.html', {'usuarios': usuarios, 'grupos': grupos})
    return render(request, 'agricola/usuario_list.html', {'usuarios': usuarios, 'grupos': grupos})

@admin_required
def usuario_cambiar_rol(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        if nuevo_rol in ['Admin', 'Vendedor', 'Comprador']:
            usuario.groups.clear()
            grupo, _ = Group.objects.get_or_create(name=nuevo_rol)
            usuario.groups.add(grupo)
            messages.success(request, f'Rol de {usuario.username} cambiado a {nuevo_rol}')
        else:
            messages.error(request, 'Rol no valido')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('usuario_list')})
        return redirect('usuario_list')
    return redirect('usuario_list')

@superadmin_required
def usuario_create_admin(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol = request.POST.get('rol', 'Comprador')
            if rol in ['Admin', 'Vendedor', 'Comprador']:
                grupo, _ = Group.objects.get_or_create(name=rol)
                user.groups.add(grupo)
            messages.success(request, f'Usuario {user.username} creado con rol {rol}')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': reverse('usuario_list')})
            return redirect('usuario_list')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'agricola/usuario_create_form.html', {'form': form})

@superadmin_required
def usuario_delete(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo')
        return redirect('usuario_list')
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuario {usuario.username} eliminado')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('usuario_list')})
        return redirect('usuario_list')
    return render(request, 'agricola/usuario_confirm_delete.html', {'usuario': usuario})

@superadmin_required
def usuario_toggle_active(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes desactivarte a ti mismo')
        return redirect('usuario_list')
    usuario.is_active = not usuario.is_active
    usuario.save()
    estado = 'activado' if usuario.is_active else 'desactivado'
    messages.success(request, f'Usuario {usuario.username} {estado}')
    return redirect('usuario_list')

@admin_required
def reporte_view(request):
    from django.db.models import Count, Sum
    from django.utils import timezone
    total_ingresos = Venta.objects.aggregate(Sum('total'))['total__sum'] or 0
    total_gastos = Compra.objects.aggregate(Sum('total'))['total__sum'] or 0
    margen = total_ingresos - total_gastos
    margen_porcentaje = ((total_ingresos - total_gastos) / total_gastos * 100) if total_gastos > 0 else 0
    productos_mas_vendidos = Venta.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')[:5]
    categorias_mas_compradas = Compra.objects.values('producto__categoria__nombre').annotate(total_gastado=Sum('total')).order_by('-total_gastado')[:5]
    compras_por_mes = Compra.objects.extra(select={'mes': "strftime('%%Y-%%m', fecha_compra)"}).values('mes').annotate(total=Sum('total')).order_by('mes')[:6]
    ventas_por_mes = Venta.objects.extra(select={'mes': "strftime('%%Y-%%m', fecha_venta)"}).values('mes').annotate(total=Sum('total')).order_by('mes')[:6]
    context = {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'margen': margen,
        'margen_porcentaje': margen_porcentaje,
        'productos_mas_vendidos': productos_mas_vendidos,
        'categorias_mas_compradas': categorias_mas_compradas,
        'compras_por_mes': compras_por_mes,
        'ventas_por_mes': ventas_por_mes,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/reporte_content.html', context)
    return render(request, 'agricola/reporte.html', context)

@superadmin_required
def configuracion_view(request):
    from django.db.models import Count, Sum
    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    total_grupos = Group.objects.count()
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_compras = Compra.objects.count()
    total_ventas = Venta.objects.count()
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'limpiar_compras':
            Compra.objects.all().delete()
            messages.success(request, 'Todas las compras han sido eliminadas')
        elif accion == 'limpiar_ventas':
            Venta.objects.all().delete()
            messages.success(request, 'Todas las ventas han sido eliminadas')
        elif accion == 'reset_stock':
            Producto.objects.all().update(stock=0)
            messages.success(request, 'Stock de todos los productos reiniciado a 0')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('configuracion')})
        return redirect('configuracion')
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'total_grupos': total_grupos,
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_compras': total_compras,
        'total_ventas': total_ventas,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/configuracion_content.html', context)
    return render(request, 'agricola/configuracion.html', context)

@superadmin_required
def auditoria_view(request):
    from django.db.models import Count
    usuarios_por_rol = Group.objects.annotate(total=Count('user')).values('name', 'total')
    usuarios_recientes = User.objects.order_by('-date_joined')[:10]
    compras_recientes = Compra.objects.select_related('producto', 'usuario').order_by('-fecha_compra')[:10]
    ventas_recientes = Venta.objects.select_related('producto', 'usuario').order_by('-fecha_venta')[:10]
    context = {
        'usuarios_por_rol': usuarios_por_rol,
        'usuarios_recientes': usuarios_recientes,
        'compras_recientes': compras_recientes,
        'ventas_recientes': ventas_recientes,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/auditoria_content.html', context)
    return render(request, 'agricola/auditoria.html', context)

@login_required
def dashboard_view(request):
    from django.db.models import Count, Sum
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    es_comprador = not request.user.is_superuser and request.user.groups.filter(name='Comprador').exists() and not request.user.groups.filter(name__in=['Admin', 'Vendedor']).exists()
    if es_comprador:
        total_compras = Compra.objects.filter(usuario=request.user).count()
        total_gastos = Compra.objects.filter(usuario=request.user).aggregate(Sum('total'))['total__sum'] or 0
        total_ventas = 0
        total_ingresos = 0
        ventas_recientes = []
    else:
        total_compras = Compra.objects.count()
        total_ventas = Venta.objects.count()
        total_ingresos = Venta.objects.aggregate(Sum('total'))['total__sum'] or 0
        total_gastos = Compra.objects.aggregate(Sum('total'))['total__sum'] or 0
        ventas_recientes = Venta.objects.select_related('producto', 'usuario').order_by('-fecha_venta')[:5]
    productos_bajo_stock = Producto.objects.filter(stock__lt=10).count()
    categorias = Categoria.objects.annotate(total=Count('productos')).order_by('-total')[:5]
    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_compras': total_compras,
        'total_ventas': total_ventas,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'productos_bajo_stock': productos_bajo_stock,
        'categorias': categorias,
        'ventas_recientes': ventas_recientes,
        'es_comprador': es_comprador,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agricola/dashboard_content.html', context)
    return render(request, 'agricola/dashboard.html', context)
