#!/usr/bin/env python3

## For more details, we have attached a pdf file

import string
import math
import time
import sys

# Store all nodes
class node:
    vertex: ""      # City name
    latitude: 0
    longitude: 0

# Store all edges/ paths in graph
class edge:
    highway: ""
    city1: node
    city2: node
    distance: 0
    speed_limit: 0

node_list, vertex_list, edge_list, visited_nodes = {}, [], [], []
total_distance_in_miles, total_time_in_hours = 0, 0
graph = {}

# Cost function to calculate distance segment
def successor_segment(graph, city, cost, hN, predecessor):
    list_successors, li_predecessors = [], [city]
    neighbors = graph.get(city)
    for d in neighbors:
        for k in d.keys():
            if(k not in visited_nodes):
                list_successors.append((k, cost + 1))
    return list_successors

# Cost function to calculate distance
def successor_distance(graph, city, cost, hN, predecessor):
    list_successors = []
    neighbors = graph.get(city)
    for d in neighbors:
        for k in d.keys():
            if (k not in visited_nodes):
                list_successors.append((k, cost + int(d.get(k).distance)))
    return list_successors

# Cost function to calculate time
def successor_time(graph, city, cost,  hN, predecessor):
    list_successors = []
    neighbors = graph.get(city)
    for d in neighbors:
        for k in d.keys():
            if (k not in visited_nodes):
                list_successors.append((k, cost + (int(d.get(k).distance)/int(d.get(k).speed_limit))))
    return list_successors

# Function to print output
def print_solution(end_node):   # end_node will have (end_city, cost, time, list to store path from start city to end city)
    visited_nodes.clear()
    dist, time = 0, 0
    end_node[3].append(end_city)    # Complete path from start city to end city
    for i in range(0, len(end_node[3])-1):
        for d in graph.get(end_node[3][i]):
            for k in d.keys():
                if i+1 != len(end_node[3]) and k.upper() == end_node[3][i+1].upper():   # current and next city
                    dist += int(d.get(k).distance)                                      # Calculate distance between 2 cities
                    if (int(d.get(k).speed_limit)!=0):
                        time += (int(d.get(k).distance)/int(d.get(k).speed_limit))      # Calculate time between 2 cities

                    # Code to find the direction between 2 cities
                    direction = ''
                    if float(node_list.get(end_node[3][i + 1]).latitude) - float(node_list.get(end_node[3][i]).latitude) > 0:
                        direction = direction + 'East'
                    elif float(node_list.get(end_node[3][i + 1]).latitude) - float(node_list.get(end_node[3][i]).latitude) < 0:
                        direction = direction +  'West'
                    if float(node_list.get(end_node[3][i + 1]).longitude) - float(node_list.get(end_node[3][i]).longitude) > 0:
                        direction = direction + 'North'
                    elif float(node_list.get(end_node[3][i + 1]).longitude) - float(node_list.get(end_node[3][i]).longitude) < 0:
                        direction = direction + 'South'

                    print('From ',end_node[3][i],'head towards', direction, 'on', d.get(k).highway, ' for', int(d.get(k).distance), 'miles at', d.get(k).speed_limit, ' speed limit till you reach ',end_node[3][i+1])
                    print()


    print()
    print('Final output - ')
    print('Cost function used: ', cost_function , ' and its cost: ', end_node[1])
    print('Distance required to travel: ', dist)
    print('Time required to travel: ', time)
    str_out = ''
    for n in end_node[3]:
        str_out = str_out+ n+ " "

    # Check with uniform search cost function if output is optimals
    if(end_node[1] <= solve_Uniform(graph, start_city, end_city, cost_function, True)[1]):
        print('yes', dist, round(time,2), str_out)

    else:
        print('no', dist, round(time,2), str_out)

def find_successor_by_cost(graph, next_node, cost_function):
    if (cost_function.lower() == 'segment'):
        successors = successor_segment(graph, next_node[0], next_node[1], next_node[2], next_node[3])
    elif (cost_function.lower() == 'distance'):
        successors = successor_distance(graph, next_node[0], next_node[1], next_node[2], next_node[3])
    elif (cost_function.lower() == 'time'):
        successors = successor_time(graph, next_node[0], next_node[1], next_node[2], next_node[3])
    return successors;

# Solve using BFS
def solve_BFS(graph, start_city, end_city, cost_function):
    fringe = [(start_city,0, 0, [])]
    while len(fringe) > 0:
        next_node = fringe.pop(0)

        if next_node[0] not in visited_nodes:
            visited_nodes.append(next_node[0])
            if (end_city.lower() == next_node[0].lower()):
                print_solution(next_node)
                return True

            successors = find_successor_by_cost(graph, next_node, cost_function)

            find_predecessor = []
            if next_node[3] is None or len(next_node[3])==0:
                find_predecessor = [next_node[0]]
            else:
                find_predecessor = [x for x in next_node[3]]
                find_predecessor.append(next_node[0])
            for s in successors:
                if next_node[3] is None:
                    fringe.append((s[0], s[1], 0, find_predecessor))
                else:
                    fringe.append((s[0], s[1], 0, find_predecessor))

    return False

# Solve using DFS
def solve_DFS(graph, start_city, end_city, cost_function):
    fringe = [(start_city,0, 0, [])]
    while len(fringe) > 0:
        next_node = fringe.pop()
        if next_node[0] not in visited_nodes:
            visited_nodes.append(next_node[0])
            if (end_city.lower() == next_node[0].lower()):
                print_solution(next_node)
                return True

            successors = find_successor_by_cost(graph, next_node, cost_function)

            find_predecessor = []
            if next_node[3] is None or len(next_node[3])==0:
                find_predecessor = [next_node[0]]
            else:
                find_predecessor = [x for x in next_node[3]]
                find_predecessor.append(next_node[0])
            for s in successors:
                fringe.append((s[0], s[1], 0, find_predecessor))

    return False

# Solve using Uniform Search
def solve_Uniform(graph, start_city, end_city, cost_function, optimality_check):
    visited_nodes = []
    fringe = [(start_city,0, 0, [])]
    while len(fringe) > 0:
        next_node = min(fringe, key=lambda t: t[1])
        fringe.remove(next_node)
        if next_node[0] not in visited_nodes:
            visited_nodes.append(next_node[0])
            if (end_city.lower() == next_node[0].lower()):
                if optimality_check:
                    return next_node
                else:
                    print_solution(next_node)
                    return True

            successors = find_successor_by_cost(graph, next_node, cost_function)

            find_predecessor = []
            if next_node[3] is None or len(next_node[3])==0:
                find_predecessor = [next_node[0]]
            else:
                find_predecessor = [x for x in next_node[3]]
                find_predecessor.append(next_node[0])
            for s in successors:
                fringe.append((s[0], s[1], 0, find_predecessor))

    return False

# Solve using IDS
def solve_IDS(graph, start_city, end_city, cost_function):
    depth = 0
    while(depth<len(graph)):

        fringe = [(start_city, 0, 0, [])]
        new_depth = depth + 10
        depth = 0
        visited_nodes = []
        while(len(fringe) > 0):
            next_node = fringe.pop()
            if next_node[0] not in visited_nodes:
                visited_nodes.append(next_node[0])
                if (end_city.lower() == next_node[0].lower()):
                    print_solution(next_node)
                    return True

                successors = find_successor_by_cost(graph, next_node, cost_function)

                find_predecessor = []
                if next_node[3] is None or len(next_node[3]) == 0:
                    find_predecessor = [next_node[0]]

                else:
                    find_predecessor = [x for x in next_node[3]]
                    find_predecessor.append(next_node[0])

                for s in successors:
                    if((len(find_predecessor)) < new_depth):                # Stop once a given depth limit is reached
                        fringe.append((s[0], s[1], 0, find_predecessor))

        depth = new_depth
    return False

# https://www.movable-type.co.uk/scripts/latlong.html
def calculate_distance(lat1, long1, lat2, long2):
    # approximate radius of earth in miles
    R = 3959.0
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    long1 = math.radians(long1)
    long2 = math.radians(long2)
    dlon = long2 - long1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return round(distance, 2)


# Solve using A Star algorithm
def solve_AStar(graph, start_city, end_city, cost_function):
    hN = calculate_distance(float(node_list.get(start_city).latitude), float(node_list.get(start_city).longitude), latitude2, longitude2)
    fringe = [(start_city, 0, hN, [])]
    while len(fringe) > 0:
        next_node = min(fringe, key=lambda t: (t[1]+t[2]))
        fringe.remove(next_node)
        if next_node[0] not in visited_nodes:
            visited_nodes.append(next_node[0])
            if (end_city.lower() == next_node[0].lower()):
                print_solution(next_node)
                return True

            successors = find_successor_by_cost(graph, next_node, cost_function)

            find_predecessor = []
            if next_node[3] is None or len(next_node[3]) == 0:
                find_predecessor = [next_node[0]]
            else:
                find_predecessor = [x for x in next_node[3]]
                find_predecessor.append(next_node[0])
            for s in successors:
                hN = calculate_distance(float(node_list.get(s[0]).latitude), float(node_list.get(s[0]).longitude), latitude2, longitude2)
                fringe.append((s[0], s[1], hN, find_predecessor))

    return False


## Read file city-gps.txt and store it
## node_list will store list of all nodes with vertex as city and corresponding GPS values
## vertex_list will be used for storing all cities
with open('city-gps.txt', 'r') as file:
    for line in file:
        node1 = node()
        node1.vertex, node1.latitude, node1.longitude = [ i for i in line.split(' ')]
        node_list[node1.vertex] = node1
        vertex_list.append(node1.vertex)

## Read file city-gps.txt and store it
## If an edge has cities with no GPS co-ordinates, it will be added in nodes_without_gps list for further checking
## vertex_list and node_list are updated with new values of cities
## Graph is stored as a dictionary where key is city name and value is list of dictionary which includes neighbouring city and edge joining two cities
## For every edge connecting city1 and city2, graph will have city1 key with one of value as {city2 : edge} similarly city2 key has one of its value as {city1:edge}
with open('road-segments.txt', 'r') as file:
    nodes_without_gps = []
    for line in file:
        new_edge = edge()
        new_edge.city1, new_edge.city2, new_edge.distance, new_edge.speed_limit, new_edge.highway = [ i for i in line.split(' ')]
        if new_edge.speed_limit is not '' and new_edge.speed_limit != str(0): # skip the lines with 0 speed limit
            edge_list.append(edge)
            if new_edge.city1 not in vertex_list:
                new_node = node()
                new_node.vertex = new_edge.city1
                new_node.latitude = 0
                new_node.longitude = 0
                node_list[new_node.vertex] = new_node
                vertex_list.append(new_node.vertex)
                nodes_without_gps.append(new_node.vertex)
            if new_edge.city2 not in vertex_list:
                new_node = node()
                new_node.vertex = new_edge.city2
                new_node.latitude = 0
                new_node.longitude = 0
                node_list[new_node.vertex] = new_node
                vertex_list.append(new_node.vertex)
                nodes_without_gps.append(new_node.vertex)
            if new_edge.city1 not in graph:
                li = []
                li.append({new_edge.city2: new_edge})
                graph[new_edge.city1] = li
            else:
                li = graph.get(new_edge.city1)
                li.append({new_edge.city2: new_edge})

            if new_edge.city2 not in graph:
                li = []
                li.append({new_edge.city1: new_edge})
                graph[new_edge.city2] = li
            else:
                li = graph.get(new_edge.city2)
                li.append({new_edge.city1: new_edge})

    # For populating latitude and longitude for cities not in GPS file
    # Find the neighbouring cities of city for which there is no GPS record in file
    # and find average value from non zero GPS values of neighbours
    for city in nodes_without_gps:
        lat, long, n = 0, 0, 0
        for d in graph.get(city):
            for k in d.keys():
                if float(node_list.get(k).latitude)!=0 and float(node_list.get(k).longitude) != 0:
                    lat = lat + float(node_list.get(k).latitude)
                    long = long + float(node_list.get(k).longitude)
                    n+=1
        if n!=0:
            avg_lat = lat / n
            avg_long = long/n
        else:
            avg_lat, avg_long = 0, 0
        node_list[city].latitude = avg_lat
        node_list[city].longitude = avg_long

# Take user input
start_city = sys.argv[1]
end_city = sys.argv[2]
type = sys.argv[3]
cost_function = sys.argv[4]


# GPS values for destination node
latitude2 = float(node_list.get(end_city).latitude)
longitude2 = float(node_list.get(end_city).longitude)

# Function calls as per algorithm
if type.upper() == 'BFS':
    solution = solve_BFS(graph, start_city, end_city, cost_function)
elif type.upper() == 'DFS':
    solution = solve_DFS(graph, start_city, end_city, cost_function)
elif type.upper() == 'UNIFORM':
    solution = solve_Uniform(graph, start_city, end_city, cost_function, False)
elif type.upper() == 'IDS':
    solution = solve_IDS(graph, start_city, end_city, cost_function)
elif type.upper() == 'ASTAR':
    solution = solve_AStar(graph, start_city, end_city, cost_function)

