# UML del Sistema (POO + MySQL + CLI)

```mermaid
classDiagram
    direction LR

    class BaseModel {
        <<abstract>>
        +to_dict() dict
        +validate() void
    }

    class Empleado {
        -id: int
        -nombre: str
        -direccion: str
        -telefono: str
        -email: str
        -fecha_inicio: date
        -salario: decimal
        -depto_id: int
        +getters/setters
        +to_dict() dict
        +validate() void
    }

    class Departamento {
        -id: int
        -nombre: str
        -gerente: str
        +getters/setters
        +to_dict() dict
        +validate() void
    }

    class Proyecto {
        -id: int
        -nombre: str
        -descripcion: str
        -fecha_inicio: date
        +getters/setters
        +to_dict() dict
        +validate() void
    }

    class RegistroTiempo {
        -id: int
        -empleado_id: int
        -proyecto_id: int
        -fecha: date
        -horas: decimal
        -descripcion: str
        +getters/setters
        +to_dict() dict
        +validate() void
    }

    class Usuario {
        -id: int
        -username: str
        -password_hash: str
        -rol: enum
        +checkPassword(pwd): bool
        +to_dict() dict
        +validate() void
    }

    class EmpleadoProyecto {
        <<tabla puente>>
        -empleado_id: int
        -proyecto_id: int
    }

    %% Herencia (polimorfismo por to_dict/validate)
    BaseModel <|-- Empleado
    BaseModel <|-- Departamento
    BaseModel <|-- Proyecto
    BaseModel <|-- RegistroTiempo
    BaseModel <|-- Usuario

    %% Relaciones
    Departamento "1" o-- "0..*" Empleado : pertenece
    Empleado "0..*" o-- "0..*" Proyecto : participa\n(EmpleadoProyecto)
    EmpleadoProyecto .. Proyecto
    EmpleadoProyecto .. Empleado

    %% Asociación de RegistroTiempo como bitácora entre Empleado y Proyecto
    Empleado "1" -- "0..*" RegistroTiempo : registra
    Proyecto "1" -- "0..*" RegistroTiempo : recibe
```

## Notas de diseño (para explicar en la defensa)

- **Herencia y polimorfismo**: todas las entidades extienden `BaseModel` y sobreescriben `validate()` y `to_dict()`.
- **Encapsulamiento**: atributos privados con `__atributo` y acceso mediante `@property`.
- **Relaciones**:
  - `Departamento 1 — * Empleado` (empleado tiene `depto_id`).
  - `Empleado * — * Proyecto` vía tabla puente `EmpleadoProyecto`.
  - `RegistroTiempo` es una asociación entre `Empleado` y `Proyecto` con atributos propios (`fecha`, `horas`, `descripcion`).
- **Usuario** no se relaciona directamente con el modelo de negocio; controla **autenticación y rol** para la **CLI**.
