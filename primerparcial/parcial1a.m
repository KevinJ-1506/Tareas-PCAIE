clc;
clear;

% Cargar el paquete de base de datos
pkg load database

% Variables globales para almacenar los datos del cliente y la conexión a la base de datos
global datos_cliente conn;
datos_cliente = struct();

try
    % Conectar a la base de datos
    conn = pq_connect(setdbopts('dbname', 'PRIMERPARCIAL', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'hidrogeno'));
    disp('Conexión a la base de datos establecida.');
catch ME
    error('No se pudo conectar a la base de datos: %s', ME.message);
end

function menu()
    global datos_cliente;
    opcion = 0;
    while opcion ~= "5"
        fprintf('\n\t\t¡Bienvenido al Menú Principal!\n');
        fprintf('1. Ingresar Usuario\n');
        fprintf('2. Ejecucion de cobro\n');
        fprintf('3. Historial de datos\n');
        fprintf('4. Borrar datos\n');
        fprintf('5. Salir\n');

        opcion = input('Seleccione una opción: ','s');
        if isempty(opcion)
            fprintf('la opcion no puede estar vacío.');
            menu();
        end
        switch opcion
            case "1"
                ingresoUsuario();
            case "2"
                if ~isempty(datos_cliente)
                    ejecucion();
                else
                    fprintf('Primero debe ingresar los datos del cliente (opción 1).\n');
                end
            case "3"
                historial_datos();
            case "4"
                borrar_datos();
            case "5"
                fprintf('¡Gracias por visitarnos! Vuelva pronto.\n');
                break;
            otherwise
                fprintf('Opción no válida, debe ser un numero entero positivo. Intente nuevamente.\n');
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function ingresoUsuario()
    global datos_cliente;
    usuario = 0;
    while usuario ~= 1
    try
      datos_cliente.nombreu = input('Ingrese el nombre del usuario: ', 's');
      if isempty(datos_cliente.nombreu)
            error('El nombre no puede estar vacío.');

      end

        fprintf('Datos ingresados correctamente.\n');
        usuario = 1;
    catch ME
        fprintf('Error: %s\n', ME.message);
    end
end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
function ejecucion();
    global datos_cliente;
    ingresoDatos();
    ingresoplaca();
    combustible();
    cantidadlitros();
    generar_factura();

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
function ingresoDatos()
    global datos_cliente;
    dc1 = 0;
    while dc1 ~= 1 ;
    try
        datos_cliente.nombre = input('Ingrese el nombre del Cliente : ', 's');
        if isempty(datos_cliente.nombre)
            error('El nombre no puede estar vacío.');
        end
        dc1 = 1;

    catch ME
        fprintf('Error: %s\n', ME.message);
    end

    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function ingresoplaca()
    global datos_cliente;
    dc2 = 0;
    while dc2 ~= 1 ;
    try
        datos_cliente.placa = input('Ingrese la placa del carro: ', 's');
        if isempty(datos_cliente.placa)
            error('La placa no puede estar vacía.');

        end
         dc2 = 1;
        fprintf('Datos ingresados correctamente.\n');
    catch ME
        fprintf('Error: %s\n', ME.message);
    end

    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function combustible()
   global datos_cliente;
    opcion1 = "0";

    while opcion1 ~= "4"

        fprintf('\n\t\t¡Seleccione combustible!\n');
        fprintf('1. Gasolina Regular    Q 10.00 litro\n');
        fprintf('2. Gasolina Premium    Q 12.00 litro\n');
        fprintf('3. Diesel              Q  9.00 litro\n');
        opcion1 = input('Seleccione una opción: ','s');

        switch opcion1
            case "1"
                datos_cliente.combustible = 'Combustible Regular';
                opcion1 = "4" ;

            case "2"
                 datos_cliente.combustible = 'Combustible Premium';
                opcion1 = "4" ;
            case "3"
                datos_cliente.combustible = 'Diesel';
                opcion1 = "4" ;

            otherwise
                fprintf('Opción no válida. Intente nuevamente.\n');
                    opcion1 = "0";
        end
    end




end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function cantidadlitros()
      global datos_cliente;
      clt = 0;
while clt ~= 1
   try
     switch datos_cliente.combustible
            case "Combustible Regular"
                datos_cliente.precio = 10;
            case "Combustible Premium"
                datos_cliente.precio = 12;
            case "Diesel"
                datos_cliente.precio = 9;
        end

      datos_cliente.clitros = input('Ingrese cantidad de litros despachados: ');
      if ischar(datos_cliente.clitros)
        error('Datos ingresados invalidos, debe ser un numero. intente de nuevo.');
      end
      if isempty(datos_cliente.clitros)
            fprintf('La cantidad de litros no puede estar vacía.\n');
            continue;
      end

     datos_cliente.total = datos_cliente.precio * datos_cliente.clitros ;
      fprintf('El total es: Q %.2f \n',datos_cliente.total);
      clt = 1;
    catch MEx
        fprintf('Error: el dato ingresado debe ser un numero entero positivo. \n');

    end

  end



end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function generar_factura();
    global datos_cliente conn;
    try
       % tiempo_estancia = datos_cliente.salida - datos_cliente.entrada;
        %pago_total = total_pago(datos_cliente.entrada, datos_cliente.salida);

        factura = sprintf([...
            '----------------------------------------------\n', ...
            'Nombre: %s\n', ...
            'No. Placa: %s\n', ...
            'Tipo combustible %s\n', ...
            'Litros: %.2f\n', ...
            'Precio por Litro: Q %.2f\n', ...
            'Total a pagar: Q%.2f\n', ...
            'Le atendio: %s\n', ...
            '----------------------------------------------\n'], ...
            datos_cliente.nombre, datos_cliente.placa, ...
            datos_cliente.combustible, datos_cliente.clitros, datos_cliente.precio, datos_cliente.total, datos_cliente.nombreu);

        fprintf('Factura generada:\n');
        fprintf('%s\n', factura);

        % Guardar en la base de datos
        try
            query = sprintf("insert into historialfacturas values ('%s', '%s', '%s', '%.2f', '%.2f', '%.2f', '%s');", ...
                datos_cliente.nombre, datos_cliente.placa, datos_cliente.combustible, ...
                datos_cliente.clitros, datos_cliente.precio, datos_cliente.total, datos_cliente.nombreu);
            pq_exec_params(conn, query);
            disp('Factura guardada en la base de datos.');
        catch ME
            fprintf('Error al guardar en la base de datos: %s\n', ME.message);
        end

        % Guardar la factura en un archivo de texto
        archivo = 'C:\\Users\\USER\\Documents\\KJ\\PCAIE\\PRIMERPARCIAL\\facturas.txt';
        fid = fopen(archivo, 'a');
        fprintf(fid, '%s', factura);
        fclose(fid);
        fprintf('Factura guardada en "facturas.txt".\n');
    catch ME
        fprintf('Error al generar la factura: %s\n', ME.message);
    end
end

function historial_datos()
    global conn;
    try
        N = pq_exec_params(conn, "select * from historialfacturas;");
        disp('---------------------------------------------------')
        disp('Historial de datos desde la base de datos:');
        disp(N.data);
        disp('---------------------------------------------------')

    catch ME
        fprintf('Error al obtener el historial: %s\n', ME.message);
    end
end

function borrar_datos()
    global conn;
    try
        pq_exec_params(conn, "delete from historialfacturas;");
        fprintf('Todos los registros de la base de datos han sido eliminados.\n');
    catch ME
        fprintf('Error al borrar los datos de la base de datos: %s\n', ME.message);
    end
end

% Ejecutar el menú principal
menu();

% Cerrar la conexión a la base de datos al finalizar
pq_close(conn);

