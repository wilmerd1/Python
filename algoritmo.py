import csv
# import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import haversine

cities = []

with open('ciudades.csv', newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')  

      for row in reader:
      #   print(', '.join(row))

      # for row in reader:
      #       city = {row[0], float(row[1]), float(row[2])}
      #       cities.append(city)


# print(cities)

# df = pd.read_csv('D:\OneDrive - Pontificia Universidad Javeriana\Informacion\Documents\coder\Viajero\ciudades.csv') 


# Crear un grafo completo con todas las ciudades
G = nx.complete_graph(len(cities))

# Calcular las distancias entre todas las ciudades utilizando la fórmula de Haversine
for i in range(len(cities)):
      for j in range(i+1, len(cities)):
          city1 = cities[i]
          city2 = cities[j]
          dist = haversine(city1['latitud'], city1['longitud'], city2['latitud'], city2['longitud'])
          G[i][j]['weight'] = dist

# Calcular la ruta óptima utilizando el algoritmo TSP
route = nx.algorithms.approximation.traveling_salesman_problem.traveling_salesman_problem(G)

# Ordenar las ciudades según la ruta óptima
ordered_cities = [cities[i] for i in route]

# Crear un mapa centrado en la primera ciudad de la ruta óptima
m = folium.Map(location=[ordered_cities[0]['latitud'], ordered_cities[0]['longitud']], zoom_start=6)

# Añadir marcadores para cada ciudad en la ruta óptima
for i in range(len(ordered_cities)):
      city = ordered_cities[i]
      folium.Marker(location=[city['latitud'], city['longitud']], popup=city['nombre']).add_to(m)

# Añadir una línea que conecte todas las ciudades en la ruta óptima
locations = [(city['latitud'], city['longitud']) for city in ordered_cities]
folium.PolyLine(locations=locations, color='blue').add_to(m)

# Mostrar el mapa en pantalla
m