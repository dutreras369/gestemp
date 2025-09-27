from __future__ import annotations
from .base import BaseModel

class RegistroTiempo(BaseModel):
    def __init__(self, empleado_id: int, proyecto_id: int, fecha: str, horas: float, descripcion: str | None = None) -> None:
        self.__id: int | None = None
        self.__empleado_id: int = int(empleado_id)
        self.__proyecto_id: int = int(proyecto_id)
        self.__fecha: str = fecha  # simplificado (YYYY-MM-DD)
        self.__horas: float = float(horas)
        self.__descripcion: str | None = descripcion

    @property
    def id(self) -> int | None: return self.__id
    @id.setter
    def id(self, value: int | None) -> None: self.__id = value

    @property
    def empleado_id(self) -> int: return self.__empleado_id
    @empleado_id.setter
    def empleado_id(self, value: int) -> None: self.__empleado_id = int(value)

    @property
    def proyecto_id(self) -> int: return self.__proyecto_id
    @proyecto_id.setter
    def proyecto_id(self, value: int) -> None: self.__proyecto_id = int(value)

    @property
    def fecha(self) -> str: return self.__fecha
    @fecha.setter
    def fecha(self, value: str) -> None: self.__fecha = value

    @property
    def horas(self) -> float: return self.__horas
    @horas.setter
    def horas(self, value: float) -> None:
        v = float(value)
        if v < 0 or v > 24:
            raise ValueError("RegistroTiempo: horas debe estar entre 0 y 24")
        self.__horas = v

    @property
    def descripcion(self) -> str | None: return self.__descripcion
    @descripcion.setter
    def descripcion(self, value: str | None) -> None: self.__descripcion = value

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "empleado_id": self.__empleado_id,
            "proyecto_id": self.__proyecto_id,
            "fecha": self.__fecha,
            "horas": self.__horas,
            "descripcion": self.__descripcion,
        }

    def validate(self) -> None:
        if self.__empleado_id <= 0:
            raise ValueError("RegistroTiempo: empleado_id inválido")
        if self.__proyecto_id <= 0:
            raise ValueError("RegistroTiempo: proyecto_id inválido")
        if not self.__fecha:
            raise ValueError("RegistroTiempo: fecha requerida")
        if self.__horas < 0 or self.__horas > 24:
            raise ValueError("RegistroTiempo: horas fuera de rango [0,24]")
