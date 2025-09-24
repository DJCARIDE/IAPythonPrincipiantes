import os
import importlib.util

# Cargar el módulo desde el archivo con nombre no convencional: "11 - clientesdb.py"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_PATH = os.path.join(BASE_DIR, "11 - clientesdb.py")

spec = importlib.util.spec_from_file_location("clientes_app", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Exponer el objeto WSGI para Gunicorn
app = module.app
