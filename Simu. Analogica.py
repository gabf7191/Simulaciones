import pandas as pd
import os
import csv

# Selecciono el directorio donde tengo los archivos
os.chdir("C:/Users/gbalonga/Desktop/sim")

# --------------------------------Constantes para cambiar-------------------------------------
Aprovechamiento = 1  # % de aprovechamiento de cada caja
Tamano_Caja =  120# K de tamano de caja (800x400x450 = 144 lt * Conicidad *Kexterno-interno (0,85) = 120lt)
Velocidad_Vieja = 1500
Velocidad_Nueva = 7000
Ratio = Velocidad_Vieja / Velocidad_Nueva  # Ratio para pasar el LOG actual a la velocidad del sorter nuevo
# --------------------------------------------------------------------------------------------

# donde n es el numero de salida y Espacio(n) es la cantidad de espacio usado en la caja
Espacio = []
# donde n es el numero de salida y Peso(n) es el peso dentro de la caja
Peso = []
# Donde n es el numero de salida y Inicio(n) es el momento en el que se pone el primer paquete
Tiempo = []
# Diccionario donde n es el numero de salida y salida(n) es el nombre del lugar
Salida = []
# Cantidad de cajas por destino, donde n es el destino
Cajas = []
# Cantidad de paquetes por caja
Paquetes = []

# Les doy el tamaño del total de salidas
for n in range(160):
    Espacio.append(0)
    Tiempo.append(0)
    Cajas.append(0)
    Paquetes.append(0)
    Peso.append(0)

n = 0


# ---Completo el Tuple Salida[n] con la info de Sucursales.csv
with open('Sucursales.csv', 'r', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter='\n')
    for row in reader:
        #print(row)
        data = ', '.join(row) #La funcion join une todos los elementos de una lista ", " es el separador de lo que estamos uniendo
        #print(data)
        Salida.append(data)

# ---

df2 = pd.DataFrame(columns=["Ncaja","Vol Ocupado", "Peso" ,"Cant paquetes" ,"comienzo", "fin", "destino"])  #df2 es el dataframe de salida donde estara cada caja identificada (tipo Alertran)
df = pd.read_csv("2611M.csv" ,sep=";",decimal=",")                                                    #df es el LOG del Sorter actual. TODOS LOS ENVIOS QUE PASAN POR LA CIT
#print(Salida[97])

#---------------------------------------------ARRANCA EL PROGRAMA---------------------------------------------------


for index, row in df.iterrows():
    n = 0  # n es el numero de salida que matchea numero de salida y lugar del envio
    # Match entre numero de salida y nombre de columna envios

    print(row["ENVIO"])
    while Salida[n] != row["DESTINO"]:
        n = n + 1
        #if n > 1: #DEBUGGER POR SI ALGO ANDA MAL
            #print(row["ENVIO"])
             #print(row["DESTINO"])
             #   print (n)
    Peso[n] = Peso[n] + row["PESO [G]"]
    Espacio[n] = Espacio[n] + row["VOL. [L]"]  # Sumo el volumen de ese envio
    Paquetes[n] = Paquetes[n] + 1

    if Espacio[n] > Tamano_Caja:      # Me fijo si el ultimo envio hizo que se supere el volumen maximo de la caja

        Cajas[n] = Cajas[n] + 1
        Comienzo = Tiempo[n] #Tomo el ultimo tiempo tomado, como el comienzo de la caja que estoy cerrando
        fin = row['HORA'] #Tomo la hora actual como el fin de la caja "n"
        Volumenguardado = Espacio[n]-row["VOL. [L]"] #La caja n se cierra sin el paquete que corresponde al row actual
        Pesoguardado = Peso[n]  - row["PESO [G]"]
        CantPaquetes = Paquetes[n] -1
        df2 = df2.append(pd.Series([Cajas[n],Volumenguardado, Pesoguardado, CantPaquetes ,Comienzo, fin, Salida[n]], index=df2.columns), ignore_index=True) #Escribo la linea de la caja cerrada
        Espacio[n] = row["VOL. [L]"]  #Agrego el volumen a la caja nueva
        Peso[n]= row["PESO [G]"]
        Tiempo[n] = row['HORA'] #Guardo la hora de comienzo de la nueva caja
        Paquetes[n] = 1
        #print(Tiempo[n])

Sum = 0
for i in range (144):
    Sum = Sum + Paquetes[i]
print(Sum)

#print(df2.groupby('destino').count())

print(df2)

df2["Peso"] = df2["Peso"]/1000
df2["Densidad"]= df2["Peso"]/df2["Vol Ocupado"]
df2["Densidad con aire"] = df2["Peso"]/Tamano_Caja
df2["Diferencia %"] = ((df2["Densidad"]/df2["Densidad con aire"] )-1 )* 100

#df["Tiempo de llenado"] = df2["fin"]-df2["comienzo"]

df2.to_csv("RESULTADO.csv",sep=";",decimal=",")

