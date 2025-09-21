def saludar():
    print("¡Hola, mundo!")


# Esta es nuestra función decoradora
def mi_decorador(funcion_original):
    # 1. Definimos una nueva función interna (el "papel de regalo")
    def funcion_envoltorio():
        print("--- Iniciando la ejecución ---")
        
        # 2. Llamamos a la función original que nos pasaron
        funcion_original()
        
        print("--- Ejecución finalizada ---")
    
    # 3. La función decoradora devuelve la función envuelta
    return funcion_envoltorio


# Usamos el decorador
#saludar = mi_decorador(saludar)

saludar()    