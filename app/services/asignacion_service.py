from __future__ import annotations
from .helpers import execute, fetchall

class AsignacionService:
    @staticmethod
    def asignar_departamento(empleado_id: int, depto_id: int | None) -> bool:
        execute("UPDATE empleados SET depto_id=%s WHERE id=%s", (depto_id, empleado_id))
        return True

    @staticmethod
    def asignar_proyecto(empleado_id: int, proyecto_id: int) -> bool:
        # Evitar duplicados con INSERT IGNORE si hay UNIQUE(empleado_id, proyecto_id)
        execute("INSERT IGNORE INTO empleado_proyecto (empleado_id, proyecto_id) VALUES (%s,%s)", (empleado_id, proyecto_id))
        return True

    @staticmethod
    def quitar_proyecto(empleado_id: int, proyecto_id: int) -> bool:
        execute("DELETE FROM empleado_proyecto WHERE empleado_id=%s AND proyecto_id=%s", (empleado_id, proyecto_id))
        return True

    @staticmethod
    def listar_proyectos_de_empleado(empleado_id: int) -> list[dict]:
        q = """SELECT ep.proyecto_id, p.nombre
                 FROM empleado_proyecto ep
                 INNER JOIN proyectos p ON p.id = ep.proyecto_id
                 WHERE ep.empleado_id=%s
                 ORDER BY p.id DESC"""
        return fetchall(q, (empleado_id,))
