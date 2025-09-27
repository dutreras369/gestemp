import pytest
from app.models.departamento import Departamento
from app.services.departamento_service import DepartamentoService

def test_crud_departamento(tmp_path):
    dep = Departamento("Pruebas", "Gerente Test")
    dep_id = DepartamentoService.crear(dep)
    row = DepartamentoService.obtener(dep_id)
    assert row["nombre"] == "Pruebas"

    ok = DepartamentoService.actualizar(dep_id, nombre="Nuevo Nombre")
    assert ok
    row2 = DepartamentoService.obtener(dep_id)
    assert row2["nombre"] == "Nuevo Nombre"

    DepartamentoService.eliminar(dep_id)
    assert DepartamentoService.obtener(dep_id) is None
