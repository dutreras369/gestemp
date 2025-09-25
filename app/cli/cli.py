import click

@click.group()
def cli():
    """CLI del Sistema de Gestión de Empleados (Paso 0: entorno listo)."""
    pass

@cli.command("ping-db")
def ping_db():
    """Prueba conexión a MySQL con variables de entorno (.env)."""
    from app.db.mysql_conn import Db
    try:
        cn = Db.get_connection()
        click.echo("✅ Conexión OK a MySQL")
        cn.close()
    except Exception as e:
        click.echo(f"❌ Error de conexión: {e}")
