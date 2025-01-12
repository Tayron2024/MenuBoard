from django.contrib import admin
from .models import (
    Pedido, Producto, Cliente, Factura,
    ItemPedido, HistorialDeFactura, Promocion,
    PagoEfectivo, PagoTarjeta, PagoTransferencia, Impuesto
)
from django.utils.translation import gettext_lazy as _


class MontoFilter(admin.SimpleListFilter):
    title = _('Monto total')
    parameter_name = 'monto_total'

    def lookups(self, request, model_admin):
        return [
            ('<50', _('Menor a $50')),
            ('50-100', _('Entre $50 y $100')),
            ('>100', _('Mayor a $100')),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<50':
            return queryset.filter(factura__total__lt=50)
        if self.value() == '50-100':
            return queryset.filter(factura__total__gte=50, factura__total__lte=100)
        if self.value() == '>100':
            return queryset.filter(factura__total__gt=100)
        return queryset


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado', 'fecha', 'cliente', 'total_pedido')
    search_fields = ('numero', 'cliente__nombre')
    list_filter = ('estado',)
    inlines = [ItemPedidoInline]

    def total_pedido(self, obj):
        return f"${obj.total_pedido():.2f}" if obj.total_pedido() else "N/A"


class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'numero', 'pedido', 'cliente', 'subtotal', 'descuento', 'impuesto_total', 'total', 'fecha', 'metodo_pago', 'promocion'
    )
    readonly_fields = ('subtotal', 'descuento', 'impuesto_total', 'total')

    def save_model(self, request, obj, form, change):
        obj.calcular_monto_total()
        super().save_model(request, obj, form, change)

    def metodo_pago(self, obj):
        if obj.metodo_pago_efectivo:
            return obj.metodo_pago_efectivo.__str__()
        elif obj.metodo_pago_tarjeta:
            return obj.metodo_pago_tarjeta.__str__()
        elif obj.metodo_pago_transferencia:
            return obj.metodo_pago_transferencia.__str__()
        return "No especificado"

    def cliente(self, obj):
        return obj.pedido.cliente.nombre
    cliente.short_description = 'Cliente'


class HistorialDeFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'cliente', 'fecha', 'monto_total')
    search_fields = ('factura__numero', 'factura__pedido__cliente__nombre')
    list_filter = ('factura__fecha', MontoFilter)
    date_hierarchy = 'factura__fecha'

    def cliente(self, obj):
        return obj.factura.pedido.cliente.nombre

    def fecha(self, obj):
        return obj.factura.fecha

    def monto_total(self, obj):
        return f"${obj.factura.total:.2f}"


class PromocionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'porcentaje_descuento')


class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')


class ImpuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje', 'descripcion')


# Registro de modelos
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)
admin.site.register(HistorialDeFactura, HistorialDeFacturaAdmin)
admin.site.register(Promocion, PromocionAdmin)
admin.site.register(Impuesto, ImpuestoAdmin)
admin.site.register(PagoEfectivo)
admin.site.register(PagoTarjeta)
admin.site.register(PagoTransferencia)
