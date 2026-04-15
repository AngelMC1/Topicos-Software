# Migración a Microservicios (Strangler Pattern)

## Módulo Estrangulado
**Checkout / Creación de pedidos**  
Ruta original en Django: `/api/checkout/place-order/`  
Ruta nueva en Flask: `/api/v2/checkout/place-order/`

---

## Matriz de decisión

| Módulo | Frecuencia de cambio | Consumo de recursos | Acoplamiento | Decisión |
|---|---|---:|---|---|
| Listado de productos | Baja | Bajo | Alto | Mantener en Django |
| Crear pedido / checkout | Alta | Medio | Medio | Estrangular a Flask |
| Detalle de pedido | Media | Bajo | Alto | Mantener en Django |

---

## Justificación

Se decidió estrangular el módulo de **creación de pedidos (checkout)** porque concentra la mayor parte de la lógica de negocio del sistema.  
Este proceso valida los productos activos, verifica cantidades, calcula subtotal, costo de importación, costo de envío y valor total del pedido.

A diferencia del listado de productos y la consulta de detalle del pedido, el checkout cambia con más frecuencia porque allí suelen modificarse reglas de negocio relacionadas con cobros, validaciones y procesamiento del pedido.

También es un buen candidato porque puede aislarse como un servicio independiente que reciba y responda JSON, sin necesidad de migrar todo el sistema.  
De esta forma, el monolito en Django sigue funcionando para las demás rutas, mientras el nuevo microservicio en Flask asume la funcionalidad crítica seleccionada.