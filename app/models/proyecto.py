from __future__ import annotations
from .base import BaseModel

class Proyecto(BaseModel):
    def __init__(self, nombre: str, descripcion: str | None = None, fecha_inicio: str | None = None) -> None:
        self.__id: int | None = None
        self.__nombre: str = nombre
        self.__descripcion: str | None = descripcion
        self.__fecha_inicio: str | None = fecha_inicio

    @property
    def id(self) -> int | None: return self.__id
    @id.setter
    def id(self, value: int | None) -> None: self.__id = value

    @property
    def nombre(self) -> str: return self.__nombre
    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value: raise ValueError("Proyecto: nombre requerido")
        self.__nombre = value

    @property
    def descripcion(self) -> str | None: return self.__descripcion
    @descripcion.setter
    def descripcion(self, value: str | None) -> None: self.__descripcion = value

    @property
    def fecha_inicio(self) -> str | None: return self.__fecha_inicio
    @fecha_inicio.setter
    def fecha_inicio(self, value: str | None) -> None: self.__fecha_inicio = value

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "descripcion": self.__descripcion,
            "fecha_inicio": self.__fecha_inicio,
        }

    def validate(self) -> None:
        if not self.__nombre:
            raise ValueError("Proyecto: nombre vacío")
