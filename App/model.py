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
from DISClib.ADT import queue as q
from DISClib.ADT import stack as st
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra
from DISClib.Algorithms.Graphs import prim
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

        mp.put(mapa_traduccion, id, nombre)


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


        mp.put(mapa_landing, id, (loc, mp.newMap(maptype="PROBING", loadfactor=0.3), pais))

    
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
        
            #Incersión de Vertices a Grafo con arcos:

            posOrigin = mp.get(mapa_landing, origin)["value"][0]
            posDestination = mp.get(mapa_landing, destination)["value"][0]
            costo = hs.haversine(posOrigin, posDestination)

            origin = origin + "|" + cable_name
            destination = destination + "|" + cable_name

            gr.insertVertex(grafo, origin)
            gr.insertVertex(grafo, destination)
            gr.addEdge(grafo, origin, destination, costo)
    
    idVertice1 = lt.getElement(gr.vertices(catalog["connections"]),1).split("|")[0]
    
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
    
    return idVertice1

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

def req1(catalog, lp1, lp2):

    grafo = catalog["connections"]
    landing_points = catalog["landing_points"]
    traductor = catalog["traduccion"]

    componentes = scc.KosarajuSCC(grafo)
    numComponentes = scc.sccCount(grafo, componentes, "4177|Aden-Djibouti")["components"]

    try:
        lp1 = lt.getElement(mp.get(traductor, lp1)["value"], 1)
        vertice1 = lp1 + "|" + lt.getElement(mp.keySet(mp.get(landing_points, lp1)["value"][1]),1)
    except TypeError:
        vertice1 = lp1

    try:
        lp2 = lt.getElement(mp.get(traductor, lp2)["value"], 1)
        vertice2 = lp2 + "|" + lt.getElement(mp.keySet(mp.get(landing_points, lp2)["value"][1]),1)
    except TypeError:
        vertice2 = lp2

    areConnected = scc.stronglyConnected(componentes, vertice1, vertice2)

    return numComponentes, areConnected


def req2(catalog):

    landing_points = catalog["landing_points"]
    traductor = catalog["traduccion"]

    resultado = lt.newList(datastructure= "SINGLE_LINKED")

    llaves = mp.keySet(landing_points)

    for lp in lt.iterator(llaves):

        numCables = mp.size(mp.get(landing_points, lp)["value"][1])

        if numCables > 1:

            id = lp
            nombre = mp.get(traductor, lp)["value"]
            pais = mp.get(landing_points, lp)["value"][2]

            lt.addLast(resultado, (id, nombre, pais, numCables))

    return resultado


def req3(catalog, pais1, pais2):

    mapa_paises = catalog["paises"]
    grafo = catalog["connections"]

    capital1 = lt.getElement(mp.get(mapa_paises, pais1)["value"], 1)
    capital2 = lt.getElement(mp.get(mapa_paises, pais2)["value"], 1)

    caminosMinimos = dijsktra.Dijkstra(grafo, capital1)
    costo = dijsktra.distTo(caminosMinimos, capital2)
    recorrido = dijsktra.pathTo(caminosMinimos, capital2)

    return costo, recorrido

def req4(catalog):

    grafo = catalog["connections"]

    initSearch = prim.initSearch(grafo)
    search = prim.prim(grafo, initSearch, "Washington, D.C.")
    mst = gr.newGraph(datastructure="ADJ_LIST", size= 3000, directed=False, comparefunction=compareIds)

    landing_points = mp.newMap(numelements= 1249, maptype= "PROBING", loadfactor= 0.3)    
    vertices = mp.keySet(search["marked"])
   
    for vertice in lt.iterator(vertices):

        lp = vertice.split("|")[0]
        mp.put(landing_points, lp, None)
        gr.insertVertex(mst, vertice)

    numLanding_points = mp.size(landing_points)

    listaArcos = mp.keySet(search["edgeTo"])
    pesoTotal = 0

    for verticeB in lt.iterator(listaArcos):
        
        verticeA = mp.get(search["edgeTo"], verticeB)["value"]["vertexA"]
        peso = mp.get(search["edgeTo"], verticeB)["value"]["weight"]
        gr.addEdge(mst, verticeA, verticeB, peso)

        pesoTotal+= peso

    dfsSearch = dfs.DepthFirstSearch(mst, "Washington, D.C.")
    maxArcos = 0
    arcos = None

    for vertice in lt.iterator(vertices):

        if dfs.pathTo(dfsSearch, vertice):

            numArcos = lt.size(dfs.pathTo(dfsSearch, vertice))

            if numArcos > maxArcos:

                maxArcos = numArcos
                arcos = dfs.pathTo(dfsSearch, vertice)

    return numLanding_points, pesoTotal, arcos


def req5(catalog, lp):

    grafo = catalog["connections"]
    landing_points = catalog["landing_points"]
    traductor = catalog["traduccion"]

    try:

        lp = lt.getElement(mp.get(traductor, lp)["value"], 1)

        paises = mp.newMap(numelements= 11, maptype="PROBING", loadfactor= 0.3)
        mp.put(paises, mp.get(landing_points, lp)["value"][2], None)

        cables = mp.keySet(mp.get(landing_points, lp)["value"][1])

        for cable in lt.iterator(cables):

            vertice = lp + "|" + cable
            adjacents = gr.adjacents(grafo, vertice)

            for adjacent in lt.iterator(adjacents):

                try:

                    id = adjacent.split("|")[0]
                    pais =  mp.get(landing_points, id)["value"][2]

                    mp.put(paises, pais, None)

                except TypeError: pass

    except TypeError:
        paises = mp.newMap(numelements= 11, maptype="PROBING", loadfactor= 0.3)
        adjacents = gr.adjacents(grafo, lp)

        for adjacent in lt.iterator(adjacents):

            try:

                id = adjacent.split("|")[0]
                pais =  mp.get(landing_points, id)["value"][2]

                mp.put(paises, pais, None)

            except TypeError: pass

    return paises



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