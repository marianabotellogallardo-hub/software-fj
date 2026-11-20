# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 del curso Programación (213023) de la UNAD.

## Descripción

Sistema orientado a objetos en Python para la empresa ficticia Software FJ, que ofrece reservas de salas, alquiler de equipos y asesorías especializadas. No usa base de datos: la información se maneja con objetos y listas, y solo se usa un archivo para registrar eventos y errores.

## Conceptos aplicados

- Abstracción: clases abstractas `Entidad` y `Servicio`
- Herencia: `Cliente` hereda de `Entidad`; `SalaReserva`, `AlquilerEquipo` y `Asesoria` heredan de `Servicio`
- Polimorfismo: cada servicio calcula su costo y valida sus parámetros a su manera
- Encapsulación: atributos privados con validación en los setters
- Manejo de excepciones: excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas |
| `logger.py` | Configuración del archivo de logs |
| `entidades.py` | Clase abstracta `Entidad` y clase `Cliente` |
| `servicios.py` | Clase abstracta `Servicio` y sus tres servicios |
| `reservas.py` | Clase `Reserva` |
| `main.py` | Simulación de 11 operaciones válidas e inválidas |
| `registro.log` | Registro de eventos y errores |

## Cómo ejecutarlo

1. Instalar Python 3.11 o superior.
2. Descargar los archivos del repositorio en una misma carpeta.
3. Ejecutar en la terminal:

```
python main.py
```

Los eventos y errores quedan guardados en `registro.log`.

## Autora

Mariana Alexandra Botello Gallardo
