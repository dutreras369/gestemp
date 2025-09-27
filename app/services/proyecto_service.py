from __future__ import annotations
from typing import Optional
from app.models.proyecto import Proyecto
from .helpers import execute, fetchall, fetchone

class ProyectoService:
    @staticmethod
    def crear(p: Proyecto) -> int:
        p.validate()
        pid = execute("INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES (%s,%s,%s)",
                      (p.nombre, p.to_dict()["descripcion"], p.to_dict()["fecha_inicio"]))
        p.id = pid
        return pid

    @staticmethod
    def listar() -> list[dict]:
        return fetchall("SELECT id, nombre, descripcion, fecha_inicio, creado_en FROM proyectos ORDER BY id DESC")

    @staticmethod
    def obtener(pid: int) -> Optional[dict]:
        return fetchone("SELECT id, nombre, descripcion, fecha_inicio, creado_en FROM proyectos WHERE id=%s", (pid,))

    @staticmethod
    def actualizar(pid: int, nombre: Optional[str] = None, descripcion: Optional[str] = None, fecha_inicio: Optional[str] = None) -> bool:
        row = ProyectoService.obtener(pid)
        if not row:
            return False
        nombre = nombre if nombre is not None else row["nombre"]
        descripcion = descripcion if descripcion is not None else row.get("descripcion")
        fecha_inicio = fecha_inicio if fecha_inicio is not None else row.get("fecha_inicio")
        execute("UPDATE proyectos SET nombre=%s, descripcion=%s, fecha_inicio=%s WHERE id=%s",
                (nombre, descripcion, fecha_inicio, pid))
        return True

    @staticmethod
    def eliminar(pid: int) -> bool:
        execute("DELETE FROM proyectos WHERE id=%s", (pid,))
        return True
