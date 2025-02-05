if(exist('OCTAVE_VERSION', 'builtin')~= 0)
pkg load signal;
end
t1();
function t1()
try
  while true
    % Pedir al usuario que ingrese un número
    n = input('Ingresa un número entero positivo: ');
    % Calcular el factorial usando la función calcularFactorial
    if( n < 0 || mod(n,1) != 0)
        disp('Error: El numero ingresado debe ser entero positivo. Intenta de nuevo.'); %si no es entero positivo, se encicla de nuevo
    elseif(isempty(n))
      disp('Error: no ingresaste nada. Intenta de nuevo'); %si no ingresa nada. Vuelve al ciclo

    else
        break; %si ingresa un entero positivo sale del ciclo
    end
  end

    if (n == 0 || n == 1)
        factorial = 1;

    elseif( n>1)
        factorial = 1;

        for (i = 2:n)
            factorial = factorial * i;
        end
    end

    % Mostrar el resultado
    fprintf('El factorial de %d es %d\n', n, factorial);

catch e
    % Manejar el error si el usuario ingresa un número negativo o no entero
    disp('Error: a ingresado letras. intentelo de nuevo');
    t1();
end

