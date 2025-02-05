import os
import math
import numpy
import numbers

def calcular_factorial():
    while True:
        numero = input("Ingresa un número para calcular su factorial: ")
        
        # Validar si el valor ingresado es un número
        if not numero.isdigit():
            print("El valor ingresado no es un número. Por favor, intenta de nuevo.")
            continue

        numero = int(numero)

        # Calcular el factorial
        factorial = 1
        for i in range(1, numero + 1):
            factorial *= i

        print(f"El factorial de {numero} es: {factorial}")
        break

calcular_factorial()
