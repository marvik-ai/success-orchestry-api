import typer

from src.utils.employees_seed_factory import seed_employees

app = typer.Typer()


@app.command()  # type: ignore[misc]
def employees(qty: int = 10) -> None:
    """Genera empleados ficticios.

    Uso: python seed.py employees --qty 50
    """
    typer.echo(f'🚀 Generando {qty} empleados...')
    seed_employees(qty)


@app.command()  # type: ignore[misc]
def all(qty: int = 10) -> None:
    """Ejecuta TODOS los seeders disponibles."""
    typer.echo('🚀 Iniciando carga completa de datos...')
    seed_employees(qty)
    typer.echo('✨ Carga completa finalizada.')


if __name__ == '__main__':
    app()
