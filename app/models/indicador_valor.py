from __future__ import annotations
from .base import BaseModel

class IndicadorValor(BaseModel):
    def __init__(self, nombre: str, fecha_valor: str, valor: float, proveedor: str) -> None:
        self.__id: int | None = None
        self.__nombre: str = nombre.upper()  # UF, IVP, IPC, UTM, DOLAR, EURO
        self.__fecha_valor: str = fecha_valor  # YYYY-MM-DD
        self.__valor: float = float(valor)
        self.__proveedor: str = proveedor

    @property
    def id(self) -> int | None: return self.__id
    @id.setter
    def id(self, v: int | None) -> None: self.__id = v

    @property
    def nombre(self) -> str: return self.__nombre
    @property
    def fecha_valor(self) -> str: return self.__fecha_valor
    @property
    def valor(self) -> float: return self.__valor
    @property
    def proveedor(self) -> str: return self.__proveedor

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "fecha_valor": self.__fecha_valor,
            "valor": self.__valor,
            "proveedor": self.__proveedor,
        }

    def validate(self) -> None:
        if self.__nombre not in ("UF","IVP","IPC","UTM","DOLAR","EURO"):
            raise ValueError("IndicadorValor: tipo no soportado")
        if not self.__fecha_valor:
            raise ValueError("IndicadorValor: fecha requerida")
        if self.__valor is None:
            raise ValueError("IndicadorValor: valor requerido")
        if not self.__proveedor:
            raise ValueError("IndicadorValor: proveedor requerido")
