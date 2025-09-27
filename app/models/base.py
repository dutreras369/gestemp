from __future__ import annotations

class BaseModel:
    """Clase base simple para modelos POO (primer año).
    Provee interfaz común para polimorfismo.
    """
    def to_dict(self) -> dict:
        """Representación serializable básica (polimorfismo)."""
        return {}

    def validate(self) -> None:
        """Validaciones por entidad (polimorfismo).
        Debe ser sobreescrita en las subclases.
        """
        pass
