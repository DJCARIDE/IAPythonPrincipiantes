def funcion_completa(parametro_fijo, *args, **kwargs):
    print(f"Parámetro fijo: {parametro_fijo}")
    
    print("\nArgumentos posicionales (*args):")
    for arg in args:
        print(f"- {arg}")
        
    print("\nArgumentos de palabra clave (**kwargs):")
    for key, value in kwargs.items():
        print(f"- {key}: {value}")

funcion_completa(
    "¡Hola!",                   # parametro_fijo
    10, "Python", True,         # *args
    nombre="Carlos",            # **kwargs
    proyecto="Demo"             # **kwargs
)