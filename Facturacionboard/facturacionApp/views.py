from django.shortcuts import render, get_object_or_404
from .models import Pedido, Factura, HistorialDeFactura

def pagina_inicio(request):
    return render(request, 'inicio.html')

def listar_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/historial_factura.html', {'facturas': facturas})

def detalle_factura(request, numero):
    factura = get_object_or_404(Factura, numero=numero)
    return render(request, 'facturas/detalle_factura.html', {'factura': factura})

def historial_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/historial_factura.html', {'facturas': facturas})