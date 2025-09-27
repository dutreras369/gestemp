from __future__ import annotations
import os
import datetime as dt
from typing import List, Dict
import requests
from .helpers import execute, fetchall

TIPOS_VALIDOS = {"UF","IVP","IPC","UTM","DOLAR","EURO"}

def _normaliza_tipo(tipo: str) -> str:
    t = (tipo or "").strip().upper()
    if t in {"DÓLAR","USD"}: t = "DOLAR"
    if t not in TIPOS_VALIDOS:
        raise ValueError(f"Tipo de indicador no soportado: {t}. Válidos: {', '.join(sorted(TIPOS_VALIDOS))}")
    return t

def _parse_iso_date(date_str: str) -> dt.date:
    # '2025-09-26T03:00:00.000Z' -> date(2025,9,26)
    return dt.date.fromisoformat(str(date_str)[:10])

def _to_str_date(d: dt.date) -> str:
    return d.strftime("%Y-%m-%d")

def _fmt_ddmmyyyy(d: dt.date) -> str:
    return d.strftime("%d-%m-%Y")

def _parse_serie(tipo: str, data: dict) -> List[Dict]:
    out: List[Dict] = []
    if isinstance(data, dict) and "serie" in data and isinstance(data["serie"], list):
        for item in data["serie"]:
            fecha_raw = item.get("fecha") or item.get("date") or item.get("Fecha")
            valor = item.get("valor") or item.get("value") or item.get("Valor")
            if not fecha_raw or valor is None:
                continue
            fecha = _parse_iso_date(str(fecha_raw))
            out.append({"nombre": tipo, "fecha_valor": _to_str_date(fecha), "valor": float(valor)})
    elif isinstance(data, dict):
        # raíz de mindicador (todos) -> campos uf, ivp, dolar, euro...
        for key in ("uf","ivp","dolar","euro","ipc","utm"):
            if key in data and isinstance(data[key], dict) and "valor" in data[key] and "fecha" in data[key]:
                fecha = _parse_iso_date(data[key]["fecha"])
                out.append({"nombre": key.upper() if key != "dolar" else "DOLAR",
                            "fecha_valor": _to_str_date(fecha),
                            "valor": float(data[key]["valor"])})
    return out

def _years_range(desde: dt.date, hasta: dt.date):
    y = desde.year
    while y <= hasta.year:
        yield y
        y += 1

class IndicadoresService:
    @staticmethod
    def _provider_base() -> str:
        base = os.getenv("INDICADORES_API_URL", "").rstrip("/")
        if not base:
            raise RuntimeError("Configurar INDICADORES_API_URL en .env (p.ej. https://mindicador.cl/api)")
        return base

    @staticmethod
    def fetch(tipo: str, fecha: str | None = None, desde: str | None = None, hasta: str | None = None) -> List[Dict]:
        tipo = _normaliza_tipo(tipo)
        base = IndicadoresService._provider_base()
        headers = {}
        api_key = os.getenv("INDICADORES_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Detección proveedor mindicador (patrones específicos)
        is_mindicador = "mindicador.cl" in base

        serie: List[Dict] = []

        if is_mindicador:
            # 1) Fecha puntual -> /{tipo}/{dd-mm-yyyy}
            if fecha:
                # aceptar YYYY-MM-DD o DD-MM-YYYY
                if re := __import__("re"):
                    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", fecha)
                if m:
                    d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                else:
                    # DD-MM-YYYY
                    d, mth, y = fecha.split("-")
                    d = dt.date(int(y), int(mth), int(d))
                url = f"{base}/{tipo.lower()}/{_fmt_ddmmyyyy(d)}"
                resp = requests.get(url, headers=headers, timeout=15)
                resp.raise_for_status()
                return _parse_serie(tipo, resp.json())

            # 2) Rango -> obtener por años /{tipo}/{yyyy} y filtrar
            if desde and hasta:
                def parse_any(s: str) -> dt.date:
                    if "-" not in s:
                        raise ValueError("Fecha inválida")
                    p = s.split("-")
                    if len(p[0]) == 4:  # YYYY-MM-DD
                        return dt.date(int(p[0]), int(p[1]), int(p[2]))
                    return dt.date(int(p[2]), int(p[1]), int(p[0]))  # DD-MM-YYYY
                d1 = parse_any(desde)
                d2 = parse_any(hasta)
                if d1 > d2:
                    d1, d2 = d2, d1
                all_items: List[Dict] = []
                for year in _years_range(d1, d2):
                    url = f"{base}/{tipo.lower()}/{year}"
                    resp = requests.get(url, headers=headers, timeout=15)
                    if resp.status_code == 404:
                        continue
                    resp.raise_for_status()
                    items = _parse_serie(tipo, resp.json())
                    all_items.extend(items)
                # filtrar por rango
                lo = _to_str_date(d1); hi = _to_str_date(d2)
                serie = [it for it in all_items if lo <= it["fecha_valor"] <= hi]
                # ordenar desc por fecha
                serie.sort(key=lambda x: x["fecha_valor"], reverse=True)
                return serie

            # 3) Sin fechas -> último mes /{tipo}
            url = f"{base}/{tipo.lower()}"
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return _parse_serie(tipo, resp.json())

        # Proveedor genérico (fallback de nuestro diseño inicial)
        if fecha:
            # se intentará /{tipo}/{YYYY-MM-DD}
            url = f"{base}/{tipo.lower()}/{fecha}"
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return _parse_serie(tipo, resp.json())
        if desde and hasta:
            url = f"{base}/{tipo.lower()}/{desde}/{hasta}"
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return _parse_serie(tipo, resp.json())
        # último valor
        url = f"{base}/{tipo.lower()}"
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return _parse_serie(tipo, resp.json())

    @staticmethod
    def save_values(valores: List[Dict], usuario: str, proveedor: str) -> int:
        if not valores:
            return 0
        total = 0
        for v in valores:
            # UPSERT manual
            execute(
                """INSERT IGNORE INTO indicadores_valores (nombre, fecha_valor, valor, proveedor)
                     VALUES (%s,%s,%s,%s)""",
                (v['nombre'], v['fecha_valor'], v['valor'], proveedor)
            )
            execute(
                "UPDATE indicadores_valores SET valor=%s, proveedor=%s WHERE nombre=%s AND fecha_valor=%s",
                (v['valor'], proveedor, v['nombre'], v['fecha_valor'])
            )
            total += 1
        return total

    @staticmethod
    def log_consulta(nombre: str, usuario: str, proveedor: str,
                     fecha_valor: str | None = None, desde: str | None = None, hasta: str | None = None) -> int:
        return execute(
            """INSERT INTO indicadores_consultas (nombre, fecha_valor, desde, hasta, consultado_por, proveedor)
                 VALUES (%s,%s,%s,%s,%s,%s)""",
            (nombre.upper(), fecha_valor, desde, hasta, usuario, proveedor)
        )

    @staticmethod
    def list_db(nombre: str | None = None, desde: str | None = None, hasta: str | None = None):
        q = "SELECT id, nombre, fecha_valor, valor, proveedor FROM indicadores_valores"
        params = []
        cond = []
        if nombre:
            cond.append("nombre = %s"); params.append(nombre.upper())
        if desde:
            cond.append("fecha_valor >= %s"); params.append(desde)
        if hasta:
            cond.append("fecha_valor <= %s"); params.append(hasta)
        if cond:
            q += " WHERE " + " AND ".join(cond)
        q += " ORDER BY fecha_valor DESC, nombre ASC"
        return fetchall(q, params)
