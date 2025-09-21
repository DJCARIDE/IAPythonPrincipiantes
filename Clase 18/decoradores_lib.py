# Módulo reutilizable de decoradores

def mi_decorador(funcion_original):
    """Un decorador simple que muestra mensajes antes y después
    de ejecutar la función original.
    """
    def funcion_envoltorio():
        print("--- Iniciando la ejecución ---")
        funcion_original()
        print("--- Ejecución finalizada ---")
    return funcion_envoltorio

def medir_tiempo(func):
    def envoltorio(*args, **kwargs):
        # *args y **kwargs permiten que el decorador funcione
        # con cualquier función, sin importar sus argumentos.
        
        inicio = time.time()
        resultado = func(*args, **kwargs) # Ejecutamos la función original
        fin = time.time()
        
        print(f"La función '{func.__name__}' tardó {fin - inicio:.4f} segundos.")
        return resultado # Devolvemos lo que la función original devolvió
    return envoltorio    
