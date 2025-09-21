import time
from decoradores_lib import medir_tiempo

@medir_tiempo
def proceso_largo(nombre):
    print(f"Iniciando proceso para {nombre}...")
    time.sleep(2) # Simulamos una tarea que tarda 2 segundos
    print("Proceso completado.")
    return "Finalizado"

@medir_tiempo
def proceso_corto():
    time.sleep(0.5)

# Llamamos a las funciones como si nada
resultado_final = proceso_largo("archivos")
proceso_corto()
print(f"El resultado fue: {resultado_final}")