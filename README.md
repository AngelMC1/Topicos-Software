# Ropium - Migración a Microservicios

**Fecha:** 14/04/26  
**Integrantes:** Cristian Cabezas, Juanes Villada y Miguel

## Descripción del proyecto

Este proyecto es una tienda web de productos importados llamada **Ropium**. La aplicación permite ver un catálogo de productos, agregarlos al carrito y finalizar un pedido por medio de un checkout.

Inicialmente el sistema estaba planteado como un monolito en **Django**, pero en este trabajo aplicamos una migración gradual usando el patrón **Strangler Pattern**, separando el módulo de checkout en un microservicio independiente hecho con **Flask**.

## ¿Qué hicimos?

En el proyecto se construyó una aplicación web con Django para manejar las páginas principales de la tienda, como inicio, catálogo, carrito y checkout. También se creó una API para listar productos, crear pedidos y consultar el detalle de un pedido.

Además, se separó la funcionalidad de creación de pedidos en un microservicio en Flask. La idea fue que el checkout pudiera funcionar aparte del monolito, sin tener que migrar toda la aplicación de una sola vez.

## Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- Flask
- Docker
- Docker Compose
- Nginx
- HTML
- CSS
- JavaScript
- Bootstrap
- SQLite

## Arquitectura general

El sistema quedó dividido en tres partes principales:

1. **Django**: maneja el monolito principal, las vistas del frontend y las rutas base de la aplicación.
2. **Flask**: maneja el nuevo microservicio encargado del checkout.
3. **Nginx**: funciona como proxy inverso para redirigir las peticiones según la ruta.

La ruta antigua del checkout en Django era:

```txt
/api/checkout/place-order/
```

La nueva ruta del microservicio en Flask es:

```txt
/api/v2/checkout/place-order/
```

## Módulo migrado

El módulo que se decidió migrar fue el de **creación de pedidos / checkout**, porque es una parte importante del negocio. En este proceso se validan los datos del cliente, los productos, las cantidades, la dirección y se calculan valores como subtotal, costo de importación, envío y total.

Se escogió este módulo porque puede cambiar con frecuencia y porque se puede separar sin afectar todo el sistema.

## Funcionalidades principales

- Página de inicio de la tienda.
- Catálogo de productos conectado a la API.
- Carrito de compras usando `localStorage`.
- Checkout con formulario de correo, ciudad y dirección.
- API para listar productos activos.
- API para crear pedidos.
- Microservicio Flask para procesar pedidos desde una nueva ruta.
- Nginx para redirigir tráfico entre Django y Flask.
- Docker Compose para levantar los servicios juntos.

## Patrones y buenas prácticas aplicadas

También se aplicaron algunas ideas de arquitectura para organizar mejor el código:

- **Service Layer**: se usó un servicio para manejar la lógica de creación de pedidos.
- **Builder Pattern**: se usó para construir y validar pedidos antes de guardarlos.
- **Factory Pattern**: se usó para decidir si la notificación se hace en modo MOCK o REAL.
- **Strangler Pattern**: se usó para migrar poco a poco una parte del monolito hacia un microservicio.

## Cómo ejecutar el proyecto

Para ejecutar el proyecto con Docker, se puede usar:

```bash
docker compose up --build
```

Después de levantar los servicios, se pueden revisar estas rutas:

```txt
http://localhost/
http://localhost/catalogo/
http://localhost/carrito/
http://localhost/checkout/
```

También se puede probar la nueva ruta del microservicio:

```txt
POST http://localhost/api/v2/checkout/place-order/
```

Ejemplo de JSON para probar el checkout:

```json
{
  "customer_email": "cliente@correo.com",
  "items": [
    {
      "product_id": 1,
      "qty": 2
    }
  ],
  "address": {
    "city": "Medellín",
    "address_line": "Cra 45 # 10 - 20"
  }
}
```

## Conclusión

Con este trabajo logramos pasar de una aplicación monolítica en Django a una arquitectura un poco más dividida, donde el checkout ya puede funcionar como microservicio en Flask. Esto permite entender cómo una empresa podría migrar partes de un sistema grande sin tener que rehacerlo todo desde cero.

En resumen, el proyecto muestra una tienda funcional, con frontend, API, lógica de negocio organizada y una primera migración usando Strangler Pattern.
