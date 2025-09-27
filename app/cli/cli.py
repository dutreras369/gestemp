import click
from security.auth import Auth
import os

# --- Helpers de salida ---
def ok(msg): click.echo(f"✅ {msg}")
def err(msg): click.echo(f"❌ {msg}")

@click.group()
def cli():
    '''CLI del Sistema de Gestión de Empleados'''
    pass

# ---------------- AUTH ----------------
@cli.group()
def auth():
    '''Comandos de autenticación y usuarios.'''
    pass

@auth.command("login")
@click.option("--username", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def login(username, password):
    if Auth.login(username, password):
        ok(f"Login correcto como {username}")
    else:
        err("Credenciales inválidas")

@auth.command("logout")
def logout():
    Auth.logout()
    ok("Sesión cerrada")

@auth.command("whoami")
def whoami():
    user = Auth.load_session()
    if not user:
        err("No has iniciado sesión")
    else:
        ok(f"Usuario: {user['username']}  Rol: {user['rol']}")

@auth.command("create-user")
@click.option("--username", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--rol", type=click.Choice(["admin","gerente","usuario"]), default="usuario")
def create_user(username, password, rol):
    # Solo admin puede crear usuarios
    user = Auth.load_session()
    if not user or user.get("rol") != "admin":
        err("Acceso denegado (se requiere rol admin)")
        return
    from app.services.usuario_service import UsuarioService
    hashed = Auth.hash_password(password)
    try:
        uid = UsuarioService.crear(username, hashed, rol)
        ok(f"Usuario creado con id={uid}")
    except Exception as e:
        err(f"No se pudo crear: {e}")

# ---------------- DEPARTAMENTO ----------------
@cli.group()
def departamento():
    '''Gestión de Departamentos.'''
    pass

@departamento.command("add")
@click.option("--nombre", prompt=True)
@click.option("--gerente", default=None)
def dep_add(nombre, gerente):
    try:
        from app.models.departamento import Departamento
        from app.services.departamento_service import DepartamentoService
        # admin/gerente
        user = Auth.load_session()
        if not user or user.get("rol") not in ["admin","gerente"]:
            err("Acceso denegado"); return
        dep = Departamento(nombre, gerente)
        dep_id = DepartamentoService.crear(dep)
        ok(f"Departamento id={dep_id} creado")
    except Exception as e:
        err(str(e))

@departamento.command("list")
def dep_list():
    from app.services.departamento_service import DepartamentoService
    rows = DepartamentoService.listar()
    for r in rows:
        click.echo(f"{r['id']} | {r['nombre']} | gerente={r.get('gerente')}")

@departamento.command("update")
@click.option("--id", "dep_id", type=int, prompt=True)
@click.option("--nombre", default=None)
@click.option("--gerente", default=None)
def dep_update(dep_id, nombre, gerente):
    from app.services.departamento_service import DepartamentoService
    ok("Actualizado") if DepartamentoService.actualizar(dep_id, nombre, gerente) else err("No existe")

@departamento.command("delete")
@click.option("--id", "dep_id", type=int, prompt=True)
def dep_delete(dep_id):
    from app.services.departamento_service import DepartamentoService
    try:
        DepartamentoService.eliminar(dep_id)
        ok("Eliminado")
    except Exception as e:
        err(str(e))

# ---------------- EMPLEADO ----------------
@cli.group()
def empleado():
    '''Gestión de Empleados.'''
    pass

# python main.py empleado add --nombre 'Javier' --email 'javi@eco.cl' --depto_id 11 --salario 800000 --direccion 'calle 1, santiago' --telefono '5697777777' --fecha_inicio '2023-10-01'

@empleado.command("add")
@click.option("--nombre", prompt=True, help="Nombre completo")
@click.option("--email", prompt=True, help="Correo del empleado")
@click.option("--depto_id", type=int, default=None, help="ID del departamento")
@click.option("--salario", type=float, default=0.0, help="Salario bruto")
@click.option("--direccion", default=None, help="Dirección")
@click.option("--telefono", default=None, help="Teléfono")
@click.option("--fecha_inicio", default=None, help="Fecha de inicio YYYY-MM-DD")
def emp_add(nombre, email, depto_id, salario, direccion, telefono, fecha_inicio):
    from app.models.empleado import Empleado
    from app.services.empleado_service import EmpleadoService
    user = Auth.load_session()
    if not user or user.get("rol") not in ["admin","gerente"]:
        err("Acceso denegado"); return

    # Normaliza strings vacíos a None
    fecha_inicio = fecha_inicio or None
    direccion = direccion or None
    telefono = telefono or None

    emp = Empleado(nombre, email, depto_id, direccion, telefono, fecha_inicio, salario)
    try:
        emp_id = EmpleadoService.crear(emp)
        ok(f"Empleado id={emp_id} creado")
    except Exception as e:
        err(str(e))

@empleado.command("list")
def emp_list():
    from app.services.empleado_service import EmpleadoService
    rows = EmpleadoService.listar()
    for r in rows:
        click.echo(f"{r['id']} | {r['nombre']} | {r['email']} | depto={r.get('depto_nombre')}")

@empleado.command("update")
@click.option("--id", "emp_id", type=int, prompt=True)
@click.option("--nombre", default=None)
@click.option("--email", default=None)
@click.option("--depto_id", type=int, default=None)
@click.option("--salario", type=float, default=None)
@click.option("--direccion", default=None)
@click.option("--telefono", default=None)
@click.option("--fecha_inicio", default=None)
def emp_update(emp_id, **kwargs):
    from app.services.empleado_service import EmpleadoService
    ok("Actualizado") if EmpleadoService.actualizar(emp_id, **kwargs) else err("No existe")

@empleado.command("delete")
@click.option("--id", "emp_id", type=int, prompt=True)
def emp_delete(emp_id):
    from app.services.empleado_service import EmpleadoService
    try:
        EmpleadoService.eliminar(emp_id)
        ok("Eliminado")
    except Exception as e:
        err(str(e))

# ---------------- PROYECTO ----------------
@cli.group()
def proyecto():
    '''Gestión de Proyectos.'''
    pass

@proyecto.command("add")
@click.option("--nombre", prompt=True)
@click.option("--descripcion", default=None)
@click.option("--fecha_inicio", default=None)
def pro_add(nombre, descripcion, fecha_inicio):
    from app.models.proyecto import Proyecto
    from app.services.proyecto_service import ProyectoService
    user = Auth.load_session()
    if not user or user.get("rol") not in ["admin","gerente"]:
        err("Acceso denegado"); return
    p = Proyecto(nombre, descripcion, fecha_inicio)
    try:
        pid = ProyectoService.crear(p)
        ok(f"Proyecto id={pid} creado")
    except Exception as e:
        err(str(e))

@proyecto.command("list")
def pro_list():
    from app.services.proyecto_service import ProyectoService
    rows = ProyectoService.listar()
    for r in rows:
        click.echo(f"{r['id']} | {r['nombre']} | {r.get('descripcion')} | {r.get('fecha_inicio')}")

@proyecto.command("update")
@click.option("--id", "pid", type=int, prompt=True)
@click.option("--nombre", default=None)
@click.option("--descripcion", default=None)
@click.option("--fecha_inicio", default=None)
def pro_update(pid, nombre, descripcion, fecha_inicio):
    from app.services.proyecto_service import ProyectoService
    ok("Actualizado") if ProyectoService.actualizar(pid, nombre, descripcion, fecha_inicio) else err("No existe")

@proyecto.command("delete")
@click.option("--id", "pid", type=int, prompt=True)
def pro_delete(pid):
    from app.services.proyecto_service import ProyectoService
    try:
        ProyectoService.eliminar(pid)
        ok("Eliminado")
    except Exception as e:
        err(str(e))

# ---------------- ASIGNAR ----------------
@cli.group()
def asignar():
    '''Asignaciones de empleados.'''
    pass

@asignar.command("depto")
@click.option("--empleado_id", type=int, prompt=True)
@click.option("--depto_id", type=int, default=None, help="Puede ser NULL para quitar asignación")
def asg_depto(empleado_id, depto_id):
    from app.services.asignacion_service import AsignacionService
    user = Auth.load_session()
    if not user or user.get("rol") not in ["admin","gerente"]:
        err("Acceso denegado"); return
    AsignacionService.asignar_departamento(empleado_id, depto_id)
    ok("Asignación de departamento actualizada")

@asignar.command("proyecto")
@click.option("--empleado_id", type=int, prompt=True)
@click.option("--proyecto_id", type=int, prompt=True)
def asg_proyecto(empleado_id, proyecto_id):
    from app.services.asignacion_service import AsignacionService
    user = Auth.load_session()
    if not user or user.get("rol") not in ["admin","gerente"]:
        err("Acceso denegado"); return
    AsignacionService.asignar_proyecto(empleado_id, proyecto_id)
    ok("Empleado asignado al proyecto")

@asignar.command("proyectos-de")
@click.option("--empleado_id", type=int, prompt=True)
def asg_list(empleado_id):
    from app.services.asignacion_service import AsignacionService
    rows = AsignacionService.listar_proyectos_de_empleado(empleado_id)
    for r in rows:
        click.echo(f"{r['proyecto_id']} | {r['nombre']}")

# ---------------- TIEMPO ----------------
@cli.group()
def tiempo():
    '''Registros de tiempo.'''
    pass

@tiempo.command("add")
@click.option("--empleado_id", type=int, prompt=True)
@click.option("--proyecto_id", type=int, prompt=True)
@click.option("--fecha", prompt=True, help="YYYY-MM-DD")
@click.option("--horas", type=float, prompt=True)
@click.option("--descripcion", default=None)
def t_add(empleado_id, proyecto_id, fecha, horas, descripcion):
    from app.models.registro_tiempo import RegistroTiempo
    from app.services.tiempo_service import TiempoService
    user = Auth.load_session()
    if not user or user.get("rol") not in ["admin","gerente","usuario"]:
        err("Acceso denegado"); return
    reg = RegistroTiempo(empleado_id, proyecto_id, fecha, horas, descripcion)
    try:
        rid = TiempoService.crear(reg)
        ok(f"Registro de tiempo id={rid} creado")
    except Exception as e:
        err(str(e))

@tiempo.command("list")
@click.option("--desde", default=None)
@click.option("--hasta", default=None)
@click.option("--empleado_id", type=int, default=None)
@click.option("--proyecto_id", type=int, default=None)
def t_list(desde, hasta, empleado_id, proyecto_id):
    from app.services.tiempo_service import TiempoService
    rows = TiempoService.listar(desde, hasta, empleado_id, proyecto_id)
    for r in rows:
        click.echo(f"{r['id']} | {r['fecha']} | {r['horas']}h | {r['empleado']} -> {r['proyecto']}")

@tiempo.command("delete")
@click.option("--id", "reg_id", type=int, prompt=True)
def t_delete(reg_id):
    from app.services.tiempo_service import TiempoService
    TiempoService.eliminar(reg_id)
    ok("Registro eliminado")



# ---------------- INDICADORES (Etapa 2) ----------------
@cli.group()
def indicadores():
    '''Consulta y registro de indicadores económicos (UF, IVP, IPC, UTM, DOLAR, EURO).'''
    pass

@indicadores.command("fetch")
@click.option("--tipo", prompt=True, help="UF, IVP, IPC, UTM, DOLAR, EURO")
@click.option("--fecha", default=None, help="YYYY-MM-DD o DD-MM-YYYY")
@click.option("--desde", default=None, help="Para rango: fecha inicio")
@click.option("--hasta", default=None, help="Para rango: fecha fin")
def ind_fetch(tipo, fecha, desde, hasta):
    from app.services.indicadores_service import IndicadoresService
    try:
        serie = IndicadoresService.fetch(tipo, fecha, desde, hasta)
        if not serie:
            click.echo("No se recibieron datos.")
            return
        for v in serie:
            click.echo(f"{v['nombre']} | {v['fecha_valor']} | {v['valor']}")
    except Exception as e:
        err(str(e))

@indicadores.command("save")
@click.option("--tipo", prompt=True)
@click.option("--fecha", default=None)
@click.option("--desde", default=None)
@click.option("--hasta", default=None)
def ind_save(tipo, fecha, desde, hasta):
    from app.services.indicadores_service import IndicadoresService
    from security.auth import Auth
    user = Auth.load_session()
    if not user or user.get("rol") not in ["admin","gerente"]:
        err("Acceso denegado"); return
    try:
        serie = IndicadoresService.fetch(tipo, fecha, desde, hasta)
        if not serie:
            err("No hay datos para guardar"); return
        proveedor = os.getenv("INDICADORES_API_URL","").rstrip("/")
        total = IndicadoresService.save_values(serie, user["username"], proveedor)
        # Log de la consulta
        IndicadoresService.log_consulta(tipo, user["username"], proveedor, fecha_valor=fecha, desde=desde, hasta=hasta)
        ok(f"{total} registros guardados en BD")
    except Exception as e:
        err(str(e))

@indicadores.command("list")
@click.option("--tipo", default=None)
@click.option("--desde", default=None)
@click.option("--hasta", default=None)
def ind_list(tipo, desde, hasta):
    from app.services.indicadores_service import IndicadoresService
    try:
        rows = IndicadoresService.list_db(tipo, desde, hasta)
        if not rows:
            click.echo("Sin datos en BD para ese filtro.")
            return
        for r in rows:
            click.echo(f"{r['nombre']} | {r['fecha_valor']} | {r['valor']} | {r['proveedor']}")
    except Exception as e:
        err(str(e))

# ---------------- PING DB ----------------
@cli.command("ping-db")
def ping_db():
    """Prueba la conexión a MySQL/MariaDB (buffered cursor para evitar 'Unread result found')."""
    try:
        from app.db.mysql_conn import Db
        cn = Db.get_connection()
        cur = cn.cursor(buffered=True)
        cur.execute("SELECT 1")
        _ = cur.fetchone()  # consumir resultado
        cur.close()
        cn.close()
        ok("Conexión OK a MySQL")
    except Exception as e:
        err(f"Error de conexión: {e}")

