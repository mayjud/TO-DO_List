# Kanban To-Do con FastAPI

Aplicación de tablero Kanban con tres columnas: Por realizar, En proceso y Realizadas.

## Requisitos

- Python 3.11+
- pip
- Entorno virtual opcional

## Instalación local

```bash
cd C:\DEVs\Azure_AppService\To_Do
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

La aplicación queda disponible en:

- http://localhost:8000/
- http://localhost:8000/health

## Estructura principal

- `app/main.py`: aplicación FastAPI
- `app/api/routes.py`: rutas de la API
- `app/services/task_service.py`: lógica de negocio
- `app/repositories/json_repository.py`: persistencia en tasks.json
- `app/templates/index.html`: plantilla Jinja2
- `app/static/`: CSS y JS frontend

## Persistencia

Se usa un archivo JSON llamado `tasks.json` ubicado en la raíz del proyecto. Si no existe, se crea automáticamente.

## Azure App Service Linux

1. Subir el proyecto al repositorio o zip.
2. En Azure App Service crear un recurso Linux con Python.
3. Configurar el Startup Command con:

```bash
bash startup.sh
```

4. Asegurarse de que `startup.sh` tenga permisos ejecutables.

## Convenciones

- Tareas con estado: `todo`, `doing`, `done`
- Identificador: UUID
- Fecha de creación: ISO 8601

## Funcionalidades

- Crear tarea
- Editar tarea
- Eliminar tarea
- Mover tarea entre columnas
- Persistencia local en JSON
- Arquitectura con capas: API, Service, Repository
