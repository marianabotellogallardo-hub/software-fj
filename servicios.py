"""
Módulo de servicios de Software FJ.
Contiene la clase abstracta Servicio y tres servicios especializados:
SalaReserva, AlquilerEquipo y Asesoria.
"""

# ABC y abstractmethod: permiten crear clases y métodos abstractos
from abc import ABC, abstractmethod

# Servicio hereda de Entidad (la clase abstracta de entidades.py)
from entidades import Entidad
# Excepciones propias que usamos para validar servicios y cálculos
from excepciones import (
    ServicioInvalidoError,
    CalculoInconsistenteError,
)


class Servicio(Entidad, ABC):
    """Clase abstracta base de todos los servicios."""

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        # Guarda el identificador usando el constructor de Entidad
        super().__init__(identificador)
        # Atributos privados (doble guion bajo): encapsulación
        self.__nombre = nombre
        self.__disponible = disponible
        # Atributo protegido: las clases hijas lo necesitan para calcular costos
        self._tarifa_hora = None
        # Se valida la tarifa ANTES de guardarla; si es mala, lanza la excepción
        self._validar_tarifa(tarifa_hora)
        self._tarifa_hora = tarifa_hora

    # ---------- Propiedades ----------
    @property
    def nombre(self):
        # Getter: permite leer el nombre del servicio
        return self.__nombre

    @property
    def disponible(self):
        # Getter: indica si el servicio se puede reservar
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        # Solo se acepta True o False; cualquier otro valor es un error
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self.__disponible = valor

    @property
    def tarifa_hora(self):
        # Getter: permite leer la tarifa por hora
        return self._tarifa_hora

    @staticmethod
    def _validar_tarifa(tarifa):
        """Valida que la tarifa sea un número positivo."""
        # staticmethod: no necesita acceder al objeto (self), solo revisa el valor
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ServicioInvalidoError(
                f"Tarifa inválida: '{tarifa}'. Debe ser un número mayor que 0."
            )

    # ---------- Métodos abstractos (cada hijo los implementa distinto) ----------
    @abstractmethod
    def calcular_costo_base(self, horas):
        """Calcula el costo base según las horas y el tipo de servicio."""
        # Sin código: cada servicio hijo define su propia fórmula
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        """Valida los parámetros propios de cada servicio."""
        # Sin código: cada servicio hijo define sus propios límites de horas
        pass

    # ---------- Método "sobrecargado" (parámetros opcionales) ----------
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo final. Simula sobrecarga con parámetros opcionales:
          calcular_costo(2)                      -> solo costo base
          calcular_costo(2, impuesto=0.19)       -> con IVA
          calcular_costo(2, 0.19, 0.10)          -> con IVA y descuento
        """
        # Primero valida las horas según el tipo de servicio (polimorfismo)
        self.validar_parametros(horas)
        # Impuesto y descuento deben ser porcentajes entre 0 (0%) y 1 (100%)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                "Impuesto y descuento deben estar entre 0 y 1."
            )
        # Cada hijo calcula su costo base de forma distinta (polimorfismo)
        base = self.calcular_costo_base(horas)
        # Se aplica primero el descuento y luego el impuesto
        total = base * (1 - descuento) * (1 + impuesto)
        # Verificación de seguridad: un costo negativo no tiene sentido
        if total < 0:
            raise CalculoInconsistenteError("El costo total no puede ser negativo.")
        # Redondea a 2 decimales
        return round(total, 2)

    def describir(self):
        # Implementa el método abstracto heredado de Entidad
        estado = "disponible" if self.__disponible else "no disponible"
        return f"{self.__nombre} (tarifa ${self._tarifa_hora}/h, {estado})"


class SalaReserva(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        # Reutiliza el constructor de Servicio para los datos comunes
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        # Validación propia de la sala: capacidad entera y positiva
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
        # Fórmula de la sala: tarifa por hora x horas
        return self._tarifa_hora * horas

    def describir(self):
        # super().describir() trae la descripción general y aquí se agrega la capacidad
        return f"Sala: {super().describir()}, capacidad {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo, disponible=True):
        # Reutiliza el constructor de Servicio para los datos comunes
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        # Validación propia: el tipo de equipo no puede estar vacío
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo es obligatorio.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas):
        # Los equipos se alquilan entre 1 y 72 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Los equipos se alquilan entre 1 y 72 horas.")

    def calcular_costo_base(self, horas):
        # Fórmula del equipo: tarifa x horas + cargo fijo de entrega de $10000
        return self._tarifa_hora * horas + 10000

    def describir(self):
        # Agrega el tipo de equipo a la descripción general
        return f"Equipo ({self.tipo_equipo}): {super().describir()}"


class Asesoria(Servicio):
    """Servicio de asesoría especializada."""

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        # Reutiliza el constructor de Servicio para los datos comunes
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        # Validación propia: la especialidad no puede estar vacía
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, horas):
        # Las asesorías duran entre 1 y 4 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 4:
            raise ServicioInvalidoError("Las asesorías duran entre 1 y 4 horas.")

    def calcular_costo_base(self, horas):
        # Fórmula de la asesoría: tarifa x horas con 25% de recargo por ser especializada
        return self._tarifa_hora * horas * 1.25

    def describir(self):
        # Agrega la especialidad a la descripción general
        return f"Asesoría de {self.especialidad}: {super().describir()}"