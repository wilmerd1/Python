import csv
import networkx as nx
import matplotlib.pyplot as plt
import folium
import haversine
import pandas as pd


cities = []

with open('ciudades.csv', newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')  
      next(reader)
      for row in reader:
        city = row[0]
        latitud = float(row[1])
        longitud = float(row[2])
        cities.append((city, latitud, longitud))
      print("Orden del archivo CSV")
      print(cities, "\n")

G = nx.complete_graph(len(cities))



for i in range(len(cities)):
      for j in range(i+1, len(cities)):
          city1 = cities[i]
          city2 = cities[j]
          dist = haversine.haversine((city1[1], city1[2]), (city2[1], city2[2]))
          G.add_weighted_edges_from([(i, j, dist)])
          #print(G)
          
# Calcular la ruta óptima utilizando el algoritmo TSP
route = nx.algorithms.approximation.traveling_salesman_problem(G)
print("ruta optima")
print(route,"\n")

# Ordenar las ciudades según la ruta óptima
ordered_cities = [cities[i] for i in route]
print("ruta optima Nombres")
print(ordered_cities,"\n")

# Crear un mapa centrado en la primera ciudad de la ruta óptima
mapa = folium.Map(location=[ordered_cities[0][1], ordered_cities[0][2]], zoom_start=5)


# Añadir marcadores para cada ciudad en la ruta óptima
for city in ordered_cities:
    folium.Marker(location=[city[1], city[2]]).add_to(mapa)


# Añadir una línea que conecte todas las ciudades en la ruta óptima
locations = [[city[1], city[2]] for city in ordered_cities]
folium.PolyLine(locations=locations, weight=2.5, color='blue').add_to(mapa)


# Mostrar el mapa en pantalla
mapa
print(mapa)
