from __future__ import annotations
from .base import BaseModel

class Usuario(BaseModel):
    def __init__(self, username: str, password_hash: str, rol: str = "usuario") -> None:
        self.__id: int | None = None
        self.__username: str = username
        self.__password_hash: str = password_hash
        self.__rol: str = rol  # 'admin' | 'gerente' | 'usuario'

    @property
    def id(self) -> int | None: return self.__id
    @id.setter
    def id(self, value: int | None) -> None: self.__id = value

    @property
    def username(self) -> str: return self.__username
    @username.setter
    def username(self, value: str) -> None:
        if not value: raise ValueError("Usuario: username requerido")
        self.__username = value

    @property
    def password_hash(self) -> str: return self.__password_hash
    @password_hash.setter
    def password_hash(self, value: str) -> None:
        if not value or len(value) < 10:
            raise ValueError("Usuario: hash inválido")
        self.__password_hash = value

    @property
    def rol(self) -> str: return self.__rol
    @rol.setter
    def rol(self, value: str) -> None:
        if value not in ("admin", "gerente", "usuario"):
            raise ValueError("Usuario: rol inválido")
        self.__rol = value

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "username": self.__username,
            "password_hash": self.__password_hash,
            "rol": self.__rol,
        }

    def validate(self) -> None:
        if not self.__username:
            raise ValueError("Usuario: username vacío")
        if self.__rol not in ("admin", "gerente", "usuario"):
            raise ValueError("Usuario: rol inválido")
        if not self.__password_hash or len(self.__password_hash) < 10:
            raise ValueError("Usuario: hash inválido")
