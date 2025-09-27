from __future__ import annotations
from .base import BaseModel

def _is_email_ok(s: str) -> bool:
    return isinstance(s, str) and ("@" in s) and ("." in s)

class Empleado(BaseModel):
    def __init__(self, nombre: str, email: str, depto_id: int | None = None,
                 direccion: str | None = None, telefono: str | None = None,
                 fecha_inicio: str | None = None, salario: float = 0.0) -> None:
        self.__id: int | None = None
        self.__nombre: str = nombre
        self.__direccion: str | None = direccion
        self.__telefono: str | None = telefono
        self.__email: str = email
        self.__fecha_inicio: str | None = fecha_inicio  # simplificado (YYYY-MM-DD)
        self.__salario: float = float(salario)
        self.__depto_id: int | None = depto_id

    # Encapsulamiento
    @property
    def id(self) -> int | None: return self.__id
    @id.setter
    def id(self, value: int | None) -> None: self.__id = value

    @property
    def nombre(self) -> str: return self.__nombre
    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value: raise ValueError("Empleado: nombre requerido")
        self.__nombre = value

    @property
    def direccion(self) -> str | None: return self.__direccion
    @direccion.setter
    def direccion(self, value: str | None) -> None: self.__direccion = value

    @property
    def telefono(self) -> str | None: return self.__telefono
    @telefono.setter
    def telefono(self, value: str | None) -> None: self.__telefono = value

    @property
    def email(self) -> str: return self.__email
    @email.setter
    def email(self, value: str) -> None:
        if not _is_email_ok(value): raise ValueError("Empleado: email inválido")
        self.__email = value

    @property
    def fecha_inicio(self) -> str | None: return self.__fecha_inicio
    @fecha_inicio.setter
    def fecha_inicio(self, value: str | None) -> None: self.__fecha_inicio = value

    @property
    def salario(self) -> float: return self.__salario
    @salario.setter
    def salario(self, value: float) -> None:
        v = float(value)
        if v < 0: raise ValueError("Empleado: salario no puede ser negativo")
        self.__salario = v

    @property
    def depto_id(self) -> int | None: return self.__depto_id
    @depto_id.setter
    def depto_id(self, value: int | None) -> None: self.__depto_id = value

    # Polimorfismo
    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "direccion": self.__direccion,
            "telefono": self.__telefono,
            "email": self.__email,
            "fecha_inicio": self.__fecha_inicio,
            "salario": self.__salario,
            "depto_id": self.__depto_id,
        }

    def validate(self) -> None:
        if not self.__nombre:
            raise ValueError("Empleado: nombre vacío")
        if not _is_email_ok(self.__email):
            raise ValueError("Empleado: email inválido")
        if self.__salario < 0:
            raise ValueError("Empleado: salario negativo")
