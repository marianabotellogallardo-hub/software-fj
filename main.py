"""
Programa principal de Software FJ.
Simula 10 operaciones (válidas e inválidas) para demostrar que el sistema
sigue funcionando aunque ocurran errores.
"""

from logger import logger
from entidades import Cliente
from servicios import SalaReserva, AlquilerEquipo, Asesoria
from reservas import Reserva
from excepciones import ErrorSoftwareFJ

# Listas internas que reemplazan a una base de datos
clientes = []
servicios = []
reservas = []


def ejecutar(numero, descripcion, operacion):
    """
    Ejecuta una operación protegida: si falla, registra el error en el log
    y el programa continúa con la siguiente.
    """
    print(f"\n--- Operación {numero}: {descripcion} ---")
    try:
        resultado = operacion()
    except ErrorSoftwareFJ as e:
        # Errores propios del sistema
        logger.error(f"Operación {numero} falló: {e}")
        print(f"  ERROR CONTROLADO: {e}")
    except Exception as e:
        # Cualquier otro error inesperado tampoco detiene el programa
        logger.error(f"Operación {numero} falló inesperadamente: {e}")
        print(f"  ERROR INESPERADO: {e}")
    else:
        logger.info(f"Operación {numero} exitosa: {descripcion}")
        print(f"  OK: {resultado}")
    finally:
        logger.info(f"Operación {numero} finalizada")


# ---------- Funciones de cada operación ----------

def op_cliente_valido():
    c = Cliente(1, "Ana Pérez", "ana@correo.com", "3101234567")
    clientes.append(c)
    return c.describir()


def op_cliente_correo_invalido():
    c = Cliente(2, "Luis Gómez", "correo-malo", "3109876543")
    clientes.append(c)
    return c.describir()


def op_cliente_telefono_invalido():
    c = Cliente(3, "Marta Ruiz", "marta@correo.com", "12ab")
    clientes.append(c)
    return c.describir()


def op_sala_valida():
    s = SalaReserva(1, "Sala Ejecutiva", 50000, 10)
    servicios.append(s)
    return s.describir()


def op_equipo_valido():
    s = AlquilerEquipo(2, "Portátil Pro", 8000, "Portátil")
    servicios.append(s)
    return s.describir()


def op_asesoria_tarifa_invalida():
    s = Asesoria(3, "Asesoría en Datos", -500, "Datos")
    servicios.append(s)
    return s.describir()


def op_asesoria_valida():
    s = Asesoria(4, "Asesoría en Datos", 90000, "Ciencia de datos")
    servicios.append(s)
    return s.describir()


def op_reserva_exitosa():
    r = Reserva(clientes[0], servicios[0], 3)
    reservas.append(r)
    costo = r.procesar()
    return f"{r.resumen()} | costo final: ${costo}"


def op_reserva_horas_invalidas():
    r = Reserva(clientes[0], servicios[2], 10)  # asesoría de 10 horas
    reservas.append(r)
    return r.resumen()


def op_reserva_servicio_no_disponible():
    servicios[1].disponible = False  # se marca el equipo como no disponible
    r = Reserva(clientes[0], servicios[1], 5)
    reservas.append(r)
    r.confirmar()
    return r.resumen()


def op_cancelar_dos_veces():
    r = reservas[0]
    r.cancelar()
    r.cancelar()  # la segunda vez debe fallar
    return r.resumen()


# ---------- Ejecución de las operaciones ----------

if __name__ == "__main__":
    logger.info("===== INICIO DE LA SIMULACIÓN =====")

    ejecutar(1, "Registrar cliente válido", op_cliente_valido)
    ejecutar(2, "Registrar cliente con correo inválido", op_cliente_correo_invalido)
    ejecutar(3, "Registrar cliente con teléfono inválido", op_cliente_telefono_invalido)
    ejecutar(4, "Crear sala válida", op_sala_valida)
    ejecutar(5, "Crear alquiler de equipo válido", op_equipo_valido)
    ejecutar(6, "Crear asesoría con tarifa inválida", op_asesoria_tarifa_invalida)
    ejecutar(7, "Crear asesoría válida", op_asesoria_valida)
    ejecutar(8, "Reserva exitosa de sala", op_reserva_exitosa)
    ejecutar(9, "Reserva de asesoría con horas inválidas", op_reserva_horas_invalidas)
    ejecutar(10, "Confirmar reserva de servicio no disponible", op_reserva_servicio_no_disponible)
    ejecutar(11, "Cancelar la misma reserva dos veces", op_cancelar_dos_veces)

    print("\n===== RESUMEN FINAL =====")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios creados: {len(servicios)}")
    print(f"Reservas creadas: {len(reservas)}")
    logger.info("===== FIN DE LA SIMULACIÓN =====")