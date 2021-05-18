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
        catalog = controller.loadCatalog(catalog)

    elif int(inputs[0]) == 2: pass

    elif int(inputs[0]) == 3: pass

    elif int(inputs[0]) == 4: pass

    elif int(inputs[0]) == 5: pass

    elif int(inputs[0]) == 6: pass

    else:
        sys.exit(0)
sys.exit(0)
