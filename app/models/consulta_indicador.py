from __future__ import annotations
from .base import BaseModel

class ConsultaIndicador(BaseModel):
    def __init__(self, nombre: str, consultado_por: str, proveedor: str,
                 fecha_valor: str | None = None, desde: str | None = None, hasta: str | None = None) -> None:
        self.__id: int | None = None
        self.__nombre: str = nombre.upper()
        self.__fecha_valor: str | None = fecha_valor
        self.__desde: str | None = desde
        self.__hasta: str | None = hasta
        self.__consultado_por: str = consultado_por
        self.__proveedor: str = proveedor

    @property
    def id(self) -> int | None: return self.__id
    @id.setter
    def id(self, v: int | None) -> None: self.__id = v

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "fecha_valor": self.__fecha_valor,
            "desde": self.__desde,
            "hasta": self.__hasta,
            "consultado_por": self.__consultado_por,
            "proveedor": self.__proveedor,
        }

    def validate(self) -> None:
        if self.__nombre not in ("UF","IVP","IPC","UTM","DOLAR","EURO"):
            raise ValueError("ConsultaIndicador: tipo no soportado")
        if not self.__consultado_por:
            raise ValueError("ConsultaIndicador: requiere usuario")
        if not self.__proveedor:
            raise ValueError("ConsultaIndicador: requiere proveedor")
