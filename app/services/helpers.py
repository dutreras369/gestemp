from __future__ import annotations
from typing import Any, Iterable
from app.db.mysql_conn import Db

def execute(query: str, params: Iterable[Any] | None = None) -> int:
    """Ejecuta INSERT/UPDATE/DELETE. Retorna lastrowid cuando exista, si no 0."""
    cn = Db.get_connection()
    try:
        cur = cn.cursor()
        cur.execute(query, params or ())
        cn.commit()
        last_id = getattr(cur, "lastrowid", 0) or 0
        cur.close()
        return int(last_id)
    finally:
        cn.close()

def fetchall(query: str, params: Iterable[Any] | None = None) -> list[dict]:
    cn = Db.get_connection()
    try:
        cur = cn.cursor(dictionary=True)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        cn.close()

def fetchone(query: str, params: Iterable[Any] | None = None) -> dict | None:
    cn = Db.get_connection()
    try:
        cur = cn.cursor(dictionary=True)
        cur.execute(query, params or ())
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        cn.close()
