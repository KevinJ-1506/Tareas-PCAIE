import psycopg2

datos = {}

def conectar_bd():
    try:
        conn = psycopg2.connect(
            dbname='tarea5',
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
        print('\nSeleccione una opción:')
        print('1. Ingresar datos')
        print('2. Mostrar datos')
        print('3. Guardar')
        print('4. Leer')
        print('5. Borrar')
        print('6. Salir')
        
        opcion = input('Ingrese su elección: ')
        if not opcion.isdigit():
            print('Opción no válida. Debe ser un número entero.')
            continue
        
        opcion = int(opcion)
        if opcion == 1:
            ingresar_datos()
        elif opcion == 2:
            mostrar_datos()
        elif opcion == 3:
            guardar()
        elif opcion == 4:
            leer()
        elif opcion == 5:
            borrar()
        elif opcion == 6:
            print('¡Gracias por visitarnos! Vuelva pronto.')
            break
        else:
            print('Opción no válida. Intente nuevamente.')

def ingresar_datos():
    global datos
    while True:
        nombre = input('Ingrese el nombre del usuario: ')
        if nombre.isdigit() or not nombre.strip():
            print('El nombre no puede ser un número o estar vacío. Intenta de nuevo.')
        else:
            datos['nombre'] = nombre
            break
    
    while True:
        try:
            peso = float(input('Ingrese el peso del usuario en kilogramos: '))
            if peso <= 0:
                raise ValueError('Peso inválido. Debe ser un número positivo.')
            datos['peso'] = peso
            break
        except ValueError as e:
            print(e)
    
    while True:
        try:
            altura = float(input('Ingrese la altura del usuario en metros: '))
            if altura <= 0:
                raise ValueError('Altura inválida. Debe ser un número positivo.')
            datos['altura'] = altura
            break
        except ValueError as e:
            print(e)
    
    datos['IMC'] = datos['peso'] / (datos['altura'] ** 2)
    if datos['IMC'] < 18.5:
        datos['categoria'] = 'Bajo Peso'
    elif datos['IMC'] < 25:
        datos['categoria'] = 'Peso Normal'
    else:
        datos['categoria'] = 'Sobre Peso'
    
    print('Información guardada correctamente.')

def mostrar_datos():
    if 'nombre' in datos:
        print(f'El Índice de Masa Corporal de {datos["nombre"]} es de {datos["IMC"]:.2f}')
        print(f'{datos["nombre"]} se encuentra en la categoría: {datos["categoria"]}')
    else:
        print('No hay datos ingresados.')

def guardar():
    conn = conectar_bd()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO imc (nombre, peso, altura, imc, categoria)
                VALUES (%s, %s, %s, %s, %s)
            """, (datos['nombre'], datos['peso'], datos['altura'], datos['IMC'], datos['categoria']))
            conn.commit()
        print('Datos guardados en la base de datos.')
    except Exception as e:
        print(f'Error al guardar en la base de datos: {e}')
    finally:
        conn.close()
    
    try:
        archivo = 'IMC.txt'
        with open(archivo, 'a') as f:
            f.write(f"Nombre: {datos['nombre']}\nPeso: {datos['peso']} kg\nAltura: {datos['altura']} m\nIMC: {datos['IMC']:.2f}\nCategoría: {datos['categoria']}\n---\n")
        print('Datos guardados en "IMC.txt".')
    except Exception as e:
        print(f'Error al guardar en el archivo: {e}')

def leer():
    try:
        archivo = 'IMC.txt'
        with open(archivo, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print('No se encontraron datos guardados.')

def borrar():
    conn = conectar_bd()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM imc;")
            conn.commit()
        print('Todos los registros de la base de datos han sido eliminados.')
    except Exception as e:
        print(f'Error al borrar los datos de la base de datos: {e}')
    finally:
        conn.close()
    
    try:
        archivo = 'IMC.txt'
        with open(archivo, 'w') as f:
            f.write('')
        print('El contenido del archivo ha sido eliminado.')
    except Exception as e:
        print(f'Error al eliminar el archivo: {e}')

menu()
