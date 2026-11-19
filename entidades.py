"""
Módulo de entidades de Software FJ.
Contiene la clase abstracta Entidad y la clase Cliente.
"""

import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador):
        # Atributo protegido: solo las clases hijas deben usarlo directamente
        self._identificador = identificador

    @property
    def identificador(self):
        """Devuelve el identificador de la entidad (solo lectura)."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Cada entidad hija debe implementar su propia descripción."""
        pass


class Cliente(Entidad):
    """Representa a un cliente de Software FJ con datos personales encapsulados."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        # Atributos privados (doble guion bajo): encapsulación de datos personales
        self.__nombre = None
        self.__correo = None
        self.__telefono = None

        # Se usan los setters, que validan los datos antes de guardarlos
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- Nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Validación: debe ser texto y tener al menos 3 caracteres
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres."
            )
        self.__nombre = valor.strip()

    # ---------- Correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Validación: debe tener formato de correo (algo@dominio.ext)
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not isinstance(valor, str) or not re.match(patron, valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self.__correo = valor

    # ---------- Teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Validación: solo dígitos y entre 7 y 10 números
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{valor}'. Debe tener entre 7 y 10 dígitos."
            )
        self.__telefono = valor

    def describir(self):
        """Implementación del método abstracto: describe al cliente."""
        return f"Cliente {self._identificador}: {self.__nombre} ({self.__correo}, tel. {self.__telefono})"