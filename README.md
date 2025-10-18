# Todos Api

## Primeros pasos

Crear el entorno virtual:

```bash
py -m venv .venv
```

Activar el entorno (elige según tu shell):

- PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

- Command Prompt (CMD):
```cmd
.venv\Scripts\activate
```

- Git Bash / WSL:
```bash
source .venv/bin/activate
```

Actualizar pip e instalar dependencias:

```bash
py -m pip install --upgrade pip
pip install -r requirements.txt
```

## Iniciar el proyecto
```bash
cd src
fastapi dev main.py
```