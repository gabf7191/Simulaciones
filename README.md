# SimulacionesSorter
 Simulacion analogica + visual + experimental 


Simulacion analogica: 
Toma un set de datos de envios (300.000) y va llenando cajas por destino segun lo haria un Sorter. 
El llenado de caja se hace con un volumen de referencia de la caja y cada paquete viene con su volumen aforado. 
Cada vez que se llena una caja, se escribe una linea y se vacia el volumen de la caja de ese destino.
El resultado es un CSV, que te muestra cuantas cajas llenaste para cada destino y en que hora. 

Simulacion Visual: 
Usando PyGame se simula visualmente como es el llenado de cajas con el Sorter funcionando

Simulacion experimental: 
El input del simulador en este caso es la camara de la pc en la que se este corriendo. 
La misma detectara codigos qr (del 1 al 8) y los asignara en la rampa que corresponda. 
