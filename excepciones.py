"""
Módulo de excepciones personalizadas de Software FJ.
Cada excepción representa un tipo de error específico del sistema.
"""


# Excepción base: todas las demás heredan de ella.
# Gracias a esto, con "except ErrorSoftwareFJ" puedo capturar cualquier error del sistema.
class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las demás excepciones del sistema heredan de ella."""
    pass  # No necesita código extra: solo sirve para dar un nombre propio al error


# Se usa cuando el nombre, correo o teléfono de un cliente no cumplen las reglas
class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no son válidos."""
    pass


# Se usa cuando una tarifa, capacidad o dato de un servicio es incorrecto
class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de un servicio no son válidos."""
    pass


# Se usa cuando se intenta reservar un servicio marcado como no disponible
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""
    pass


# Se usa cuando una reserva no se puede crear (tipos incorrectos o horas inválidas)
class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no se puede crear o procesar."""
    pass


# Se usa cuando se pide algo que el estado actual no permite (ej: cancelar dos veces)
class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""
    pass


# Se usa cuando impuesto, descuento o costo total dan valores sin sentido
class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos da un resultado inconsistente."""
    pass