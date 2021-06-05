"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.ADT import queue as q
from DISClib.ADT import stack as st
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar la cantidad de clústeres dentro de la red y consultar si 2 landing points pertenecen o no a un mismo clúster")
    print("3- Encontrar los landing points que sirven como puntos de interconexión a más cables en la red")
    print("4- Encontrar la ruta mínima en distancia para enviar información entre dos países (entre las capitales)")
    print("5- Encontrar la red de expansión mínima con mayor cobertura")
    print("6- Consultar el impacto que tendría el fallo de un landing point determinado")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        resultado = controller.loadCatalog(catalog)
        catalog = resultado[0]

        numLandingPoints = mp.size(catalog["landing_points"])
        numConexiones = gr.numEdges(catalog["connections"])
        numPaises = mp.size(catalog["paises"])
        idVertice1 = resultado[1]
        nombreVertice1 = mp.get(catalog["traduccion"], idVertice1)["value"]
        latitud = mp.get(catalog["landing_points"], idVertice1)["value"][0][0]
        longitud = mp.get(catalog["landing_points"], idVertice1)["value"][0][1]


        print("Total de Landing Points: " + str(numLandingPoints))
        print("Total de conexiones entre Landing Points: " + str(numConexiones))
        print("Total de paises: " + str(numPaises ) + "\n")
        print("Informacion del primer Landing Point cargado: ")
        print("ID: " + idVertice1)
        print("Nombre: " + nombreVertice1)
        print("Latitud: " + str(latitud))
        print("Longitud: " + str(longitud))

    elif int(inputs[0]) == 2:

        lp1 = input("Ingrese el nombre del primer landing point: ")
        lp2 = input("Ingrese el nombre del segundo landing point: ")

        resultado = controller.req1(catalog, lp1, lp2)

        print("El número de componentes conectados del grafo es " + str(resultado[0]))

        if resultado[1]:
            print("Los dos landing points consultados se encuentran en el mismo componente conectado.")

        else:
            print("Los dos landing points consultados no se encuentran en el mismo componente conectado.\n") 


    elif int(inputs[0]) == 3:

        resultado = controller.req2(catalog)

        for elemento in lt.iterator(resultado):

            print("Nombre del landing point: " + elemento[1])
            print("ID: " + elemento[0])
            print("País en el que se encuentra: " + elemento[2])
            print("Número de cables a los que está conectado: " + str(elemento[3]) + "\n\n")

    elif int(inputs[0]) == 4:

        pais1 = input("Ingrese el primer país: ")
        pais2 = input("Ingrese el segundo país: ")

        resultado = controller.req3(catalog, pais1, pais2)

        print("El recorrido es de " + str(resultado[0]) + " Km.")
        print("El recorrido se realiza en los siguientes pasos:\n")

        for arco in lt.iterator(resultado[1]):
            print(arco["vertexA"] + " - " + arco["vertexB"] + ": " + str(arco["weight"]) + " Km.")

    elif int(inputs[0]) == 5:
        
        resultado = controller.req4(catalog)

        print("Número de nodos incluidos en el arbol de expansión mínima: " + str(resultado[0]))
        print("El peso de todos los arcos del arbol es: " + str(resultado[1]))
        print("La ruta más larga es: ")

        for vertice in lt.iterator(resultado[2]):
            print(vertice)

    elif int(inputs[0]) == 6: 

        lp = input("Ingrese el landing point que desea consultar: ")

        resultado = controller.req5(catalog, lp)
        paises = mp.keySet(resultado)

        print("El número de paises afectados en caso de que el landing point consultado se dañase es " + str(mp.size(resultado)))

        for pais in lt.iterator(paises):
            print(pais)


    else:
        sys.exit(0)

sys.exit(0)
