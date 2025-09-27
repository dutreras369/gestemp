from __future__ import annotations
from typing import Optional
from app.models.registro_tiempo import RegistroTiempo
from .helpers import execute, fetchall, fetchone

class TiempoService:
    @staticmethod
    def crear(reg: RegistroTiempo) -> int:
        reg.validate()
        sql = ("""INSERT INTO registros_tiempo
                (empleado_id, proyecto_id, fecha, horas, descripcion)
                VALUES (%s,%s,%s,%s,%s)""")
        rid = execute(sql, (reg.empleado_id, reg.proyecto_id, reg.fecha, reg.horas, reg.to_dict().get("descripcion")))
        reg.id = rid
        return rid

    @staticmethod
    def listar(desde: str | None = None, hasta: str | None = None, empleado_id: int | None = None, proyecto_id: int | None = None) -> list[dict]:
        q = """SELECT t.id, t.fecha, t.horas, t.descripcion,
                          e.id AS empleado_id, e.nombre AS empleado,
                          p.id AS proyecto_id, p.nombre AS proyecto
                   FROM registros_tiempo t
                   INNER JOIN empleados e ON e.id = t.empleado_id
                   INNER JOIN proyectos p ON p.id = t.proyecto_id
                 """
        params = []
        cond = []
        if desde:
            cond.append("t.fecha >= %s"); params.append(desde)
        if hasta:
            cond.append("t.fecha <= %s"); params.append(hasta)
        if empleado_id:
            cond.append("t.empleado_id = %s"); params.append(empleado_id)
        if proyecto_id:
            cond.append("t.proyecto_id = %s"); params.append(proyecto_id)
        if cond:
            q += " WHERE " + " AND ".join(cond)
        q += " ORDER BY t.fecha DESC, t.id DESC"
        return fetchall(q, params)

    @staticmethod
    def eliminar(reg_id: int) -> bool:
        execute("DELETE FROM registros_tiempo WHERE id=%s", (reg_id,))
        return True
