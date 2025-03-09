clc;
clear;

if(exist('OCTAVE_VERSION', 'builtin')~= 0)
pkg load signal;
end
% Cargar el paquete de base de datos
pkg load database
% Definición de categorías

#IMC=0;
global datos conn;
datos = struct();
try
    % Conectar a la base de datos
    conn = pq_connect(setdbopts('dbname', 'tarea5', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'hidrogeno'));
    disp('Conexión a la base de datos establecida.');
catch ME
    error('No se pudo conectar a la base de datos: %s', ME.message);
end

% Menú principal
function menu()
opcion = "0";
while opcion ~= 6
  % Menú de opciones
  disp('Seleccione una opcion:');
  disp('1. Ingresar datos');
  disp('2. Mostrar datos');
  disp('3. Guardar');
  disp('4. Leer');
  disp('5. Borrar');
  disp('6. Salir');
  opcion = input('Ingrese su eleccion: ','s');
      if isempty(opcion)
            fprintf('la opcion no puede estar vacío.');
            menu();
      end
          switch opcion
            case "1"
                ingresodatos();
            case "2"
                mostrardatos();
            case "3"
                guardar();
            case "4"
                leer();
            case "5"
                borrar();
            case "6"
                fprintf('¡Gracias por visitarnos! Vuelva pronto.\n');
                break;
            otherwise
                fprintf('Opción no válida, debe ser un numero entero positivo. Intente nuevamente.\n');
          end
end


end
%ingreso de datos %%%%%%%%%%%%%%%%%%%%%%%
function ingresodatos()
   global datos;
    d1 = 0;
    while d1 ~= 1
      try
        datos.nombre = input('Ingrese el nombre del usuario: ', 's');
        if isempty(datos.nombre) || ~ischar(datos.nombre) || ~isempty(str2num(datos.nombre))
            error('El nombre no puede ser un número o estar vacío. Intenta de nuevo.');
        end
        d1 = 1;
        lasterror ("reset");
      catch ME
        fprintf('Error: %s\n', ME.message);
      end
    end
    while d1 ~= 2
      try
        datos.peso = input('Ingrese el peso del usuario en kilogramos: ');
        if isempty(datos.peso) || ischar(datos.peso) ||datos.peso <= 0
            error('Peso invalido. Intenta de nuevo.');

      end
        d1 = 2;
        lasterror ("reset");
      catch ME
        fprintf('Error: %s\n', ME.message);
      end
    end
    while d1 ~= 3
      try
        datos.altura = input('Ingrese la altura del usuario en metros: ');
        if isempty(datos.altura) || ~isnumeric(datos.altura) || datos.altura <= 0
            error('Altura inválida. Debe ser un número positivo. Intenta de nuevo.');
      end
        d1 = 3;
        disp('Información guardada correctamente.');
        lasterror ("reset");
        disp(' ');
      catch ME
        fprintf('Error: %s\n', ME.message);
      end
    end
 % Calcula el IMC
        datos.IMC = datos.peso / datos.altura^2;
        % Determina la categoría del IMC
        if datos.IMC < 18.5
          datos.categoria = "Bajo Peso";
        elseif datos.IMC >= 18.5 && datos.IMC < 25
          datos.categoria = "Peso Normal";
        else
          datos.categoria = "Sobre Peso";
        end

end
%mostrar datos%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function mostrardatos()
  global datos;
   % Mostrar datos del IMC
        % Muestra el valor del IMC
        fprintf('El Índice de Masa Corporal de %s es de %.2f \n', datos.nombre, datos.IMC);
        % Muestra la categoría
        fprintf('%s se encuentra en la categoría: %s \n',datos.nombre, datos.categoria);
        disp(' ');


end
%guardar datos %%%%%%%%%%%%%%%%%%%%%%%%%%%
function guardar()
 % Guardar información en un archivo txt
global datos conn;
    try
        imc = sprintf([...
            '----------------------------------------------\n', ...
            'Nombre: %s\n', ...
            'Peso: %.2f [kg]\n', ...
            'Altura: %.2f [m]\n', ...
            'Indice de Masa Corporal (IMC): %.2f \n', ...
            'Categoría: %s \n', ...
            '----------------------------------------------\n'], ...
            datos.nombre, datos.peso, ...
            datos.altura, datos.IMC, datos.categoria);

        fprintf('Documento generado:\n');
        fprintf('%s\n', imc);

        % Guardar en la base de datos
        try
            query = sprintf("insert into imc values ('%s', '%.2f', '%.2f', '%.2f', '%s');", ...
                datos.nombre, datos.peso, datos.altura, ...
                datos.IMC, datos.categoria);
            pq_exec_params(conn, query);
            disp('Datos guardados en la base de datos.');
        catch ME
            fprintf('Error al guardar en la base de datos: %s\n', ME.message);
        end

        % Guardar IMC en un archivo de texto
        datos.archivo = 'C:\\Users\\USER\\Documents\\KJ\\PCAIE\\TAREA5\\IMC.txt';
        fid = fopen(datos.archivo, 'a');
        fprintf(fid, '%s', imc);
        fclose(fid);
        fprintf('Datos guardados en "IMC.txt".\n');
    catch ME
        fprintf('Error al generar la factura: %s\n', ME.message);
    end
%%%%%%%%%%%%%%%%%%%%%
end

%leer datos %%%%%%%%%%%%%%%%%%%%%%%%%%%
function leer()
  global datos;
   % Leer los datos del archivo txt
      try
        disp('Leyendo el archivo...');
        file1 = fopen(datos.archivo, 'r');
        while ~feof(file1) % Mientras no sea el final del archivo
          linea = fgets(file1); % Leer una línea
          disp(linea); % Mostrar la línea en pantalla
        end
        fclose(file1); % Cerrar el archivo
        disp('Cerrando archivo...');
        disp(' ');
      catch
        disp('No se pudieron leer los datos del archivo. Intente de nuevo.');
      end_try_catch
end
%borrar datos %%%%%%%%%%%%%%%%%%%%%%%%%%%%
function borrar()
  % Borrar el archivo


   global datos conn;
   try
        fclose('all'); % Cierra cualquier archivo abierto
        % Intenta borrar el archivo
        if exist(datos.archivo, 'file') % Verifica si el archivo existe

        % Abrir el archivo en modo de escritura (esto borrará su contenido)
        fid = fopen(datos.archivo, 'w');

        % Cerrar el archivo
        fclose(fid);

        disp('El contenido del archivo ha sido eliminado.');
          disp(' ' );
        else
          disp('No se pudo eliminar los datos del archivo, el archivo esta vacio.');
          disp(' ');
        end
      catch
        disp('Error al intentar eliminar el archivo.');
        disp(' ');
      end_try_catch
   %borrar datos de la db
    try
        pq_exec_params(conn, "delete from imc;");
        fprintf('Todos los registros de la base de datos han sido eliminados.\n');
    catch ME
        fprintf('Error al borrar los datos de la base de datos: %s\n', ME.message);
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
menu();




