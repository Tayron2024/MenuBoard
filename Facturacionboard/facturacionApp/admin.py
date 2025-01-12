from django.contrib import admin
from .models import (
    Pedido, Producto, Cliente, Factura,
    ItemPedido, HistorialDeFactura, Promocion,
    PagoEfectivo, PagoTarjeta, PagoTransferencia
)

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # Filas vacías por defecto para agregar más productos


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado', 'fecha', 'cliente', 'total_pedido')  # Asegúrate de que 'total_pedido' está en list_display
    search_fields = ('numero', 'cliente__nombre')  # Búsqueda por número de pedido o cliente
    list_filter = ('estado',)  # Filtro por estado
    inlines = [ItemPedidoInline]  # Mostrar los productos del pedido en línea

    def total_pedido(self, obj):
        return f"${obj.total_pedido():.2f}" if obj.total_pedido() else "N/A"


class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'numero', 'pedido', 'cliente', 'subtotal', 'descuento', 'impuesto_total', 'total', 'fecha', 'metodo_pago', 'promocion'
    )
    search_fields = ('numero', 'pedido__numero', 'pedido__cliente__nombre')
    list_filter = ('fecha', 'metodo_pago_efectivo', 'metodo_pago_tarjeta', 'metodo_pago_transferencia', 'promocion')

    def metodo_pago(self, obj):
        if obj.metodo_pago_efectivo:
            return obj.metodo_pago_efectivo.__str__()
        elif obj.metodo_pago_tarjeta:
            return obj.metodo_pago_tarjeta.__str__()
        elif obj.metodo_pago_transferencia:
            return obj.metodo_pago_transferencia.__str__()
        return "No especificado"
    metodo_pago.short_description = 'Método de Pago'

    def cliente(self, obj):
        return obj.pedido.cliente.nombre
    cliente.short_description = 'Cliente'


class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('pedido__numero', 'producto__nombre')

    def subtotal(self, obj):
        return f"${obj.subtotal():.2f}"
    subtotal.short_description = 'Subtotal'


class PromocionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'porcentaje_descuento')


class PagoEfectivoAdmin(admin.ModelAdmin):
    list_display = ('monto_pagado', 'cambio')


class PagoTarjetaAdmin(admin.ModelAdmin):
    list_display = ('monto_pagado', 'numero_tarjeta', 'titular', 'vencimiento')


class PagoTransferenciaAdmin(admin.ModelAdmin):
    list_display = ('monto_pagado', 'numero_transferencia', 'banco_origen')


class HistorialDeFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'cliente', 'fecha_factura')
    search_fields = ('factura__numero', 'factura__pedido__cliente__nombre')  # Buscar por factura o cliente

    def cliente(self, obj):
        return obj.factura.pedido.cliente.nombre
    cliente.short_description = 'Cliente'

    def fecha_factura(self, obj):
        return obj.factura.fecha
    fecha_factura.short_description = 'Fecha de Factura'


# Registro de modelos en el panel de administración
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)
admin.site.register(Promocion, PromocionAdmin)
admin.site.register(PagoEfectivo, PagoEfectivoAdmin)
admin.site.register(PagoTarjeta, PagoTarjetaAdmin)
admin.site.register(PagoTransferencia, PagoTransferenciaAdmin)
admin.site.register(HistorialDeFactura, HistorialDeFacturaAdmin)
