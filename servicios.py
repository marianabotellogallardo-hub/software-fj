"""
Módulo de servicios de Software FJ.
Contiene la clase abstracta Servicio y tres servicios especializados:
SalaReserva, AlquilerEquipo y Asesoria.
"""

from abc import ABC, abstractmethod

from entidades import Entidad
from excepciones import (
    ServicioInvalidoError,
    CalculoInconsistenteError,
)


class Servicio(Entidad, ABC):
    """Clase abstracta base de todos los servicios."""

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        self.__nombre = nombre
        self.__disponible = disponible
        self._tarifa_hora = None
        # Se valida la tarifa antes de guardarla
        self._validar_tarifa(tarifa_hora)
        self._tarifa_hora = tarifa_hora

    # ---------- Propiedades ----------
    @property
    def nombre(self):
        return self.__nombre

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self.__disponible = valor

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @staticmethod
    def _validar_tarifa(tarifa):
        """Valida que la tarifa sea un número positivo."""
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ServicioInvalidoError(
                f"Tarifa inválida: '{tarifa}'. Debe ser un número mayor que 0."
            )

    # ---------- Métodos abstractos (cada hijo los implementa distinto) ----------
    @abstractmethod
    def calcular_costo_base(self, horas):
        """Calcula el costo base según las horas y el tipo de servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        """Valida los parámetros propios de cada servicio."""
        pass

    # ---------- Método "sobrecargado" (parámetros opcionales) ----------
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo final. Simula sobrecarga con parámetros opcionales:
          calcular_costo(2)                      -> solo costo base
          calcular_costo(2, impuesto=0.19)       -> con IVA
          calcular_costo(2, 0.19, 0.10)          -> con IVA y descuento
        """
        self.validar_parametros(horas)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                "Impuesto y descuento deben estar entre 0 y 1."
            )
        base = self.calcular_costo_base(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo total no puede ser negativo.")
        return round(total, 2)

    def describir(self):
        estado = "disponible" if self.__disponible else "no disponible"
        return f"{self.__nombre} (tarifa ${self._tarifa_hora}/h, {estado})"


class SalaReserva(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(
                f"Capacidad inválida: '{capacidad}'. Debe ser un entero positivo."
            )
        self.capacidad = capacidad

    def validar_parametros(self, horas):
        # Las salas se reservan entre 1 y 8 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError("Las salas se reservan entre 1 y 8 horas.")

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas

    def describir(self):
        return f"Sala: {super().describir()}, capacidad {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo es obligatorio.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas):
        # Los equipos se alquilan entre 1 y 72 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Los equipos se alquilan entre 1 y 72 horas.")

    def calcular_costo_base(self, horas):
        # Cargo fijo de entrega de $10000 sobre la tarifa por hora
        return self._tarifa_hora * horas + 10000

    def describir(self):
        return f"Equipo ({self.tipo_equipo}): {super().describir()}"


class Asesoria(Servicio):
    """Servicio de asesoría especializada."""

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, horas):
        # Las asesorías duran entre 1 y 4 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 4:
            raise ServicioInvalidoError("Las asesorías duran entre 1 y 4 horas.")

    def calcular_costo_base(self, horas):
        # Las asesorías tienen un recargo del 25% por ser especializadas
        return self._tarifa_hora * horas * 1.25

    def describir(self):
        return f"Asesoría de {self.especialidad}: {super().describir()}"