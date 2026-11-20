"""
Programa principal de Software FJ.
Simula 11 operaciones (válidas e inválidas) para demostrar que el sistema
sigue funcionando aunque ocurran errores.
"""

# Objeto para escribir en el archivo registro.log
from logger import logger
# Clases del sistema que vamos a usar en la simulación
from entidades import Cliente
from servicios import SalaReserva, AlquilerEquipo, Asesoria
from reservas import Reserva
# Excepción base: sirve para capturar cualquier error propio del sistema
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
        # Se ejecuta la función que recibimos como parámetro
        resultado = operacion()
    except ErrorSoftwareFJ as e:
        # Errores propios del sistema (cliente inválido, reserva inválida, etc.)
        logger.error(f"Operación {numero} falló: {e}")
        print(f"  ERROR CONTROLADO: {e}")
    except Exception as e:
        # Cualquier otro error inesperado tampoco detiene el programa
        logger.error(f"Operación {numero} falló inesperadamente: {e}")
        print(f"  ERROR INESPERADO: {e}")
    else:
        # Solo se ejecuta si la operación salió bien
        logger.info(f"Operación {numero} exitosa: {descripcion}")
        print(f"  OK: {resultado}")
    finally:
        # Se ejecuta siempre, haya o no error
        logger.info(f"Operación {numero} finalizada")


# ---------- Funciones de cada operación ----------

def op_cliente_valido():
    # Cliente con todos los datos correctos: debe registrarse sin problema
    c = Cliente(1, "Ana Pérez", "ana@correo.com", "3101234567")
    clientes.append(c)
    return c.describir()


def op_cliente_correo_invalido():
    # Correo sin formato válido: debe lanzar ClienteInvalidoError
    c = Cliente(2, "Luis Gómez", "correo-malo", "3109876543")
    clientes.append(c)
    return c.describir()


def op_cliente_telefono_invalido():
    # Teléfono con letras y muy corto: debe lanzar ClienteInvalidoError
    c = Cliente(3, "Marta Ruiz", "marta@correo.com", "12ab")
    clientes.append(c)
    return c.describir()


def op_sala_valida():
    # Sala con datos correctos: se agrega a la lista de servicios (posición 0)
    s = SalaReserva(1, "Sala Ejecutiva", 50000, 10)
    servicios.append(s)
    return s.describir()


def op_equipo_valido():
    # Equipo con datos correctos: queda en la posición 1 de la lista
    s = AlquilerEquipo(2, "Portátil Pro", 8000, "Portátil")
    servicios.append(s)
    return s.describir()


def op_asesoria_tarifa_invalida():
    # Tarifa negativa: debe lanzar ServicioInvalidoError
    s = Asesoria(3, "Asesoría en Datos", -500, "Datos")
    servicios.append(s)
    return s.describir()


def op_asesoria_valida():
    # Asesoría con datos correctos: queda en la posición 2 de la lista
    s = Asesoria(4, "Asesoría en Datos", 90000, "Ciencia de datos")
    servicios.append(s)
    return s.describir()


def op_reserva_exitosa():
    # Reserva de la sala (servicios[0]) por 3 horas para el cliente 0
    r = Reserva(clientes[0], servicios[0], 3)
    reservas.append(r)
    # procesar() confirma la reserva y calcula el costo con IVA
    costo = r.procesar()
    return f"{r.resumen()} | costo final: ${costo}"


def op_reserva_horas_invalidas():
    # Asesoría (servicios[2]) de 10 horas: supera el máximo de 4, falla al crear
    r = Reserva(clientes[0], servicios[2], 10)
    reservas.append(r)
    return r.resumen()


def op_reserva_servicio_no_disponible():
    # Se marca el equipo como no disponible y luego se intenta confirmar
    servicios[1].disponible = False
    r = Reserva(clientes[0], servicios[1], 5)
    reservas.append(r)
    # confirmar() debe lanzar ServicioNoDisponibleError
    r.confirmar()
    return r.resumen()


def op_cancelar_dos_veces():
    # Toma la primera reserva y la cancela dos veces
    r = reservas[0]
    r.cancelar()
    # La segunda cancelación debe lanzar OperacionNoPermitidaError
    r.cancelar()
    return r.resumen()


# ---------- Ejecución de las operaciones ----------

# Este bloque solo corre si ejecutamos main.py directamente
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

    # Resumen final: cuántos objetos quedaron en cada lista
    print("\n===== RESUMEN FINAL =====")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios creados: {len(servicios)}")
    print(f"Reservas creadas: {len(reservas)}")
    logger.info("===== FIN DE LA SIMULACIÓN =====")