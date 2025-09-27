from __future__ import annotations
from .base import BaseModel

class Departamento(BaseModel):
    def __init__(self, nombre: str, gerente: str | None = None) -> None:
        self.__id: int | None = None
        self.__nombre: str = nombre
        self.__gerente: str | None = gerente

    # Encapsulamiento con properties
    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, value: int | None) -> None:
        self.__id = value

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value:
            raise ValueError("El nombre de departamento es requerido")
        self.__nombre = value

    @property
    def gerente(self) -> str | None:
        return self.__gerente

    @gerente.setter
    def gerente(self, value: str | None) -> None:
        self.__gerente = value

    # Polimorfismo
    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "gerente": self.__gerente,
        }

    def validate(self) -> None:
        if not self.__nombre:
            raise ValueError("Departamento: nombre vacío")
