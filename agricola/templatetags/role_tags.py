from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def has_group(user, group_name):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()

@register.filter
def is_comprador_puro(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return False
    return user.groups.filter(name='Comprador').exists() and not user.groups.filter(name__in=['Admin', 'Vendedor']).exists()
