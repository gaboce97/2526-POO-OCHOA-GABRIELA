
Programación Tradicional vs POO

En el ejemplo de cálculo del promedio semanal de temperaturas, podemos observar las diferencias entre 
la programación tradicional y la programación orientada a objetos (POO) en términos de los cuatro pilares
fundamentales: abstracción, encapsulamiento, herencia y polimorfismo.

Si vemos el ejemplo de progrmamación tradicional, el código se organiza en funciones y procedimientos que operan sobre datos
globales. No hay una estructura clara que agrupe los datos y las funciones relacionadas, lo que puede llevar a un código 
menos modular y más difícil de mantener.

En contraste, en el ejemplo de POO, podemos observar cómo se aplican los principios de la POO:


- la abstracción se usa al definir la clase ClimaSemanal que encapsula todos los datos y métodos relacionados
con el cálculo del promedio semanal de temperaturas. Los detalles internos de cómo se capturan, calculan y
 muestran las temperaturas están ocultos dentro de la clase, proporcionando una interfaz clara para interactuar con ella.

- El encapsulamiento se observa en el uso de atributos y métodos dentro de la clase ClimaSemanal.
 Los atributos como dias, temperaturas, suma_temperaturas y promedio_semanal están encapsulados dentro de la clase,
 y solo se accede a ellos a través de los métodos definidos (capturar_temperaturas, calcular_promedio, mostrar_promedio).
 Esto protege los datos internos y asegura que solo se modifiquen de manera controlada a través de los métodos de la clase.

- La herencia no se aplica en este ejemplo específico, ya que no hay clases derivadas que extiendan la funcionalidad de ClimaSemanal.

- El polimorfismo tampoco se ilustra en este ejemplo, ya que no hay múltiples clases con métodos que compartan el mismo nombre pero se comporten de manera diferente.