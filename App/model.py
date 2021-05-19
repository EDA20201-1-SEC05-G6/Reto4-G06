"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.chaininghashtable import keySet
import config as cf
import haversine as hs
from DISClib.ADT.graph import gr, vertices
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initcatalog():

    catalog = {
               "cables":None,
               "cables_landing":None,
               "landing_points":None,
               "traduccion":None,
               "paises":None,
               "connections":None,
               "components":None,
               "paths":None
                }

    catalog["cables"] = mp.newMap(maptype="PROBING", loadfactor=0.3)
    catalog["cables_landing"] = mp.newMap(maptype="PROBING", loadfactor=0.3)
    catalog["landing_points"] = mp.newMap(maptype="PROBING", loadfactor=0.3)
    catalog["traduccion"] = mp.newMap(maptype="PROBING", loadfactor=0.3)
    catalog["paises"] = mp.newMap(maptype="PROBING", loadfactor=0.3)
    catalog["connections"] = gr.newGraph(datastructure="ADJ_LIST", directed=False, size=3500, comparefunction=compareIds)

    return catalog

# Funciones para agregar informacion al catalogo
def suicidenme(catalog, landing_points, connections):
    mapa_traduccion = catalog["traduccion"]
    mapa_pais = catalog["paises"]
    mapa_landing = catalog["landing_points"]
    mapa_cables = catalog["cables"]
    mapa_cables_landing = catalog["cables_landing"]
    grafo = catalog["connections"]

    for landing_point in landing_points:
        id = landing_point["landing_point_id"]
        name = landing_point["name"]
        particion = name.split(",")
       
        nombre = particion[0]
        pais = particion[len(particion) - 1]
        if pais[0] == " ":
            pais = pais[1:]
        
        if nombre[0] == " ":
            nombre = nombre[1:]

        loc = (float(landing_point["latitude"]), float(landing_point["longitude"]))

        if not mp.contains(mapa_traduccion, nombre):
        
            mp.put(mapa_traduccion, nombre, lt.newList("SINGLE_LINKED"))
            lista = me.getValue(mp.get(mapa_traduccion, nombre))
            lt.addLast(lista, id)

        else:

            lista = me.getValue(mp.get(mapa_traduccion, nombre))
            lt.addLast(lista, id)


        if not mp.contains(mapa_pais, pais):
            mp.put(mapa_pais, pais, lt.newList(datastructure="SINGLE_LINKED"))
            lista = me.getValue(mp.get(mapa_pais, pais))
            lt.addLast(lista, lt.newList(datastructure="SINGLE_LINKED"))
            sublista = lt.getElement(lista, 1)
            lt.addLast(sublista, id)

        else:
            lista = me.getValue(mp.get(mapa_pais, pais))
            sublista = lt.getElement(lista, 1)
            lt.addLast(sublista, id)


        mp.put(mapa_landing, id, (loc, mp.newMap(maptype="PROBING", loadfactor=0.3)))

    
    for num, connection in enumerate(connections):
        if num % 2 == 0:
            origin = connection["origin"]
            destination = connection["destination"]
            cable_name = connection["cable_name"]
            capacity = float(connection["capacityTBPS"])

            mp.put(mapa_cables, cable_name, capacity)

            if not mp.contains(mapa_cables_landing, cable_name):
                mp.put(mapa_cables_landing, cable_name, mp.newMap(maptype="PROBING", loadfactor=0.3))
                mp.put(mp.get(mapa_cables_landing, cable_name)["value"], origin, None)
                mp.put(mp.get(mapa_cables_landing, cable_name)["value"], destination, None)

            else:
                mp.put(mp.get(mapa_cables_landing, cable_name)["value"], origin, None)
                mp.put(mp.get(mapa_cables_landing, cable_name)["value"], destination, None)
            
            mapa = me.getValue(mp.get(mapa_landing, origin))[1]
            mp.put(mapa, cable_name, None)
            mapa = me.getValue(mp.get(mapa_landing, destination))[1]
            mp.put(mapa, cable_name, None)
        
            #Incersión de Vertices a Grafo:

            origin = origin + "|" + cable_name
            destination = destination + "|" + cable_name

            gr.insertVertex(grafo, origin)
            gr.insertVertex(grafo, destination)

    #Creación de arcos entre vertices de un mismo cable:

    llaves = mp.keySet(mapa_cables_landing)
    
    for llave in lt.iterator(llaves):

        landingPoints = mp.keySet(mp.get(mapa_cables_landing, llave)["value"])

        for landingPoint in lt.iterator(landingPoints):

            for landingPoint1 in lt.iterator(landingPoints):

                if landingPoint != landingPoint1:

                    origen = landingPoint + "|" + llave
                    destino = landingPoint1 + "|" + llave

                    if gr.getEdge(grafo, origen, destino) == None:

                        pos1 = mp.get(mapa_landing, landingPoint)["value"][0]
                        pos2 = mp.get(mapa_landing, landingPoint1)["value"][0]
                        costo = hs.haversine(pos1, pos2)

                        gr.addEdge(grafo, origen, destino, costo)
    
    #Creación de arcos entre vertices de un mismo Landing Point:

    llaves = mp.keySet(mapa_landing)

    for llave in lt.iterator(llaves):
        
        cables = mp.keySet(mp.get(mapa_landing, llave)["value"][1])
        bwMenor = 100000000000000000000000000000000000000000000000000

        for cable in lt.iterator(cables):

            bw = mp.get(mapa_cables, cable)["value"]

            if bw < bwMenor:

                bwMenor = bw

            for cable1 in lt.iterator(cables):

                if cable != cable1:

                    origen = llave + "|" + cable
                    destino = llave + "|" + cable1

                    if gr.getEdge(grafo, origen, destino) == None:

                        gr.addEdge(grafo, origen, destino, 0.1)
        
        mp.put(mapa_cables, llave, bwMenor)

#Creación de vertices y arcos de capitales

def suicidenmeLaSecuela(catalog, countries):

    mapa_pais = catalog["paises"]
    mapa_landing = catalog["landing_points"]
    mapa_cables = catalog["cables"]
    grafo = catalog["connections"]

    for country in countries:


        pais = country["CountryName"]
        capital = country["CapitalName"]

        if country["CapitalLatitude"] != "":
            capitalPos = (float(country["CapitalLatitude"]), float(country["CapitalLongitude"]))

        if mp.contains(mapa_pais, pais):

            lt.addFirst(mp.get(mapa_pais, pais)["value"], capital)
            gr.insertVertex(grafo, capital)

            landing_points = lt.getElement(mp.get(mapa_pais, pais)["value"], 2)
            bwMenor = 10000000000000000000000000000000000000


            for landing_point in lt.iterator(landing_points):

                bw = mp.get(mapa_cables, landing_point)["value"]
                
                if bw < bwMenor:
                    
                    bwMenor = bw
                
                cables = mp.keySet(mp.get(mapa_landing, landing_point)["value"][1])
                pos = mp.get(mapa_landing, landing_point)["value"][0]

                for cable in lt.iterator(cables):

                    destino = landing_point + "|" + cable
                    costo = hs.haversine(capitalPos, pos)

                    gr.addEdge(grafo, capital, destino, costo)

            mp.put(mapa_cables, capital, bwMenor) 

        elif pais != "":

            mp.put(mapa_pais, pais, lt.newList(datastructure="SINGLE_LINKED"))
            lt.addFirst(mp.get(mapa_pais, pais)["value"], capital)
            gr.insertVertex(grafo, capital)

            llaves = mp.keySet(mapa_landing)
            distanciaMin = 1000000000000000000000000000000000000000000000000
            landing_point = None

            for llave in lt.iterator(llaves):

                pos = mp.get(mapa_landing, llave)["value"][0]
                costo = hs.haversine(capitalPos, pos)

                if costo < distanciaMin:

                    distanciaMin = costo
                    landing_point = llave 


            cables = mp.keySet(mp.get(mapa_landing, landing_point)["value"][1])
            bw = mp.get(mapa_cables, landing_point)["value"]

            for cable in lt.iterator(cables):

                destino = landing_point + "|" + cable

                gr.addEdge(grafo, capital, destino, distanciaMin)
            
            mp.put(mapa_cables, capital, bw)

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de Comparacion

def compareIds(llave, vertice):
    """
    Compara dos estaciones
    """
    llave2 = vertice['key']
    if (llave == llave2):
        return 0
    elif (llave > llave2):
        return 1
    else:
        return -1