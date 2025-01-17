from django.contrib import admin
from .models import Menu, Categoria, Producto

class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 1  # Número de categorías adicionales que se mostrarán por defecto
    fields = ('nombre',)  # Campos que se mostrarán en el formulario de categoría

# Personalización de la administración del modelo Menu
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')  # Muestra columnas en la lista de administración
    list_filter = ('estado',)  # Filtro por estado
    search_fields = ('nombre',)  # Búsqueda por nombre

    actions = ['activar_menus', 'desactivar_menus']  # Acciones personalizadas
    inlines = [CategoriaInline]  # Permite gestionar categorías desde el menú
    @admin.action(description='Activar menús seleccionados')
    def activar_menus(self, request, queryset):
        queryset.update(estado=True)


    @admin.action(description='Desactivar menús seleccionados')
    def desactivar_menus(self, request, queryset):
        queryset.update(estado=False)


# Personalización de la administración del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'menu')  # Muestra columnas de nombre y menú
    list_filter = ('menu',)  # Filtro por menú
    search_fields = ('nombre',)  # Búsqueda por nombre


# Personalización de la administración del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'disponibilidad', 'categoria')  # Muestra detalles del producto
    list_filter = ('disponibilidad', 'categoria')  # Filtro por disponibilidad y categoría
    search_fields = ('nombre', 'descripcion')  # Búsqueda por nombre y descripción

    actions = ['cambiar_a_disponible', 'cambiar_a_no_disponible']  # Acciones personalizadas

    @admin.action(description='Marcar como disponible')
    def cambiar_a_disponible(self, request, queryset):
        queryset.update(disponibilidad=True)

    @admin.action(description='Marcar como no disponible')
    def cambiar_a_no_disponible(self, request, queryset):
        queryset.update(disponibilidad=False)

