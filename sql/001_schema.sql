-- =========================================
-- 001_schema.sql (compatible MariaDB/XAMPP)
-- =========================================

-- Crea la BD con collation compatible
CREATE DATABASE IF NOT EXISTS sgempleados
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE sgempleados;

SET FOREIGN_KEY_CHECKS = 0;

-- ======================
-- TABLA: departamentos
-- ======================
DROP TABLE IF EXISTS departamentos;
CREATE TABLE departamentos (
  id        INT AUTO_INCREMENT PRIMARY KEY,
  nombre    VARCHAR(100) NOT NULL UNIQUE,
  gerente   VARCHAR(100) NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ===============
-- TABLA: empleados
-- ===============
DROP TABLE IF EXISTS empleados;
CREATE TABLE empleados (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  direccion     VARCHAR(200) NULL,
  telefono      VARCHAR(30)  NULL,
  email         VARCHAR(120) NOT NULL UNIQUE,
  fecha_inicio  DATE         NULL,
  salario       DECIMAL(12,2) DEFAULT 0.00,
  depto_id      INT NULL,
  creado_en     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_emp_depto
    FOREIGN KEY (depto_id) REFERENCES departamentos(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_empleados_depto ON empleados(depto_id);

-- ===============
-- TABLA: proyectos
-- ===============
DROP TABLE IF EXISTS proyectos;
CREATE TABLE proyectos (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(120) NOT NULL UNIQUE,
  descripcion  TEXT NULL,
  fecha_inicio DATE NULL,
  creado_en    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =======================================
-- TABLA puente: empleado_proyecto (N:M)
-- =======================================
DROP TABLE IF EXISTS empleado_proyecto;
CREATE TABLE empleado_proyecto (
  empleado_id INT NOT NULL,
  proyecto_id INT NOT NULL,
  asignado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (empleado_id, proyecto_id),
  CONSTRAINT fk_ep_emp FOREIGN KEY (empleado_id)
    REFERENCES empleados(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_ep_pro FOREIGN KEY (proyecto_id)
    REFERENCES proyectos(id)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ==========================
-- TABLA: registros_tiempo
-- ==========================
DROP TABLE IF EXISTS registros_tiempo;
CREATE TABLE registros_tiempo (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  empleado_id INT NOT NULL,
  proyecto_id INT NOT NULL,
  fecha       DATE NOT NULL,
  horas       DECIMAL(5,2) NOT NULL,
  descripcion VARCHAR(255) NULL,
  creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_rt_emp FOREIGN KEY (empleado_id)
    REFERENCES empleados(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_rt_pro FOREIGN KEY (proyecto_id)
    REFERENCES proyectos(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_rt_emp ON registros_tiempo(empleado_id);
CREATE INDEX idx_rt_pro ON registros_tiempo(proyecto_id);
CREATE INDEX idx_rt_fecha ON registros_tiempo(fecha);

-- Nota: En MariaDB antiguas, CHECK puede ignorarse. Validaremos horas en la app.

-- ===============
-- TABLA: usuarios
-- ===============
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  username      VARCHAR(60) NOT NULL UNIQUE,
  -- para simplificar en primer año, guardamos el bcrypt como texto
  password_hash VARCHAR(100) NOT NULL,
  rol           ENUM('admin','gerente','usuario') NOT NULL DEFAULT 'usuario',
  creado_en     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;


-- ===============
-- TABLA: indicadores_valores
-- ===============
CREATE TABLE IF NOT EXISTS indicadores_valores (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(20) NOT NULL,
  fecha_valor  DATE NOT NULL,
  valor        DECIMAL(16,6) NOT NULL,
  proveedor    VARCHAR(100) NOT NULL,
  UNIQUE KEY uq_indicador_fecha (nombre, fecha_valor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ===============
-- TABLA: indicadores_consultas
-- ===============
CREATE TABLE IF NOT EXISTS indicadores_consultas (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  nombre         VARCHAR(20) NOT NULL,
  fecha_valor    DATE NULL,
  desde          DATE NULL,
  hasta          DATE NULL,
  consultado_por VARCHAR(60) NOT NULL,
  consultado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  proveedor      VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;