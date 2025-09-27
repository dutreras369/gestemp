import pytest
from app.models.empleado import Empleado

def test_empleado_valido():
    emp = Empleado("Luis", "luis@test.cl", depto_id=1, salario=500000)
    emp.validate()
    assert emp.to_dict()["nombre"] == "Luis"

def test_empleado_email_invalido():
    with pytest.raises(ValueError):
        Empleado("Ana", "correo-invalido").validate()
