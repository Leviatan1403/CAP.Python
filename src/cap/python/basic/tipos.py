# Comentario en linea

"""
Comentario Multilinea
Prueba
de un
Comentario
"""

mi_entero = 10
mi_flotante = 10.5
mi_cadena = "Hola Mundo"
mi_boolean = True

print("Hola mundo", mi_entero)

# impresion del tipo de dato
print(type(mi_entero))

# Impresion de variables dinamicas
mi_variable: int = 10
print(type(mi_variable))
mi_variable: float = 10.5
print(type(mi_variable))
mi_variable: str = "Hola Mundo"
print(type(mi_variable))
mi_variable: bool = True
print(type(mi_variable))

# Estructura de datos

# Listas
mi_lista = [1, 2, 3]
print(type(mi_lista))

print("Mi lista antes del cambio", mi_lista)
mi_lista[2] = 4
print("Mi lista despues del cambio", mi_lista)

# Tuplas
mi_tupla: tuple = (1, 2, 3)

# Diccionarios
mi_diccionario: dict = {"clave1": "valor1", "clave2": "valor2"}

# f-string
nombre: str = "Manu"
print("Hola, " + nombre)  # Impresion tradicional
print(f"Hola, {nombre}")  # Impresion con F-string

# For Comprimido
cuadrados: list = [x**2 for x in range(10)]
print(cuadrados)
