from django.db import models


# Modelo para Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    @staticmethod
    def obtener_producto_mas_vendido():
        # Obtiene el producto más vendido basado en las facturas
        return Producto.objects.annotate(total_vendido=models.Sum('item_factura__cantidad')).order_by('-total_vendido').first()


# Modelo para Item_Factura
class Item_Factura(models.Model):
    subtotal = models.FloatField()
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, related_name='item_factura', on_delete=models.CASCADE)

    def __str__(self):
        return self.producto.nombre

    def calcular_subtotal(self):
        return self.cantidad * self.producto.precio

    def calcular_total(self):
        return self.subtotal


# Modelo para Factura
class Factura(models.Model):
    numero = models.CharField(max_length=20)
    fecha = models.DateField()
    impuesto = models.FloatField()
    descuento = models.FloatField()
    total = models.FloatField()
    mesero= models.ForeignKey('Mesero', related_name='factura', on_delete=models.CASCADE, null=True)
    mesa= models.ForeignKey('Mesa', related_name='factura', on_delete=models.CASCADE, null=True)

    item_factura_list = models.ForeignKey(Item_Factura, related_name='factura', on_delete=models.CASCADE)

    def __str__(self):
        return self.numero

    def calcular_impuesto(self):
        # Calcula el impuesto total de la factura
        return sum([item.calcular_subtotal() for item in self.item_factura_list.all()]) * self.impuesto

    def calcular_descuento(self):
        # Calcula el descuento total de la factura
        return sum([item.calcular_subtotal() for item in self.item_factura_list.all()]) * self.descuento

    def calcular_total(self):
        # Calcula el total de la factura
        subtotal = sum([item.calcular_subtotal() for item in self.item_factura_list.all()])
        return subtotal + self.calcular_impuesto() - self.calcular_descuento()


# Modelo para Mesa
class Mesa(models.Model):
    cantidad_uso = models.IntegerField()
    codigo = models.CharField(max_length=20)

    def __str__(self):
        return self.codigo

    @staticmethod
    def obtener_mesa_mas_utilizada():
        # Obtiene la mesa más utilizada, basada en la cantidad de uso
        return Mesa.objects.annotate(uso_total=models.Sum('cantidad_uso')).order_by('-uso_total').first()


# Modelo para Persona
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


# Modelo para Mesero, que hereda de Persona
class Mesero(Persona):
    pedidosAtendidos = models.IntegerField()

    def actualizar_pedidos_atendidos(self):
        # Aumenta el número de pedidos atendidos
        self.pedidosAtendidos += 1
        self.save()

    @staticmethod
    def obtener_estadistica_pedidos():
            # Devuelve una lista con los nombres de los meseros y sus pedidos atendidos
            return Mesero.objects.values('nombre', 'pedidosAtendidos').order_by('-pedidosAtendidos')

    @staticmethod
    def obtener_mejor_mesero():
        # Obtiene el mesero con más pedidos atendidos
        return Mesero.objects.order_by('-pedidosAtendidos').first()


# Clase base para todas las estadísticas
class Estadistica(models.Model):
    titulo = models.CharField(max_length=50)

    @staticmethod
    def obtener_estadistica_producto():
        # Obtiene el producto más vendido
        return Producto.obtener_producto_mas_vendido()

    @staticmethod
    def obtener_estadistica_mesa():
        # Obtiene la mesa más utilizada
        return Mesa.obtener_mesa_mas_utilizada()

    @staticmethod
    def obtener_estadistica_mesero():
        # Obtiene el mejor mesero
        return Mesero.obtener_mejor_mesero()


# Clases específicas de estadística
class estadistica_mesero(Estadistica):
    mejor_mesero = models.CharField(max_length=50)
    factura_list = models.ForeignKey(Factura, related_name='estadistica_mesero', on_delete=models.CASCADE, null=True)

    def generar_estadistica(self):
        # Asignamos al mejor mesero
        mejor_mesero = self.obtener_estadistica_mesero()
        self.mejor_mesero = mejor_mesero.nombre
        self.save()


class estadistica_mesa(Estadistica):
    mesa_mas_usada = models.CharField(max_length=50)
    factura_list = models.ForeignKey(Factura, related_name='estadistica_mesa', on_delete=models.CASCADE, null=True)

    def generar_estadistica(self):
        # Asignamos la mesa más utilizada
        mesa_mas_usada = self.obtener_estadistica_mesa()
        self.mesa_mas_usada = mesa_mas_usada.codigo
        self.save()


class estadistica_producto(Estadistica):
    producto_mas_vendido = models.CharField(max_length=50)
    item_factura_list = models.ForeignKey(Item_Factura, related_name='estadistica_producto', on_delete=models.CASCADE, null=True)

    def generar_estadistica(self):
        # Asignamos el producto más vendido
        producto_mas_vendido = self.obtener_estadistica_producto()
        self.producto_mas_vendido = producto_mas_vendido.nombre
        self.save()


# Modelo para Reporte
class Reporte(models.Model):
    titulo = models.CharField(max_length=50)
    estadistica_list = models.ForeignKey(Estadistica, related_name='reporte', on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, related_name='reporte', on_delete=models.CASCADE, default=0000)
    grafico= models.ForeignKey('Grafico', related_name='reporte', on_delete=models.CASCADE, default=0000)

    class TipoReporte(models.TextChoices):
        DIARIO = 'DIARIO'
        SEMANAL = 'SEMANAL'
        MENSUAL = 'MENSUAL'

    class TipoArchivo(models.TextChoices):
        PDF = 'PDF'
        IMAGEN = 'IMAGEN'

    def generar_reporte(self, tipo_reporte):
        # Lógica para generar el reporte basado en el tipo
        if tipo_reporte == self.TipoReporte.DIARIO:
            # Generar reporte diario
            self.estadistica_list = f"Producto más vendido: {self.obtener_estadistica_producto().nombre}, Mesa más usada: {self.obtener_estadistica_mesa().codigo}, Mejor mesero: {self.obtener_estadistica_mesero().nombre}"
        elif tipo_reporte == self.TipoReporte.SEMANAL:
            # Generar reporte semanal
            pass
        elif tipo_reporte == self.TipoReporte.MENSUAL:
            # Generar reporte mensual
            pass
        self.save()

    def obtener_reporte(self):
        # Devuelve el reporte guardado
        return self.estadistica_list


# Modelo para Grafico (pendiente por detalles adicionales)
class Grafico(models.Model):
    titulo = models.CharField(max_length=50)
