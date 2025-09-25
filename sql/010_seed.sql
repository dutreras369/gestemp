-- ======================
-- 010_seed.sql
-- Datos básicos de arranque (MariaDB)
-- Idempotente: no falla si ya existen registros
-- ======================

USE sgempleados;

-- Ajuste de juego de caracteres por si el cliente no lo envía
SET NAMES utf8mb4;

-- Departamentos iniciales
INSERT IGNORE INTO departamentos (id, nombre, gerente) VALUES
  (1, 'Recursos Humanos', 'María Soto'),
  (2, 'I+D',               'Ana Pérez'),
  (3, 'Ventas',            'Luis Gómez');

-- Proyectos iniciales
INSERT IGNORE INTO proyectos (id, nombre, descripcion, fecha_inicio) VALUES
  (1, 'EcoGrid',    'Optimización de redes de energía', CURDATE()),
  (2, 'GreenTrack', 'Trazabilidad de residuos',         CURDATE());

-- Usuario admin inicial (password: admin123)
-- Hash bcrypt provisto (string, compatible con VARCHAR(100))
INSERT IGNORE INTO usuarios (id, username, password_hash, rol) VALUES
  (1, 'admin', '$2b$12$7ULtqD809irGcc6o2zvleOXqotHJ9ou86n32hR831t/pi0OexxGxu', 'admin');
