# CHECKLIST DE ACEPTACIÓN — SG Empleados

Marcar cada punto cuando se verifique en laboratorio.

## A. Entorno y conexión
- [ ] venv + dependencias instaladas
- [ ] `.env` configurado (DB + INDICADORES_API_URL)
- [ ] `python main.py ping-db` devuelve ✅

## B. Seguridad
- [ ] Login admin (hash bcrypt) y `whoami`
- [ ] Acceso por rol: admin/gerente/usuario (intentar acción no permitida y ver error)

## C. CRUD Core
- [ ] Crear/Listar/Actualizar/Eliminar Departamento
- [ ] Crear/Listar/Actualizar/Eliminar Empleado
- [ ] Crear/Listar/Actualizar/Eliminar Proyecto
- [ ] Asignar empleado a proyecto y listar proyectos del empleado

## D. Registro de tiempo
- [ ] Crear registro de tiempo (0–24h)
- [ ] Listar por rango de fechas

## E. Indicadores (Etapa 2)
- [ ] `fetch` por fecha y por periodo
- [ ] `save` con rol admin/gerente
- [ ] `list` muestra lo guardado
- [ ] Bitácora de consulta almacenada (indicadores_consultas)

## F. Validaciones y errores
- [ ] Email inválido rechazado
- [ ] Horas fuera de [0,24] rechazadas
- [ ] Tipo de indicador inválido muestra lista de válidos

## G. Documentación
- [ ] README + UML + anexos Etapa 2 presentes
