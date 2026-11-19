"""
Módulo de excepciones personalizadas de Software FJ.
Cada excepción representa un tipo de error específico del sistema.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las demás excepciones del sistema heredan de ella."""
    pass


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no son válidos."""
    pass


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de un servicio no son válidos."""
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no se puede crear o procesar."""
    pass


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""
    pass


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos da un resultado inconsistente."""
    pass