
#Programacion tradicional
#Determinar promedio semanal del clima de una ciudad

#Definicion de variables globales

dias= ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
temperaturas=[] #se define una lista vacia para almacenar las temperaturas diarias
suma_temperaturas=0 #variable para almacenar la suma de las temperaturas
promedio_semanal=0  #variable para almacenar el promedio semanal


#Funcion para capturar las temperaturas diarias
def capturar_temperaturas():
    for dia in dias:
        temp=float(input(f"Ingrese la temperatura del {dia}: ")) #se captura la temperatura diaria
        temperaturas.append(temp) #se agrega la temperatura a la lista

#Funcion para calcular el promedio semanal
def calcular_promedio():
    global suma_temperaturas, promedio_semanal
    for temp in temperaturas:
        suma_temperaturas += temp #se suma cada temperatura a la variable suma_temperaturas
    promedio_semanal = suma_temperaturas / len(temperaturas) #se calcula el promedio dividiendo la suma entre el numero de dias

#Funcion para mostrar el promedio semanal
def mostrar_promedio():
    print(f"El promedio semanal de temperaturas es: {promedio_semanal:.2f} grados centígrados.") #se muestra el promedio con dos decimales

#Uso de las funciones

capturar_temperaturas() #llamada a la funcion para capturar temperaturas
calcular_promedio()     #llamada a la funcion para calcular el promedio
mostrar_promedio()      #llamada a la funcion para mostrar el promedio



