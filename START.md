# Inicio Rápido - Sistema Agrícola

## Requisitos
- Python 3.8+
- Django 6.0+
- pip

## 1. Instalación

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear grupos de roles
python manage.py crear_grupos

# Superusuario
python manage.py createsuperuser
```

## 2. Iniciar Servidor

```bash
python manage.py runserver
```

Acceder a: `http://127.0.0.1:8000/agricola/dashboard/`

## 3. Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/agricola/dashboard/` | Panel de control con estadísticas |
| `/agricola/productos/` | Gestión de productos |
| `/agricola/categorias/` | Gestión de categorías |
| `/agricola/compras/` | Registro de compras |
| `/agricola/ventas/` | Registro de ventas |
| `/admin/` | Panel de administración Django |
| `/registro/` | Crear cuenta nueva |
| `/login/` | Iniciar sesión |

## 4. Roles del Sistema

| Rol | Permisos |
|-----|----------|
| Admin | Acceso completo a todo el sistema |
| Vendedor | Gestionar productos y ventas |
| Comprador | Registrar compras |

## 5. Características

- **SPA**: Navegación sin recarga con pushState
- **Seguridad**: 4 capas (autenticación, autorización, protección, validación)
- **Diseño**: Tema agrícola responsivo con Bootstrap 5.3 local
- **Validaciones**: Regex en todos los campos críticos
- **Alertas**: Sistema de mensajes con auto-ocultación
- **Stock**: Actualización automática en compras/ventas
- **Exportación**: Categorías exportables a CSV
- **Paginación**: Listas paginadas para mejor rendimiento
