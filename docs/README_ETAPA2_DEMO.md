# Guía de Demo — Etapa 2 (Indicadores Económicos)

## Configuración
En `.env`:
```
INDICADORES_API_URL=https://mindicador.cl/api
# INDICADORES_API_KEY=   # no requerido para mindicador.cl
```

## Comandos clave
```bash
# Consultar último mes:
python main.py indicadores fetch --tipo UF

# Consultar por fecha específica (dos formatos válidos):
python main.py indicadores fetch --tipo DOLAR --fecha 2025-09-26
python main.py indicadores fetch --tipo DOLAR --fecha 26-09-2025

# Consultar por periodo (el servicio obtiene por año y filtra):
python main.py indicadores fetch --tipo UF --desde 2025-09-01 --hasta 2025-09-10

# Guardar valores consultados (admin/gerente) y registrar consulta:
python main.py indicadores save --tipo UF --desde 2025-09-01 --hasta 2025-09-10

# Listar lo guardado:
python main.py indicadores list --tipo UF --desde 2025-09-01 --hasta 2025-09-30
```

## Errores comunes
- `Tipo de indicador no soportado` → válidos: UF, IVP, IPC, UTM, DOLAR, EURO.
- `Configurar INDICADORES_API_URL...` → falta variable en `.env`.
- `Timeout` o `HTTPError` → proveedor caído; reintentar o cambiar de red.
