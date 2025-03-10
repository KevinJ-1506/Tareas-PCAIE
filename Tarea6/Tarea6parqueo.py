import psycopg2
import math

datos_cliente = {}

def conectar_bd():
    try:
        conn = psycopg2.connect(
            dbname='Tarea6',
            host='localhost',
            port='5432',
            user='postgres',
            password='hidrogeno'
        )
        print('Conexión a la base de datos establecida.')
        return conn
    except Exception as e:
        print(f'No se pudo conectar a la base de datos: {e}')
        return None

def menu():
    while True:
        print('\n\t\t¡Bienvenido al Menú Principal!')
        print('1. Ingresar datos de facturación')
        print('2. Generación de factura')
        print('3. Historial de datos')
        print('4. Borrar datos')
        print('5. Salir')
        
        opcion = input('Seleccione una opción: ')
        if not opcion.isdigit():
            print('Opción no válida. Debe ser un número entero.')
            continue
        
        opcion = int(opcion)
        if opcion == 1:
            ingreso_datos()
        elif opcion == 2:
            if datos_cliente:
                generar_factura()
            else:
                print('Primero debe ingresar los datos del cliente (opción 1).')
        elif opcion == 3:
            historial_datos()
        elif opcion == 4:
            borrar_datos()
        elif opcion == 5:
            print('¡Gracias por visitarnos! Vuelva pronto.')
            break
        else:
            print('Opción no válida. Intente nuevamente.')

def ingreso_datos():
    global datos_cliente
    while True:
        nombre = input('Ingrese el nombre del usuario: ')
        if nombre.isdigit() or not nombre.strip():
            print('El nombre no puede ser un número o estar vacío. Intenta de nuevo.')
        else:
            datos_cliente['nombre'] = nombre
            break
    
    while True:
        nit = input('Ingrese el NIT del usuario (sin guiones ni espacios): ')
        if not nit.isdigit():
            print('El NIT debe contener solo números.')
        else:
            datos_cliente['nit'] = nit
            break
    
    while True:
        placa = input('Ingrese la placa del carro: ')
        if not placa.strip():
            print('La placa no puede estar vacía.')
        else:
            datos_cliente['placa'] = placa
            break
    
    while True:
        try:
            entrada = float(input('Ingrese la hora de entrada (Hora.Minutos): '))
            datos_cliente['entrada'] = entrada
            break
        except ValueError:
            print('La hora de entrada debe ser un número válido.')
    
    while True:
        try:
            salida = float(input('Ingrese la hora de salida (Hora.Minutos): '))
            if salida <= datos_cliente['entrada']:
                print('La hora de salida debe ser mayor que la hora de entrada.')
            else:
                datos_cliente['salida'] = salida
                break
        except ValueError:
            print('La hora de salida debe ser un número válido.')
    
    print('Datos ingresados correctamente.')

def total_pago(hora_entrada, hora_salida):
    tiempo_estancia = hora_salida - hora_entrada
    horas_totales = math.ceil(tiempo_estancia)
    return 15.00 if horas_totales == 1 else 15.00 + (horas_totales - 1) * 20.00

def generar_factura():
    conn = conectar_bd()
    if not conn:
        return
    
    try:
        tiempo_estancia = datos_cliente['salida'] - datos_cliente['entrada']
        pago_total = total_pago(datos_cliente['entrada'], datos_cliente['salida'])

        factura = f"""
        ----------------------------------------------
        Nombre: {datos_cliente['nombre']}
        NIT: {datos_cliente['nit']}
        Placa: {datos_cliente['placa']}
        Hora de entrada: {datos_cliente['entrada']:.2f} [h.m]
        Hora de salida: {datos_cliente['salida']:.2f} [h.m]
        Tiempo de estancia: {tiempo_estancia:.2f} horas
        Total a pagar: Q{pago_total:.2f}
        ----------------------------------------------
        """
        
        print('Factura generada:')
        print(factura)

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO parqueo (nombre, nit, noplaca, horaentrada, horasalida, tiemporestancia, pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (datos_cliente['nombre'], datos_cliente['nit'], datos_cliente['placa'],
                  datos_cliente['entrada'], datos_cliente['salida'], tiempo_estancia, pago_total))
            conn.commit()
        print('Factura guardada en la base de datos.')
    
        with open('facturas.txt', 'a') as f:
            f.write(factura + '\n')
        print('Factura guardada en "facturas.txt".')
    except Exception as e:
        print(f'Error al generar la factura: {e}')
    finally:
        conn.close()

def historial_datos():
    conn = conectar_bd()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM parqueo;")
            registros = cur.fetchall()
            print('---------------------------------------------------')
            print('Historial de datos desde la base de datos:')
            for registro in registros:
                print(registro)
            print('---------------------------------------------------')
    except Exception as e:
        print(f'Error al obtener el historial: {e}')
    finally:
        conn.close()

def borrar_datos():
    conn = conectar_bd()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM parqueo;")
            conn.commit()
        print('Todos los registros de la base de datos han sido eliminados.')
    except Exception as e:
        print(f'Error al borrar los datos de la base de datos: {e}')
    finally:
        conn.close()
    
    try:
        open('facturas.txt', 'w').close()
        print('El contenido del archivo ha sido eliminado.')
    except Exception as e:
        print(f'Error al eliminar el archivo: {e}')

menu()
