from django.db import models

# Modelo del Menú
class Menu(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField()

    def _str_(self):
        return self.nombre

    def activar_menu(self):
        self.estado = True
        self.save()

    def desactivar_menu(self):
        self.estado = False
        self.save()

# Modelo de Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categorias')

    def _str_(self):
        return self.nombre

    def agregar_producto(self, producto):
        producto.categoria = self
        producto.save()

    def eliminar_producto(self, producto_id):
        Producto.objects.filter(id=producto_id, categoria=self).delete()

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    precio = models.FloatField()
    disponibilidad = models.BooleanField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def _str_(self):
        return self.nombre

    def cambiar_disponibilidad(self, disponible):
        self.disponibilidad = disponible
        self.save()

# Implementación de la interfaz IMenu
class IMenu:

    @staticmethod
    def agregar_producto(id_categoria, producto):
        categoria = Categoria.objects.get(id=id_categoria)
        producto.categoria = categoria
        producto.save()

    @staticmethod
    def eliminar_producto(id_categoria, id_producto):
        Categoria.objects.get(id=id_categoria).productos.filter(id=id_producto).delete()

    @staticmethod
    def agregar_categoria(menu_id, categoria):
        menu = Menu.objects.get(id=menu_id)
        categoria.menu = menu
        categoria.save()

    @staticmethod
    def eliminar_categoria(id_categoria):
        Categoria.objects.filter(id=id_categoria).delete()

    @staticmethod
    def modificar_categoria(categoria):
        Categoria.objects.filter(id=categoria.id).update(nombre=categoria.nombre)

    @staticmethod
    def modificar_producto(producto):
        Producto.objects.filter(id=producto.id).update(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            disponibilidad=producto.disponibilidad
        )

    @staticmethod
    def buscar_categoria(nombre):
        return Categoria.objects.filter(nombre__icontains=nombre)

    @staticmethod
    def buscar_producto(nombre):
        return Producto.objects.filter(nombre__icontains=nombre)

    @staticmethod
    def mostrar_menu(menu_id):
        menu = Menu.objects.get(id=menu_id)
        return {
            "menu": menu,
            "categorias": menu.categorias.all()
        }