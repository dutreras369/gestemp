from __future__ import annotations
from typing import Optional
from app.models.empleado import Empleado
from .helpers import execute, fetchall, fetchone

class EmpleadoService:
    @staticmethod
    def crear(emp: "Empleado") -> int:
        emp.validate()

        # MySQL/Postgres -> %s ; SQLite -> ?
        sql = ("""INSERT INTO empleados
                  (nombre, direccion, telefono, email, fecha_inicio, salario, depto_id)
                  VALUES (%s,%s,%s,%s,%s,%s,%s)""")

        params = (
            emp.nombre,
            emp.direccion,
            emp.telefono,
            emp.email,
            emp.fecha_inicio,  # 'YYYY-MM-DD' o None
            emp.salario,
            emp.depto_id
        )

        # Debug opcional para verificar cantidad y orden
        # print(">>> SQL params:", params)

        emp_id = execute(sql, params)
        emp.id = emp_id
        return emp_id

    @staticmethod
    def listar() -> list[dict]:
        return fetchall("""
            SELECT e.id, e.nombre, e.email, e.salario, e.depto_id, d.nombre AS depto_nombre
            FROM empleados e
            LEFT JOIN departamentos d ON d.id = e.depto_id
            ORDER BY e.id DESC
        """)

    @staticmethod
    def obtener(emp_id: int) -> Optional[dict]:
        return fetchone("""
            SELECT e.id, e.nombre, e.direccion, e.telefono, e.email, e.fecha_inicio,
                   e.salario, e.depto_id, d.nombre AS depto_nombre
            FROM empleados e
            LEFT JOIN departamentos d ON d.id = e.depto_id
            WHERE e.id=%s
        """, (emp_id,))

    @staticmethod
    def actualizar(emp_id: int, **kwargs) -> bool:
        row = EmpleadoService.obtener(emp_id)
        if not row:
            return False
        # Preparar valores nuevos (fallback a los existentes)
        nombre = kwargs.get("nombre", row["nombre"])
        direccion = kwargs.get("direccion", row.get("direccion"))
        telefono = kwargs.get("telefono", row.get("telefono"))
        email = kwargs.get("email", row["email"])
        fecha_inicio = kwargs.get("fecha_inicio", row.get("fecha_inicio"))
        salario = kwargs.get("salario", row["salario"]
        )
        depto_id = kwargs.get("depto_id", row.get("depto_id"))

        sql = ("""UPDATE empleados
                 SET nombre=%s, direccion=%s, telefono=%s, email=%s,
                     fecha_inicio=%s, salario=%s, depto_id=%s
               WHERE id=%s""")
        execute(sql, (nombre, direccion, telefono, email, fecha_inicio, salario, depto_id, emp_id))
        return True

    @staticmethod
    def eliminar(emp_id: int) -> bool:
        execute("DELETE FROM empleados WHERE id=%s", (emp_id,))
        return True
