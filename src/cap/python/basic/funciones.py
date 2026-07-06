"""
Funciones
"""


# Funcion sin Argumentos
def saludar() -> None:
    # Funcion para saludar
    print("Hola Mundo")


saludar()


# Funcion con Argumentos
def saludar(nombre: str) -> None:
    # Funcion que recibe un parametro personalizado
    print(f"Hola, {nombre}")


saludar("Manuel")


# Funcion con un argumento opcional
def saludar(nombre: str = "Opcional") -> None:
    # Funcion que recibe un parametro personalizado
    print(f"Hola, {nombre}")


saludar()
saludar("Manuel")

# Lambda

# Para operaciones sencillas
sumar = lambda num_1, num_2: num_1 + num_2
result: int = sumar(5, 3)
print(f"Resultado, {result}")

# Maps

print(list(map(lambda num_1: num_1**2, range(5))))


def potencia(num_1: int) -> int:
    return num_1**2


print(list(map(potencia, range(5))))

# Filters

print("Filter")
print(list(filter(lambda x: x % 2 == 0, range(10))))
