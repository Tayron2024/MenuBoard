# MenuBoard

# Proyecto
MenuBoard es un sistema de gestión de restaurantes diseñado para facilitar la administración de restaurantes, cafeterías o cualquier establecimiento de alimentos y bebidas. La aplicación permite crear, modificar y gestionar menús de manera eficiente, proporcionando a los usuarios una interfaz sencilla para realizar actualizaciones rápidas, gestionar categorías de platos y actualizar precios de forma intuitiva.


## Descripción
MenuBoard es un proyecto orientado a simplificar la gestión de menús digitales. El sistema permite a los administradores agregar platos, organizar menús por categorías y modificar descripciones o precios de manera dinámica. El objetivo principal es ofrecer una herramienta que permita la actualización en tiempo real de los menús, brindando flexibilidad para adaptarse a cambios en los ingredientes, promociones o ajustes de precios.


### Funcionalidades

#### Módulo de Mesas y Reservaciones
Este módulo gestiona la disponibilidad y uso de las mesas dentro del restaurante. Las mesas pueden estar en diferentes estados, tales como libre, ocupada o reservada. Los clientes pueden hacer reservaciones de mesas con antelación, especificando la fecha y hora de la reserva. Es necesario gestionar las características de cada mesa, como el número de asientos y su ubicación en el restaurante. Cuando un cliente llega, una mesa puede ser asignada, y al finalizar su uso, la mesa debe ser liberada para otros clientes. Las reservaciones pueden ser modificadas o canceladas por el cliente o el personal del restaurante.

##### Requerimientos:

* Registrar la cantidad total de mesas en el restaurante.
* Asignar, liberar y modificar el estado de las mesas.
* Crear, modificar y eliminar reservaciones.
* Controlar la disponibilidad de las mesas según el tiempo de reserva.
* Notificar al personal cuando una mesa está lista para ser asignada.
#### Módulo de Pedidos
El módulo de pedidos permite gestionar los pedidos de los clientes, desde que se realiza el pedido hasta que es servido y pagado. Cada pedido puede contener uno o más productos del menú, y es posible agregar o eliminar productos mientras el pedido no haya sido servido. El sistema debe permitir modificar cantidades de productos en los pedidos, así como su estado (pendiente, en preparación, servido, pagado). El personal del restaurante puede visualizar y actualizar el estado de cada pedido. Además, se requiere tener un registro histórico de todos los pedidos realizados en el restaurante para futuras consultas.

##### Requerimientos:
* Crear, modificar y eliminar pedidos.
* Agregar y eliminar productos de un pedido.
* Modificar la cantidad de productos dentro de un pedido.
* Cambiar el estado del pedido (pendiente, en preparación, servido, pagado).
* Visualizar el historial de pedidos por mesa o por cliente.
* Generar un resumen del pedido para la cocina.

#### Módulo de Menús y Productos
Este módulo permite gestionar los productos y platos que se ofrecen en el restaurante. Cada producto tiene atributos como nombre, descripción, categoría, precio y disponibilidad. El menú puede estar organizado en categorías, como entradas, platos principales, postres y bebidas. El sistema debe permitir agregar nuevos productos al menú, modificarlos o eliminarlos cuando sea necesario. Además, se requiere que los productos puedan estar temporalmente fuera de stock o deshabilitados para su venta si los ingredientes no están disponibles. También se debe mantener un control de precios, permitiendo actualizarlos según sea necesario.

##### Requerimientos:
* Crear, modificar y eliminar productos del menú.
* Clasificar productos en categorías.
* Controlar la disponibilidad de los productos (en stock o no disponible).
* Modificar precios de productos en el menú.
* Visualizar el menú en un formato accesible para el personal.

#### Módulo de Facturación y Pagos
Este módulo es responsable de generar la factura para los clientes al finalizar su pedido. La factura debe calcular automáticamente el total del pedido, incluyendo impuestos y descuentos aplicables. Además, debe permitir seleccionar el método de pago, ya sea en efectivo, tarjeta de crédito o débito, entre otros. El sistema debe generar un comprobante de pago que puede ser impreso o enviado al correo del cliente. También es necesario mantener un registro de todas las facturas emitidas para efectos contables y de auditoría.

##### Requerimientos:
* Generar facturas para cada pedido.
* Calcular el total del pedido con impuestos y descuentos aplicables.
* Registrar diferentes métodos de pago (efectivo, tarjeta, etc.).
* Permitir la impresión o envío digital de la factura.
* Mantener un historial de todas las facturas emitidas.

#### Módulo de Inventario
El módulo de inventario permite gestionar los insumos y productos necesarios para la preparación de los platos del restaurante. Cada insumo debe ser registrado con información como nombre, cantidad disponible y unidad de medida. El sistema debe permitir registrar entradas de nuevos insumos y salidas de los mismos cuando se utilizan en la preparación de los productos del menú. Además, es necesario generar alertas cuando el inventario de un insumo esté bajo o agotado. También debe permitir generar reportes de consumo de insumos y de stock disponible para facilitar la reposición.

##### Requerimientos:
* Registrar y controlar el inventario de insumos.
* Registrar entradas y salidas de insumos del inventario.
* Generar alertas cuando los niveles de inventario son bajos.
* Visualizar el inventario de todos los insumos.
* Generar reportes de consumo y stock de insumos.

#### Módulo de Reportes y Estadísticas
Este módulo proporciona información sobre el desempeño del restaurante a través de reportes y estadísticas. Los reportes incluyen datos sobre las ventas diarias, productos más vendidos, mesas más utilizadas, ingresos generados, y el desempeño de los empleados. El sistema debe permitir generar reportes personalizados por rango de fechas y categorías específicas, como ventas por categoría de producto o por empleado. Además, se deben generar gráficos y tablas que faciliten la interpretación de los datos.

##### Requerimientos:
* Generar reportes de ventas diarias, semanales y mensuales.
* Visualizar estadísticas sobre productos más vendidos y mesas más utilizadas.
* Generar reportes de ingresos por categoría de producto.
* Producir gráficos que resuman el desempeño del restaurante.
* Personalizar reportes por fecha y categoría.