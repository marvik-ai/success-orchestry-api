# 🛠 Backend Development Standards & Quality Control

Este documento define la configuración del entorno de desarrollo y los estándares de calidad para el backend del **Success Orchestry API**.

Usamos un stack de alto rendimiento optimizado para **Python 3.14.2**, manteniendo **paridad total con el estilo de código del frontend**.

---

## 🚀 Quick Start: Setup Guide

Para configurar tu entorno local de la manera más rápida, contamos con un comando de automatización en nuestro **Makefile** que gestiona todo el proceso por ti.

### ⭐ Comando principal

**`make setup`**

Este comando realiza **tres acciones críticas en una sola ejecución**:

1. Crea el entorno virtual (`.venv`)
2. Instala todas las dependencias (producción y desarrollo)
3. Configura y activa los **Git Hooks**:
   - `pre-commit`
   - `commit-msg`
   - `pre-push`

---

## 🔌 Extensiones Requeridas (VS Code / Cursor)

Para recibir feedback en tiempo real mientras codificas y evitar que los hooks rechacen tus cambios, es **obligatorio** instalar:

- **Ruff (Astral-sh)**
  Linter y formatter ultra-rápido.

- **Mypy Type Checker**
  Resalta errores de tipado estático directamente en el editor.

---

## 🤖 Automatización en el Editor (`settings.json`)

Para garantizar que el código cumpla con los estándares **sin esfuerzo manual**, utilizamos una configuración compartida en
`.vscode/settings.json`.

### ¿Por qué usamos este archivo?

- **Unificar criterios**
  Asegura que todos los desarrolladores (VS Code o Cursor) formateen el código exactamente igual.

- **Evitar ruidos en Git**
  Previene cambios innecesarios de espacios o comillas en los Pull Requests.

- **Silencio visual**
  Oculta carpetas de caché innecesarias (`.ruff_cache`, `__pycache__`) para mantener el árbol de archivos limpio.

---

## ⌨️ El comando mágico: Ctrl + S (o Cmd + S)

En este proyecto, **guardar el archivo no solo almacena los cambios**, sino que ejecuta automáticamente el plugin de **Ruff**.

### ¿Por qué es necesario este flujo?

- **Feedback instantáneo**
  Al presionar `Ctrl + S`, Ruff:
  - Reordena imports
  - Cambia comillas dobles por simples
  - Elimina espacios extra

- **Cero fricción en el commit**
  Si formateas al guardar, el `pre-commit` nunca rechazará tu trabajo, permitiendo un flujo continuo y fluido.

---

## ⚡ Optimización del Ciclo de Feedback: Mypy a `pre-push`

Hemos movido el chequeo de tipos (**Mypy**) del stage de `commit` al stage de `push`.

### ✅ Agilidad en el desarrollo

Ruff es instantáneo, pero Mypy analiza todo el árbol de dependencias y puede tardar varios segundos.
Moverlo al `push` permite **commits locales inmediatos**.

---

## 🔄 Flujo de Trabajo de Desarrollo

### 1. Chequeos Automáticos (Git Hooks)

- **`pre-commit` (Instantáneo)**
  Ejecuta Ruff.
  👉 Si usas `Ctrl + S` habitualmente, este check siempre pasará en verde.

- **`commit-msg`**
  Valida el estándar del mensaje:

TICKET-ID tipo: descripción


- **`pre-push` (Riguroso)**
Ejecuta:
- **Mypy**
- **Suite de tests**

Es el filtro de calidad final antes de llegar a la rama remota.

---

### 2. Comandos Manuales (Makefile)

- **`make format`**
Corrección manual (en caso de no usar el plugin del editor).

- **`make lint`**
Escaneo de errores sin modificar archivos.

- **`make ci`**
Suite completa:
- Format
- Lint
- Types
- Tests

👉 Recomendado antes de iniciar un `push`.

---

## 🛠 Troubleshooting

### ❌ ¿El commit fue rechazado?

Verifica si el error es de formato (¿olvidaste guardar con `Ctrl + S`?) o de mensaje de commit.
El mensaje debe empezar con el ID del ticket, por ejemplo:

IAS-123 feat: añadir endpoint de healthcheck

---

### ❌ ¿El push falló pero el commit funcionó?

Esto indica que:
- Mypy detectó una inconsistencia de tipos **o**
- Algún test falló

👉 Revisa la consola, corrige el error, haz un nuevo commit y reintenta el `push`.

---

## 📐 Estándares de Código

El archivo **`pyproject.toml`** define las reglas que Ruff aplica automáticamente al guardar:

- **Comillas simples (`' '`)**
  Obligatorio para paridad con el frontend.

- **Longitud de línea: 100**
  Equilibrio entre legibilidad y densidad de código.

- **Sintaxis moderna**
  Uso de características nativas de **Python 3.14** (`UP`).

- **FastAPI Compliance**
  Se permite la regla **B008** para el uso correcto de `Depends()`.

---
