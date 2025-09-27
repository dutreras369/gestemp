from __future__ import annotations
from typing import Optional
from app.models.departamento import Departamento
from .helpers import execute, fetchall, fetchone

class DepartamentoService:
    @staticmethod
    def crear(dep: Departamento) -> int:
        dep.validate()
        sql = "INSERT INTO departamentos (nombre, gerente) VALUES (%s, %s)"
        dep_id = execute(sql, (dep.nombre, dep.gerente))
        dep.id = dep_id
        return dep_id

    @staticmethod
    def listar() -> list[dict]:
        return fetchall("SELECT id, nombre, gerente, creado_en FROM departamentos ORDER BY id DESC")

    @staticmethod
    def obtener(dep_id: int) -> Optional[dict]:
        return fetchone("SELECT id, nombre, gerente, creado_en FROM departamentos WHERE id=%s", (dep_id,))

    @staticmethod
    def actualizar(dep_id: int, nombre: Optional[str] = None, gerente: Optional[str] = None) -> bool:
        row = DepartamentoService.obtener(dep_id)
        if not row:
            return False
        new_nombre = nombre if nombre is not None else row["nombre"]
        new_gerente = gerente if gerente is not None else row["gerente"]
        sql = "UPDATE departamentos SET nombre=%s, gerente=%s WHERE id=%s"
        execute(sql, (new_nombre, new_gerente, dep_id))
        return True

    @staticmethod
    def eliminar(dep_id: int) -> bool:
        # ON DELETE RESTRICT no aplica; empleados quedan con depto_id NULL
        execute("DELETE FROM departamentos WHERE id=%s", (dep_id,))
        return True
