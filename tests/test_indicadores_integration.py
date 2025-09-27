from app.services.indicadores_service import IndicadoresService

def test_fetch_and_save(monkeypatch):
    # Mock respuesta de requests
    def fake_get(url, **kwargs):
        class R:
            def raise_for_status(self): pass
            def json(self):
                return {"serie":[{"fecha":"2025-09-01T00:00:00.000Z","valor":999.9}]}
        return R()
    monkeypatch.setattr("requests.get", fake_get)

    serie = IndicadoresService.fetch("UF", fecha="2025-09-01")
    assert serie[0]["valor"] == 999.9
