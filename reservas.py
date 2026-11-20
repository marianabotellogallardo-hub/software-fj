"""
Módulo de reservas de Software FJ.
Contiene la clase Reserva, que une cliente, servicio, duración y estado.
"""

# Cliente y Servicio se importan para poder verificar el tipo de los objetos recibidos
from entidades import Cliente
from servicios import Servicio
# Excepciones propias que se lanzan o capturan en este módulo
from excepciones import (
    ErrorSoftwareFJ,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)
# Objeto para escribir en el archivo registro.log
from logger import logger


class Reserva:
    """Representa la reserva de un servicio hecha por un cliente."""

    # Estados posibles de una reserva (constantes de la clase)
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"

    def __init__(self, cliente, servicio, horas):
        # Validación de tipos: evita pasar objetos incorrectos a la reserva
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")

        # Guarda los datos de la reserva; toda reserva nueva empieza como "pendiente"
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = Reserva.PENDIENTE

        # Encadenamiento de excepciones: si las horas no son válidas para el servicio,
        # se lanza una ReservaInvalidaError que conserva el error original (from e)
        try:
            self.servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as e:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva: {e}"
            ) from e

    def confirmar(self):
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        # Solo se puede confirmar una reserva que esté pendiente
        if self.estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self.estado}."
            )
        # Si el servicio está marcado como no disponible, no se puede confirmar
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' no está disponible."
            )
        # Cambia el estado y deja constancia en el log
        self.estado = Reserva.CONFIRMADA
        logger.info(f"Reserva confirmada: {self.resumen()}")

    def cancelar(self):
        """Cancela la reserva si no estaba cancelada."""
        # No se puede cancelar dos veces la misma reserva
        if self.estado == Reserva.CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        # Cambia el estado y deja constancia en el log
        self.estado = Reserva.CANCELADA
        logger.info(f"Reserva cancelada: {self.resumen()}")

    def procesar(self, impuesto=0.19, descuento=0.0):
        """
        Procesa la reserva: confirma y calcula el costo final.
        Usa try/except/else/finally para controlar todo el flujo.
        """
        try:
            # Primero confirma (puede fallar) y luego calcula el costo (también puede fallar)
            self.confirmar()
            costo = self.servicio.calcular_costo(self.horas, impuesto, descuento)
        except ErrorSoftwareFJ as e:
            # Error controlado: se registra y se devuelve None, sin romper el programa
            logger.error(f"Fallo al procesar reserva: {e}")
            return None
        else:
            # Solo se ejecuta si NO hubo errores en el try
            logger.info(f"Reserva procesada. Costo final: ${costo}")
            return costo
        finally:
            # Se ejecuta SIEMPRE, haya o no error
            logger.info(f"Intento de procesamiento finalizado (estado: {self.estado})")

    def resumen(self):
        # Devuelve un texto corto con cliente, servicio, horas y estado
        return (
            f"{self.cliente.nombre} -> {self.servicio.nombre} "
            f"({self.horas}h) [{self.estado}]"
        )