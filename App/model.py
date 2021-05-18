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


import config as cf
import haversine as hs
from DISClib.ADT.graph import gr
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
        
        mp.put(mapa_traduccion, id, nombre)

        if not mp.contains(mapa_pais, pais):
            mp.put(mapa_pais, pais, lt.newList(datastructure="ARRAY_LIST"))
            lista = me.getValue(mp.get(mapa_pais, pais))
            lt.addLast(lista, lt.newList(datastructure="ARRAY_LIST"))
            sublista = lt.getElement(lista, 1)
            lt.addLast(sublista, nombre)

        else:
            lista = me.getValue(mp.get(mapa_pais, pais))
            sublista = lt.getElement(lista, 1)
            lt.addLast(sublista, nombre)

        if not mp.contains(mapa_landing, nombre):
            mp.put(mapa_landing, nombre, (loc, mp.newMap(maptype="PROBING", loadfactor=0.3)))
    
    for num, connection in enumerate(connections):
        if num % 2 == 0:
            origin = connection["origin"]
            destination = connection["destination"]
            origin = me.getValue(mp.get(mapa_traduccion, origin))
            destination = me.getValue(mp.get(mapa_traduccion, destination))
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
            mp.put(mapa, cable_name)
            mapa = me.getValue(mp.get(mapa_landing, destination))[1]
            mp.put(mapa, cable_name)
#TODO REVISAR QUE MAPA_LANDING ESTÉ BIEN
#TODO HACER GRAFO (INCLUYENDO TRASBORDOS)
#TODO HACER CONEXIONES CAPITALES
#TODO HACER ASOCIACION ANCHOS DE BANDA-CAPITALES Y TRASBORDOS

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