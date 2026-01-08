from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

import typer

from src.utils.employees_seed_factory import seed_employees


F = TypeVar('F', bound=Callable[..., Any])

if TYPE_CHECKING:
    # Shadow Typer to provide valid type hints for decorators
    class TyperShadow:
        def command(self, *args: Any, **kwargs: Any) -> Callable[[F], F]:
            def decorator(f: F) -> F:
                return f

            return decorator

    app = TyperShadow()
else:
    app = typer.Typer()


@app.command()
def employees(qty: int = 10) -> None:
    """Genera empleados ficticios."""
    typer.echo(f'🚀 Generando {qty} empleados...')
    seed_employees(qty)


@app.command()
def all(qty: int = 10) -> None:
    """Ejecuta TODOS los seeders disponibles."""
    typer.echo('🚀 Iniciando carga completa de datos...')
    seed_employees(qty)
    typer.echo('✨ Carga completa finalizada.')


if __name__ == '__main__':
    if not TYPE_CHECKING:
        # Use type cast or internal check to call the real app
        app()  # type: ignore
