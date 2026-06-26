from django.test import TestCase
from django.contrib.auth.models import User
from .models import Categoria, Producto

class ProductoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Verduras', descripcion='Productos frescos')
        self.usuario = User.objects.create_user(username='testuser', password='testpass')

    def test_producto_creation(self):
        producto = Producto.objects.create(
            nombre='Tomate',
            descripcion='Tomate fresco',
            precio=2.50,
            stock=100,
            categoria=self.categoria
        )
        self.assertEqual(producto.nombre, 'Tomate')
        self.assertEqual(producto.precio, 2.50)
        self.assertEqual(producto.stock, 100)
        self.assertEqual(producto.categoria, self.categoria)

    def test_categoria_creation(self):
        categoria = Categoria.objects.create(
            nombre='Frutas',
            descripcion='Frutas frescas'
        )
        self.assertEqual(categoria.nombre, 'Frutas')
        self.assertTrue(categoria.descripcion, 'Frutas frescas')