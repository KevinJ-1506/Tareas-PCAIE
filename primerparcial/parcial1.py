import psycopg2

datos_cliente = {}

# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        dbname="PRIMERPARCIAL", 
        user="postgres", 
        password="hidrogeno", 
        host="localhost", 
        port="5432"
    )
    print("Conexión a la base de datos establecida.")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    exit()

def menu():
    while True:
        print("\n\t\t¡Bienvenido al Menú Principal!")
        print("1. Ingresar Usuario")
        print("2. Ejecución de cobro")
        print("3. Historial de datos")
        print("4. Borrar datos")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        if opcion not in ["1", "2", "3", "4", "5"]:
            print("Opción no válida. Intente nuevamente.")
            continue
        
        if opcion == "1":
            ingreso_usuario()
        elif opcion == "2":
            if datos_cliente:
                ejecucion()
            else:
                print("Primero debe ingresar los datos del cliente (opción 1).")
        elif opcion == "3":
            historial_datos()
        elif opcion == "4":
            borrar_datos()
        elif opcion == "5":
            print("¡Gracias por visitarnos! Vuelva pronto.")
            break

def ingreso_usuario():
    while True:
        nombre = input("Ingrese el nombre del usuario: ")
        if nombre:
            datos_cliente["nombreu"] = nombre
            print("Datos ingresados correctamente.")
            break
        else:
            print("El nombre no puede estar vacío. Intente de nuevo.")

def ejecucion():
    ingreso_datos()
    ingreso_placa()
    combustible()
    cantidad_litros()
    generar_factura()

def ingreso_datos():
    while True:
        nombre = input("Ingrese el nombre del Cliente: ")
        if nombre:
            datos_cliente["nombre"] = nombre
            break
        else:
            print("El nombre no puede estar vacío. Intente de nuevo.")

def ingreso_placa():
    while True:
        placa = input("Ingrese la placa del carro: ")
        if placa:
            datos_cliente["placa"] = placa
            print("Datos ingresados correctamente.")
            break
        else:
            print("La placa no puede estar vacía. Intente de nuevo.")

def combustible():
    opciones = {"1": "Combustible Regular", "2": "Combustible Premium", "3": "Diesel"}
    precios = {"1": 10, "2": 12, "3": 9}
    while True:
        print("\n\t\t¡Seleccione combustible!")
        print("1. Gasolina Regular    Q 10.00 litro")
        print("2. Gasolina Premium    Q 12.00 litro")
        print("3. Diesel              Q  9.00 litro")
        opcion = input("Seleccione una opción: ")
        if opcion in opciones:
            datos_cliente["combustible"] = opciones[opcion]
            datos_cliente["precio"] = precios[opcion]
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def cantidad_litros():
    while True:
        try:
            litros = float(input("Ingrese cantidad de litros despachados: "))
            if litros > 0:
                datos_cliente["clitros"] = litros
                datos_cliente["total"] = datos_cliente["precio"] * litros
                print(f"El total es: Q {datos_cliente['total']:.2f}")
                break
            else:
                print("La cantidad de litros debe ser un número positivo.")
        except ValueError:
            print("Error: el dato ingresado debe ser un número entero positivo.")

def generar_factura():
    try:
        factura = f"""
----------------------------------------------
Nombre: {datos_cliente['nombre']}
No. Placa: {datos_cliente['placa']}
Tipo combustible: {datos_cliente['combustible']}
Litros: {datos_cliente['clitros']:.2f}
Precio por Litro: Q {datos_cliente['precio']:.2f}
Total a pagar: Q {datos_cliente['total']:.2f}
Le atendió: {datos_cliente['nombreu']}
----------------------------------------------
"""
        print("Factura generada:")
        print(factura)
        
        cursor = conn.cursor()
        query = """INSERT INTO historialfacturas VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        valores = (
            datos_cliente["nombre"], datos_cliente["placa"], datos_cliente["combustible"],
            datos_cliente["clitros"], datos_cliente["precio"], datos_cliente["total"], datos_cliente["nombreu"]
        )
        cursor.execute(query, valores)
        conn.commit()
        print("Factura guardada en la base de datos.")
        cursor.close()
        
        # Guardar la factura en un archivo de texto
        with open("facturas.txt", "a") as file:
            file.write(factura + "\n")
        print("Factura guardada en 'facturas.txt'.")
    except Exception as e:
        print(f"Error al generar la factura: {e}")

def historial_datos():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historialfacturas;")
        registros = cursor.fetchall()
        print("---------------------------------------------------")
        print("Historial de datos desde la base de datos:")
        for row in registros:
            print(row)
        print("---------------------------------------------------")
        cursor.close()
    except Exception as e:
        print(f"Error al obtener el historial: {e}")

def borrar_datos():
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM historialfacturas;")
        conn.commit()
        print("Todos los registros de la base de datos han sido eliminados.")
        cursor.close()
    except Exception as e:
        print(f"Error al borrar los datos de la base de datos: {e}")

menu()
conn.close()
