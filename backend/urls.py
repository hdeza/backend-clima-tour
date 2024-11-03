"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Importamos el módulo admin de Django para manejar el panel de administración.
from django.contrib import admin
# Importamos las funciones path e include para definir las rutas de URL.
from django.urls import path, include

# Definimos la lista de patrones de URL.
urlpatterns = [
    # Ruta para acceder al panel de administración de Django.
    path('admin/', admin.site.urls),
    # Incluimos las URLs de la aplicación 'api' en el prefijo 'api/'.
    path('api/', include('api.urls')),
]
