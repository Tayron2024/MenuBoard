"""
URL configuration for Facturacionboard project.

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
from django.urls import path
from facturacionApp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagina_inicio, name='inicio'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('facturas/<int:numero>/pdf/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('pedidos/<int:numero>/', views.detalle_pedido, name='detalle_pedido'),
    path('facturas/<int:numero>/', views.detalle_factura, name='detalle_factura'),
    path('historial/', views.historial_facturas, name='historial_facturas'),
    path('historial/filtrar/', views.filtrar_historial, name='filtrar_historial'),
    path('factura/<int:numero>/pdf/', views.generar_factura_pdf, name='generar_factura_pdf'),
]
