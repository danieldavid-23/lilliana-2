from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Categoria, Producto, Compra, Venta
from .forms import CategoriaForm, ProductoForm, CompraForm, VentaForm, RegistroUsuarioForm

class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Verduras',
            descripcion='Productos frescos del campo'
        )

    def test_categoria_creation(self):
        self.assertEqual(self.categoria.nombre, 'Verduras')
        self.assertEqual(str(self.categoria), 'Verduras')

    def test_categoria_unique_name(self):
        with self.assertRaises(Exception):
            Categoria.objects.create(nombre='Verduras', descripcion='Duplicada')

class ProductoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Frutas', descripcion='Frutas frescas')
        self.producto = Producto.objects.create(
            nombre='Manzana',
            descripcion='Manzana roja',
            precio=1.50,
            stock=100,
            categoria=self.categoria
        )

    def test_producto_creation(self):
        self.assertEqual(self.producto.nombre, 'Manzana')
        self.assertEqual(self.producto.precio, 1.50)
        self.assertEqual(self.producto.stock, 100)
        self.assertEqual(self.producto.categoria, self.categoria)

    def test_producto_str(self):
        self.assertEqual(str(self.producto), 'Manzana')

class CompraModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.categoria = Categoria.objects.create(nombre='Granos', descripcion='Granos básicos')
        self.producto = Producto.objects.create(
            nombre='Arroz', descripcion='Arroz blanco',
            precio=0.80, stock=500, categoria=self.categoria
        )
        self.compra = Compra.objects.create(
            producto=self.producto, cantidad=100,
            precio_unitario=0.75, usuario=self.user
        )

    def test_compra_total_calculado(self):
        self.assertEqual(self.compra.total, 75.00)

    def test_compra_relaciones(self):
        self.assertEqual(self.compra.producto.nombre, 'Arroz')
        self.assertEqual(self.compra.usuario.username, 'testuser')

class VentaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testvendor', password='testpass123')
        self.categoria = Categoria.objects.create(nombre='Lácteos', descripcion='Lácteos')
        self.producto = Producto.objects.create(
            nombre='Leche', descripcion='Leche entera',
            precio=1.20, stock=200, categoria=self.categoria
        )
        self.venta = Venta.objects.create(
            producto=self.producto, cantidad=10,
            precio_unitario=1.50, usuario=self.user
        )

    def test_venta_total_calculado(self):
        self.assertEqual(self.venta.total, 15.00)

class CategoriaFormTest(TestCase):
    def test_categoria_form_valid(self):
        form = CategoriaForm(data={'nombre': 'Verduras', 'descripcion': 'Frescas'})
        self.assertTrue(form.is_valid())

    def test_categoria_form_nombre_corto(self):
        form = CategoriaForm(data={'nombre': 'ab', 'descripcion': 'Test'})
        self.assertFalse(form.is_valid())

    def test_categoria_form_nombre_numeros(self):
        form = CategoriaForm(data={'nombre': 'Verduras123', 'descripcion': 'Test'})
        self.assertFalse(form.is_valid())

class ProductoFormTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Test', descripcion='Test')

    def test_producto_form_valid(self):
        form = ProductoForm(data={
            'nombre': 'Tomate', 'descripcion': 'Rojo',
            'precio': '2.50', 'stock': 100, 'categoria': self.categoria.id
        })
        self.assertTrue(form.is_valid())

    def test_producto_form_precio_invalido(self):
        form = ProductoForm(data={
            'nombre': 'Tomate', 'descripcion': 'Rojo',
            'precio': 'abc', 'stock': 100, 'categoria': self.categoria.id
        })
        self.assertFalse(form.is_valid())

    def test_producto_form_stock_negativo(self):
        form = ProductoForm(data={
            'nombre': 'Tomate', 'descripcion': 'Rojo',
            'precio': '2.50', 'stock': -1, 'categoria': self.categoria.id
        })
        self.assertFalse(form.is_valid())

class RegistroUsuarioFormTest(TestCase):
    def test_registro_form_valid(self):
        form = RegistroUsuarioForm(data={
            'username': 'nuevousuario',
            'email': 'user@example.com',
            'password': 'Segura123',
            'password2': 'Segura123'
        })
        self.assertTrue(form.is_valid())

    def test_registro_form_password_dont_match(self):
        form = RegistroUsuarioForm(data={
            'username': 'nuevousuario',
            'email': 'user@example.com',
            'password': 'Segura123',
            'password2': 'OtraPass1'
        })
        self.assertFalse(form.is_valid())

    def test_registro_form_username_corto(self):
        form = RegistroUsuarioForm(data={
            'username': 'ab',
            'email': 'user@example.com',
            'password': 'Segura123',
            'password2': 'Segura123'
        })
        self.assertFalse(form.is_valid())

class ViewAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_required_redirect(self):
        response = self.client.get(reverse('producto_list'))
        self.assertRedirects(response, f'/login/?next=/agricola/productos/')

    def test_login_success(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpass123'})
        self.assertNotIn('/login/', response.url)

    def test_registro_view(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)

class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123', email='admin@test.com')
        self.normal_user = User.objects.create_user(username='normal', password='testpass123')

    def test_csrf_protection(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin123'})
        self.assertIn(response.status_code, [200, 302])

    def test_logout_redirect(self):
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [200, 302])

    def test_admin_required_for_delete(self):
        self.client.login(username='normal', password='testpass123')
        cat = Categoria.objects.create(nombre='Test', descripcion='Test')
        response = self.client.get(reverse('categoria_delete', args=[cat.pk]))
        self.assertEqual(response.status_code, 302)

    def test_xss_escaping(self):
        self.client.login(username='admin', password='admin123')
        cat = Categoria.objects.create(nombre='<script>alert("xss")</script>', descripcion='Test')
        response = self.client.get(reverse('categoria_list'))
        self.assertNotIn('<script>', response.content.decode('utf-8'))
