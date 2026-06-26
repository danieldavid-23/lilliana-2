from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from agricola.models import Producto, Categoria, Compra, Venta

class Command(BaseCommand):
    help = 'Crea los grupos de roles por defecto (Admin, Vendedor, Comprador)'

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
        comprador_group, _ = Group.objects.get_or_create(name='Comprador')

        for model in [Producto, Categoria, Compra, Venta]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            admin_group.permissions.add(*perms)
            if model in [Producto, Venta]:
                vendedor_group.permissions.add(*perms)
            if model == Compra:
                comprador_group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS('Grupos creados exitosamente: Admin, Vendedor, Comprador'))
