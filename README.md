# Sistema de Gestión de Empleados (POO + MySQL + CLI)

Este proyecto implementa un sistema académico para gestionar empleados, departamentos, proyectos y tiempos de trabajo. 
Está desarrollado en **Python** con **POO de primer año**, conexión a **MySQL/MariaDB** y una **CLI** con roles (admin, gerente, usuario).

---

## 🚀 Instalación

### 1) Crear y activar entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3) Variables de entorno
Copia `config/.env.example` a `.env` en la raíz y completa con tus credenciales:
```
MYSQL_HOST=localhost
MYSQL_DB=sgempleados
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
```

> Asegúrate de que MySQL/MariaDB tenga un usuario con permisos sobre la base de datos `sgempleados`.

### 4) Probar conexión
```bash
python main.py ping-db
```
Si ves `✅ Conexión OK a MySQL`, el entorno está listo para avanzar al **Paso 1 (Base de Datos)**.

---

## 📖 Explicación

El sistema fue diseñado con conceptos básicos de **Programación Orientada a Objetos (POO)**:

- **Objetos**: `Empleado`, `Departamento`, `Proyecto`, `RegistroTiempo`, `Usuario`.
- **Encapsulamiento**: atributos privados con `__atributo` y acceso mediante `@property`.
- **Herencia y Polimorfismo**: todas las entidades extienden `BaseModel` y sobreescriben `validate()` y `to_dict()`.
- **Relaciones de negocio**:
  - Un **Departamento** contiene muchos **Empleados**.
  - Un **Empleado** puede participar en varios **Proyectos** (relación N:M).
  - Un **Registro de Tiempo** une a un Empleado con un Proyecto.
  - Un **Usuario** controla autenticación y permisos (roles).

Además, la **CLI** permite operar el sistema con comandos organizados por rol:
- **Admin**: acceso total (usuarios, departamentos, proyectos, reportes).
- **Gerente**: gestiona empleados, proyectos y reportes.
- **Usuario**: puede registrar y listar sus tiempos de trabajo.

---

## 📊 Diagramas

Para visualizar la estructura completa, consulta el archivo:

📂 [docs/uml.md](docs/uml.md)

El diagrama UML muestra las clases principales, relaciones entre entidades y notas de diseño para la defensa académica.
