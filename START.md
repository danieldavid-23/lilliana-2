# Inicio Rápido - Sistema Agrícola

## Iniciar el Servidor de Desarrollo

Para iniciar el servidor de desarrollo de Django, ejecute el siguiente comando en la raíz del proyecto:

```bash
python manage.py runserver
```

Luego, abra su navegador web y vaya a `http://127.0.0.1:8000/agricola/productos/` para acceder al sistema.

## Panel de Administración

Para acceder al panel de administración de Django, vaya a `http://127.0.0.1:8000/admin/` e inicie sesión con las credenciales del superusuario que creó durante la instalación.

## Usuarios y Roles

El sistema implementa control de acceso basado en roles:
- Superusuarios tienen acceso completo a todas las funcionalidades
- Usuarios regulares pueden tener permisos limitados según la configuración

## Funcionalidades Disponibles

Una vez iniciado el servidor, podrá:

- Gestionar productos (crear, leer, actualizar, eliminar)
- Gestionar categorías de productos
- Registrar compras y ventas
- Visualizar listados con paginación
- Recibir alertas visuales para operaciones exitosas o con error

## Notas Importantes

- Asegúrese de tener instalado Python 3.8 o superior
- El sistema utiliza SQLite como base de datos por defecto
- Todos los recursos CSS y JS están alojados localmente (no depende de CDNs)
- El sistema incluye validaciones de entrada con expresiones regulares
- Se implementan medidas de seguridad XSS y CSRF