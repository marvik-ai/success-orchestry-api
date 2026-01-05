# 🛠 Backend Development Standards & Quality Control

Este documento define la configuración del entorno de desarrollo y los estándares de calidad para el backend del **Sucess Orchestry API**. Usamos un stack de alto rendimiento optimizado para **Python 3.14.2**, manteniendo total paridad con el estilo de código del frontend.

---

## 🚀 Quick Start: Setup Guide

Para configurar tu entorno local con todas las dependencias y los Git hooks automáticos, sigue estos pasos:

1. **Crear y activar el entorno virtual:**

python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate

2. **Ejecutar la instalación unificada:**

make install

`make install` instala las dependencias de producción y desarrollo (`requirements-dev.txt`) y activa los Git Hooks nativos de Python en tu carpeta `.git`.

---

## 🔌 Extensiones Requeridas (VS Code / Cursor)

Para recibir feedback en tiempo real mientras codificas y evitar errores durante los commits, instala:

- **Ruff (Astral-sh):** Linter y Formatter que aplica comillas simples automáticamente al guardar.
- **Mypy Type Checker (Microsoft o Matloob):** Muestra errores de type-hint en la pestaña "Problemas".

---

## 📂 El Rol de `.gitignore`

Aunque no está explícito en el ticket, el archivo `.gitignore` es técnicamente necesario para que el linter y el type checker funcionen correctamente.

- **Performance:** Evita que Ruff y Mypy escaneen miles de archivos dentro de `.venv` o `__pycache__`.
- **Precisión:** Sin él, las herramientas reportarían errores dentro de librerías de terceros en vez de tu código.
- **Éxito en CI:** Asegura que solo tu código fuente se suba y analice en el repositorio remoto.

---

## 🧰 El Stack Moderno de Herramientas

| Herramienta      | Función                   | Reemplaza...                                  |
|------------------|---------------------------|----------------------------------------------|
| Ruff             | Linter & Formatter        | Black, Flake8, isort, pyupgrade, pep8-naming|
| Mypy             | Static Type Checking       | Equivalente a TypeScript (modo estricto)    |
| pre-commit       | Gestor de Git Hooks       | Husky (implementación sin Node)              |
| Makefile         | Orquestador de Scripts    | Scripts de npm                               |

---

## 📐 Explicación Detallada de Reglas

Nuestro archivo `pyproject.toml` está configurado con las siguientes reglas clave:

- **Comillas simples (')**: Estrictamente forzado para coincidir con la configuración Prettier del frontend.
- **Longitud de línea (100):** Coincide con el printWidth del frontend.
- **UP (Pyupgrade):** Mantiene nuestra sintaxis actualizada a los estándares de Python 3.14.
- **B (Bugbear):** Detecta posibles bugs. Ignoramos específicamente `B008` para permitir la sintaxis `Depends()` de FastAPI.
- **D (Pydocstyle):** Aplica docstrings estilo Google, ideales para auto-generar documentación Swagger.

---

## 🔄 Flujo de Trabajo de Desarrollo

1. **Chequeos Automáticos (Git Hooks)**

- `pre-commit`: Ejecuta Ruff y Mypy en los archivos staged.
- `commit-msg`: Valida que el mensaje de commit coincida con el patrón del equipo: `TICKET-ID type: descripción`.
- `pre-push`: Ejecuta pytest para asegurar que no se suba código roto.

2. **Comandos Manuales (Makefile)**

- `make format`: Corrige automáticamente comillas, indentación y orden de imports.
- `make lint`: Escanea errores de estilo y sintaxis.
- `make typecheck`: Ejecuta un análisis estricto de type hints con Mypy.
- `make ci`: Ejecuta toda la suite completa (Format + Lint + Types + Tests). Úsalo antes de pushear.

---

## 🛠 Troubleshooting

Si tu commit es rechazado por un error de "Commit message invalid", verifica que uses un tipo válido (ejemplo: `feat:`, `fix:`, `chore:`) y que el Ticket ID (ejemplo: `IAS-10`) esté al principio del mensaje.
