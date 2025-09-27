import pytest
from app.services.indicadores_service import _normaliza_tipo, _parse_serie

def test_normaliza_tipo_ok():
    assert _normaliza_tipo("uf") == "UF"
    assert _normaliza_tipo("DÓLAR") == "DOLAR"

def test_parse_serie_mindicador():
    fake = {"serie": [{"fecha": "2025-09-26T03:00:00.000Z", "valor": 1000}]}
    out = _parse_serie("UF", fake)
    assert out[0]["valor"] == 1000
