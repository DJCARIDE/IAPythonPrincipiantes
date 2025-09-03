from pelicula import Pelicula
from servicio_peliculas import ServicioPeliculas

class AppCatalogo:
    def __init__(self):
        self.servicio_peliculas = ServicioPeliculas()

    def mostrar_menu(self):
        print("*** Bienvenido al Catálogo de Películas ***\n")
        while True:
            try:
                print(f"=== MENU ===\n"
                      f"1. Agregar película\n"
                      f"2. Listar películas\n"
                      f"3. Eliminar datos del catálogo\n"
                      f"4. Salir\n")
                
                opcion = int(input("Seleccione una opción (1-4): "))
                if opcion == 1:
                    nombre_pelicula = input("Ingrese el nombre de la película: ")
                    director = input("Ingrese el director: ")
                    anio = input("Ingrese el año: ")
                    try:
                        anio = int(anio)
                    except ValueError:
                        anio = None
                    pelicula = Pelicula(nombre=nombre_pelicula, director=director, anio=anio)
                    self.servicio_peliculas.agregar_pelicula(pelicula)
                elif opcion == 2:
                    self.servicio_peliculas.listar_peliculas()
                elif opcion == 3:
                    self.servicio_peliculas.eliminar_catalogo()
                    print("Catálogo de películas eliminado.\n")
                elif opcion == 4:
                    print("Saliendo del catálogo...")
                    break
                else:
                    print("Opción no válida. Intente de nuevo.\n")
            except ValueError:
                print("Por favor, ingrese un número válido.\n")        
            except Exception as e:
                print(f"Error al mostrar el menú: {e}\n")

if __name__ == "__main__":
    app = AppCatalogo()
    app.mostrar_menu()
   
