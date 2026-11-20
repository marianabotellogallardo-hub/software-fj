"""
Módulo de entidades de Software FJ.
Contiene la clase abstracta Entidad y la clase Cliente.
"""

# re: librería para validar textos con patrones (la usamos para el correo)
import re
# ABC y abstractmethod: permiten crear clases abstractas
from abc import ABC, abstractmethod

# Importamos nuestra excepción personalizada para los errores de cliente
from excepciones import ClienteInvalidoError


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador):
        # Atributo protegido (un guion bajo): solo las clases hijas deben usarlo directamente
        self._identificador = identificador

    @property
    def identificador(self):
        """Devuelve el identificador de la entidad (solo lectura)."""
        # No hay setter, así que el identificador no se puede cambiar desde afuera
        return self._identificador

    @abstractmethod
    def describir(self):
        """Cada entidad hija debe implementar su propia descripción."""
        # Al ser abstracto, no se puede crear una Entidad directamente
        pass


class Cliente(Entidad):
    """Representa a un cliente de Software FJ con datos personales encapsulados."""

    def __init__(self, identificador, nombre, correo, telefono):
        # Llama al constructor de la clase padre (Entidad) para guardar el identificador
        super().__init__(identificador)

        # Atributos privados (doble guion bajo): encapsulación de datos personales.
        # Empiezan en None y se llenan a través de los setters, que validan.
        self.__nombre = None
        self.__correo = None
        self.__telefono = None

        # Estas tres líneas llaman a los setters de abajo (no asignan directo),
        # por eso si un dato es inválido se lanza la excepción desde el inicio
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- Nombre ----------
    @property
    def nombre(self):
        # Getter: permite leer el nombre con cliente.nombre
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Validación: debe ser texto y tener al menos 3 caracteres (sin contar espacios)
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres."
            )
        # strip() elimina espacios sobrantes al inicio y al final
        self.__nombre = valor.strip()

    # ---------- Correo ----------
    @property
    def correo(self):
        # Getter: permite leer el correo
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Patrón de correo: texto + @ + dominio + punto + extensión (ej: ana@correo.com)
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        # Si no es texto o no coincide con el patrón, el correo es inválido
        if not isinstance(valor, str) or not re.match(patron, valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self.__correo = valor

    # ---------- Teléfono ----------
    @property
    def telefono(self):
        # Getter: permite leer el teléfono
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Validación: debe ser texto, solo dígitos y tener entre 7 y 10 números
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{valor}'. Debe tener entre 7 y 10 dígitos."
            )
        self.__telefono = valor

    def describir(self):
        """Implementación del método abstracto: describe al cliente."""
        # Devuelve un texto con los datos principales del cliente
        return f"Cliente {self._identificador}: {self.__nombre} ({self.__correo}, tel. {self.__telefono})"