from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Pedido, Factura, HistorialDeFactura
from django.db.models import Q

def pagina_inicio(request):
    return render(request, 'inicio.html')

def listar_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/historial_factura.html', {'facturas': facturas})

def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

def detalle_factura(request, numero):
    factura = Factura.objects.get(numero=numero)

    # Calcular impuestos totales
    impuestos_totales = factura.calcular_impuesto_total()

    # Calcular el total de la factura con impuestos y descuentos
    factura.calcular_monto_total()

    return render(request, 'facturas/detalle_factura.html', {
        'factura': factura,
        'impuesto_total': impuestos_totales,  # Enviamos los impuestos calculados
    })

def historial_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/historial_factura.html', {'facturas': facturas})

def filtrar_historial(request):
    cliente = request.GET.get('cliente', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    monto_total = request.GET.get('monto_total', '')

    filtros = Q()
    if cliente:
        filtros &= Q(pedido__cliente__nombre__icontains=cliente)
    if fecha_inicio and fecha_fin:
        filtros &= Q(fecha__range=[fecha_inicio, fecha_fin])

    if monto_total == '<50':
        filtros &= Q(total__lt=50)
    elif monto_total == '50-100':
        filtros &= Q(total__gte=50, total__lte=100)
    elif monto_total == '>100':
        filtros &= Q(total__gt=100)

    facturas = Factura.objects.filter(filtros)
    for factura in facturas:
        factura.calcular_monto_total()  # Aquí aseguras que se calculen correctamente los valores de impuestos, descuentos, etc.

    return render(request, 'facturas/historial_factura.html', {'facturas': facturas, 'cliente': cliente, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'monto_total': monto_total})

def detalle_pedido(request, numero):
    pedido = get_object_or_404(Pedido, numero=numero)
    items = pedido.itempedido_set.all()
    total_pedido = pedido.total_pedido()
    total_con_impuestos = pedido.total_pedido_con_impuestos()

    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'items': items,
        'total_pedido': total_pedido,
        'total_con_impuestos': total_con_impuestos
    })



def generar_factura_pdf(request, numero):
    # Obtener la factura por número
    factura = get_object_or_404(Factura, numero=numero)

    # Preparar el contexto con los detalles de la factura
    context = {
        'factura': factura,
    }

    # Cargar la plantilla HTML para la factura
    template_path = 'facturas/detalle_factura.html'  # Asegúrate de que la ruta sea correcta
    template = get_template(template_path)

    # Renderizar la plantilla con el contexto
    html = template.render(context)

    # Crear un buffer para almacenar el PDF
    pdf_buffer = BytesIO()

    # Generar el PDF utilizando xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    # Asegúrate de que el buffer se posicione al inicio
    pdf_buffer.seek(0)

    # Responder con el PDF generado
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.numero}.pdf"'

    return response