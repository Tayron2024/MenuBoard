from django.db import models
from datetime import date

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    correo_electronico = models.EmailField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio
        self.save()


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
        ('ENPROCESO', 'En Proceso'),
    ]

    numero = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha = models.DateField(default=date.today)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemPedido')

    def agregar_item(self, producto, cantidad):
        item, created = ItemPedido.objects.get_or_create(pedido=self, producto=producto)
        item.cantidad += cantidad
        item.precio_unitario = producto.precio  # Usamos el precio del producto automáticamente
        item.save()

    def total_pedido(self):
        return sum(item.subtotal() for item in self.itempedido_set.all())

    def __str__(self):
        return f"Pedido {self.numero} - {self.cliente.nombre}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.FloatField()

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"


class Factura(models.Model):
    numero = models.AutoField(primary_key=True)
    total = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)  # Se agrega el campo para el subtotal
    impuesto_total = models.FloatField(default=0.0)
    descuento = models.FloatField(default=0.0)
    fecha = models.DateField(default=date.today)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago_efectivo = models.ForeignKey('PagoEfectivo', null=True, blank=True, on_delete=models.SET_NULL)
    metodo_pago_tarjeta = models.ForeignKey('PagoTarjeta', null=True, blank=True, on_delete=models.SET_NULL)
    metodo_pago_transferencia = models.ForeignKey('PagoTransferencia', null=True, blank=True, on_delete=models.SET_NULL)
    promocion = models.ForeignKey('Promocion', null=True, blank=True, on_delete=models.SET_NULL)

    def calcular_monto_total(self):
        subtotal = self.pedido.total_pedido()
        impuestos = self.impuesto_total  # El valor del impuesto se toma de la propiedad
        descuento = self.descuento
        total_con_descuento = subtotal - descuento + impuestos
        self.subtotal = subtotal
        self.total = total_con_descuento
        self.impuesto_total = impuestos
        self.save()

    def aplicar_promocion(self):
        if self.promocion:
            self.promocion.aplicar_promocion(self)

    def generar_comprobante(self):
        return {
            "Factura": self.numero,
            "Cliente": self.pedido.cliente.nombre,
            "Productos": [
                {
                    "Producto": item.producto.nombre,
                    "Cantidad": item.cantidad,
                    "Precio Unitario": item.precio_unitario,
                    "Subtotal": item.subtotal(),
                }
                for item in self.pedido.itempedido_set.all()
            ],
            "Subtotal": self.subtotal,
            "Descuento": self.descuento,
            "Impuestos": self.impuesto_total,
            "Total": self.total,
            "Metodo de Pago Efectivo": self.metodo_pago_efectivo.__str__() if self.metodo_pago_efectivo else "No especificado",
            "Metodo de Pago Tarjeta": self.metodo_pago_tarjeta.__str__() if self.metodo_pago_tarjeta else "No especificado",
            "Metodo de Pago Transferencia": self.metodo_pago_transferencia.__str__() if self.metodo_pago_transferencia else "No especificado",
            "Promocion Aplicada": self.promocion.descripcion if self.promocion else "Ninguna",
        }

    def __str__(self):
        return f"Factura {self.numero} para Pedido {self.pedido.numero}"


class Promocion(models.Model):
    descripcion = models.CharField(max_length=255)
    porcentaje_descuento = models.FloatField()

    def aplicar_promocion(self, factura):
        descuento = factura.pedido.total_pedido() * (self.porcentaje_descuento / 100)
        factura.descuento = descuento
        factura.calcular_monto_total()

    def __str__(self):
        return self.descripcion


class MetodoDePago(models.Model):
    monto_pagado = models.FloatField()
    cuenta_por_cobrar = models.FloatField()

    class Meta:
        abstract = True


class PagoTransferencia(MetodoDePago):
    numero_transferencia = models.CharField(max_length=50)
    banco_origen = models.CharField(max_length=255)


class PagoEfectivo(MetodoDePago):
    cambio = models.FloatField()


class PagoTarjeta(MetodoDePago):
    numero_tarjeta = models.CharField(max_length=16)
    titular = models.CharField(max_length=255)
    vencimiento = models.DateField()


class HistorialDeFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    @classmethod
    def consultar_por_fecha(cls, fecha_inicio, fecha_fin):
        return cls.objects.filter(factura__fecha__range=[fecha_inicio, fecha_fin])

    @classmethod
    def consultar_por_cliente(cls, cliente):
        return cls.objects.filter(factura__pedido__cliente=cliente)

    def __str__(self):
        return f"Historial de Factura {self.factura.numero}"
