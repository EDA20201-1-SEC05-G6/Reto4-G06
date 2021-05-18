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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def loadCatalog(catalog):

    catalog = model.initcatalog()

    connections0 = cf.data_dir + "connections.csv"
    connections = csv.DictReader(open(connections0, encoding="utf-8-sig"),
                                delimiter=",")
    
    landing_points0 = cf.data_dir + "landing_points.csv"
    landing_points = csv.DictReader(open(landing_points0, encoding="utf-8"),
                                delimiter=",")

    countries0 = cf.data_dir + "countries.csv"
    countries = csv.DictReader(open(countries0, encoding="utf-8"),
                                delimiter=",")

    model.suicidenme(catalog, landing_points, connections)

    return catalog

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
