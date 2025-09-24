# Ejecutar la aplicación Flask con Gunicorn

Este proyecto contiene una aplicación Flask y un archivo de entrada WSGI para ejecutarla con Gunicorn en entornos Linux/WSL. También se describe una alternativa para Windows nativo con Waitress y una opción con Docker.

## Estructura esperada del proyecto

- `wsgi.py`: expone el objeto `app` para el servidor WSGI (Gunicorn/Waitress).
- `11 - clientesdb.py`: módulo principal Flask donde se define `app` y las rutas.
- `database.py`: utilidades para conexión SQLite y función `init_db()`.
- `schema.sql`: esquema de base de datos SQLite.
- `templates/`: plantillas HTML usadas por la app.

Asegurate de ejecutar los comandos desde el directorio raíz del proyecto (donde están estos archivos), para que las rutas relativas funcionen correctamente (por ejemplo, la base `clientes.db`).

## Requisitos

- Python 3.8+
- Entorno Linux/WSL recomendado para usar Gunicorn en Windows

Dependencias mínimas:

```bash
pip install flask gunicorn
```

Para Windows nativo (sin WSL), alternativa con Waitress:

```bash
pip install flask waitress
```

## Inicialización de la base de datos (importante)

Actualmente, la app ejecuta la inicialización de base de datos al importar el módulo principal (por ejemplo, dentro de `11 - clientesdb.py`):

```python
with app.app_context():
    init_db()
```

Y `schema.sql` comienza con:

```sql
DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes (...)
```

Esto implica dos consideraciones:

- Al iniciar la app, se borra y recrea la tabla `clientes` (se pierden datos).
- Si ejecutás Gunicorn con múltiples workers, cada worker puede disparar la inicialización, lo que genera condiciones de carrera.

### Opciones para evitar problemas

- Opción rápida (desarrollo): usar 1 worker en Gunicorn para evitar efectos colaterales por concurrencia.
- Opción recomendada (producción/desarrollo estable):
  - Cambiar `schema.sql` a `CREATE TABLE IF NOT EXISTS clientes (...)` y quitar la línea `DROP TABLE IF EXISTS ...`.
  - Asegurar que los datos de ejemplo solo se inserten si la tabla está vacía (el proyecto ya lo hace consultando `COUNT(*)`).
  - Evitar llamar `init_db()` automáticamente en el import de la app. En su lugar, ejecutar la inicialización de forma manual una sola vez o mediante un comando/CLI dedicado.

Ejemplo de flujo recomendado:

1) Ajustar `schema.sql` para que NO borre datos (usar `IF NOT EXISTS`).
2) Ejecutar la inicialización una vez antes de arrancar el servidor:

```bash
python -c "import importlib.util, os; 
from flask import Flask; 
base=os.path.dirname(os.path.abspath(__file__)); 
spec=importlib.util.spec_from_file_location('clientes_app', os.path.join(base, '11 - clientesdb.py')); 
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); 
app=mod.app; 
from database import init_db; 
with app.app_context(): init_db()"
```

3) Arrancar el servidor WSGI (ver siguientes secciones).

## Ejecutar con Gunicorn (Linux/WSL)

1) Crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Instalar dependencias:

```bash
pip install flask gunicorn
```

3) Ejecutar Gunicorn desde el directorio del proyecto:

- Modo seguro inicial (1 worker):

```bash
gunicorn -w 1 -b 0.0.0.0:8000 wsgi:app
```

- Multiproceso/concurrencia (asegurate de tener la inicialización idempotente como se describió antes):

```bash
gunicorn -w 2 --threads 2 -b 0.0.0.0:8000 wsgi:app
```

4) Probar en el navegador:

```
http://localhost:8000/
```

Notas:
- Ejecutá Gunicorn siempre desde el directorio raíz del proyecto. `database.py` usa rutas relativas (`clientes.db`, `schema.sql`).
- Ajustá `-w` (workers) y `--threads` según los recursos y la carga.

## Alternativa en Windows nativo (Waitress)

Si no querés usar WSL, podés ejecutar la app con Waitress (servidor WSGI compatible con Windows):

1) Crear y activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias:

```powershell
pip install flask waitress
```

3) Ejecutar el servidor:

```powershell
waitress-serve --listen=0.0.0.0:8000 wsgi:app
```

4) Probar en el navegador:

```
http://localhost:8000/
```

## Docker (opcional)

Podés contenedorar la app con Docker. Ejemplo de `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask gunicorn
EXPOSE 8000
CMD ["gunicorn", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
```

Construir y ejecutar:

```bash
docker build -t flask-clientes .
docker run --rm -p 8000:8000 -v $(pwd)/clientes.db:/app/clientes.db flask-clientes
```

Si usás Windows PowerShell, podés reemplazar `$(pwd)` por `${PWD}` o mapear rutas absolutas.

## Consejos finales

- Para desarrollo, `-w 1` es suficiente y evita efectos de la inicialización concurrente.
- Para producción, asegurate de que la inicialización de la base de datos sea idempotente y no borre datos (evitar `DROP TABLE` en `schema.sql`).
- Verificá logs de la app/servidor si encontrás errores al iniciar.
- Si cambiás la ubicación de `schema.sql` o del archivo de base de datos, actualizá las rutas en `database.py`.
