from __future__ import annotations
from typing import Optional
from .helpers import execute, fetchall, fetchone

class UsuarioService:
    @staticmethod
    def crear(username: str, password_hash: str, rol: str = "usuario") -> int:
        sql = "INSERT INTO usuarios (username, password_hash, rol) VALUES (%s,%s,%s)"
        return execute(sql, (username, password_hash, rol))

    @staticmethod
    def obtener_por_username(username: str) -> Optional[dict]:
        return fetchone("SELECT id, username, password_hash, rol, creado_en FROM usuarios WHERE username=%s", (username,))

    @staticmethod
    def listar() -> list[dict]:
        return fetchall("SELECT id, username, rol, creado_en FROM usuarios ORDER BY id DESC")

    @staticmethod
    def cambiar_rol(user_id: int, nuevo_rol: str) -> bool:
        execute("UPDATE usuarios SET rol=%s WHERE id=%s", (nuevo_rol, user_id))
        return True

    @staticmethod
    def eliminar(user_id: int) -> bool:
        execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
        return True
