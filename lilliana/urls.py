"""lilliana URL Configuration

La ruta principal del proyecto que incluye las aplicaciones.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from agricola import views

def handler404_view(request, exception):
    return render(request, '404.html', status=404)

def handler500_view(request):
    return render(request, '500.html', status=500)

handler404 = handler404_view
handler500 = handler500_view

urlpatterns = [
    path('', RedirectView.as_view(url='/agricola/productos/', permanent=False)),
    path('admin/', admin.site.urls),
    path('agricola/', include('agricola.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_view, name='registro'),
]