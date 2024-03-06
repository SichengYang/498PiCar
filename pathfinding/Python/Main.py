from Graph import Map
from module import Dijkstra
#Ger the cost matrix from a file
temp_map=Map('python\Map.txt')
#Print cost matrix and vertex
print(temp_map.vertex)
print(temp_map.vertex)
#Still Have BUGS, FIXING...
dj=Dijkstra(temp_map.vertex,temp_map.vertex,'1')
result = dj.find_shortestPath('6')
print(result)