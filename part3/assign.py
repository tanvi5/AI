#!/usr/bin/env python2
"""

Kindly go through README pdf first 

"""

from __future__ import division
import time
import math
from Queue import PriorityQueue as pq
import sys


'''
This function is used to divide class of students into mutiple subsets 
If the numbers of students > 55
Here we try to consider preferences of all students being added in a subset, so that the cost can be reduced 
'''
def divide_data_in_sets():
    no_of_sets = math.ceil(len(data) / 55)
    size_of_set = math.ceil(len(data) / no_of_sets)
    nodes_in_sets = []				#list is used to keep track of students who have been added to subsets
    for student in data:			#used to add only one student in set
        sets.append({student:data[student]})
        nodes_in_sets.append(student)
        break
    
    index = 0					#index denotes the subset number
    while len(nodes_in_sets) < len(data):	#data is dictionary having preferences of all students
        for student in sets[index].keys():	
            if len(sets[index]) > size_of_set and data[student][1] != '_':
                sets.append({})			#create a new subset if size of previous set is exceeding limit
                index+=1
                for partner in data[student][1].split(','):#here we add all students which are mentioned in current student's preferred list in current group
                    if partner not in nodes_in_sets:
                        sets[index][partner] = data[partner] 
                        nodes_in_sets.append(partner)
            elif data[student][1] != '_' :
                for partner in data[student][1].split(','):#here we add all students which are mentioned in current student's preferred list in current group
                    if partner not in nodes_in_sets:
                        sets[index][partner] = data[partner] 
                        nodes_in_sets.append(partner)
	#if the control comes out of above for loop and there are still students not assigned to a subset, then following for loop takes care of such conditions
        if len(nodes_in_sets) < len(data):
	    for student in data:
        	if student not in nodes_in_sets:	#search for a student who is not added in any subset
                    sets[index][student] = data[student]
	            nodes_in_sets.append(student)
        	    break


#A successor will have 1 group which will combine any two groups from parent, and remaining groups will be kept as they are
def successors(state):
    new_groups = []
    for i in range(len(state)):				#select a group - grp1
        for j in range(i+1,len(state)):			#select a group - grp2
            if len(state[i]+state[j])<4 :		#ensure if combination of grp1 and grp2 will result in a group size < 4
		#merge grp1 and grp2
                new_group = [state[x] for x in range(i)]+[state[i]+state[j]]+[state[y] for y in range(i+1,len(state)) if state[y]!=state[j]]
                if new_group not in groups_explored:
                    groups_explored.append(new_group)
                    new_groups.append(new_group)
                              
    return new_groups
    
#find cost using the rules provided in question
def cost(state):
    cost = len(state)*k					#total grading time is k times number of teams.
    for group in state:
        for student in group:
            if len(group) != data[student][0] and data[student][0] != 0:
                cost+=1					#1 min if group size not satisfied
            if data[student][1] != '_':			#if preference list given
                for requested_partner in data[student][1].split(","):	  #for each student in prefernce list
                    if requested_partner not in group:	#if student in prefernce list is not in group
                        cost+=n				#then 'n' minutes will be added to cost
            
            if data[student][2] != '_':            	#for each student in enemy list
                for requested_not_partner in data[student][2].split(","):
                    if requested_not_partner in group:	#if enemy present in group
                        cost+=m				#m minutes for each meetings 
    return cost
                    
    
def solve(initial_group):
    fringe = pq()
    fringe.put((cost(initial_group),initial_group))
    setOfStates.append((initial_group,cost(initial_group)))
    while not fringe.empty():
        (currentCost, state) = fringe.get()
        
        for succ in successors( state ): 
            succCost = cost(succ)
            
            if min(setOfStates, key=lambda tup: tup[1])[1] > succCost:	#consider combination only when cost is lesser minimum of all states visited till now
                fringe.put((succCost, succ) )
                setOfStates.append((succ, succCost))
                    
                    
    
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

fo = open(sys.argv[1], "r") 
data = {}
rows = fo.read().split('\n')

for row in rows:
    student_data = row.split(" ")
    data[student_data[0]] = [int(student_data[1]),student_data[2],student_data[3]]
fo.close()    
sets = []
#start_time = time.time()     

if len(data)>55:
    divide_data_in_sets()
else:
    sets = [data]

total_cost = 0
final_groups = []  

for aset in sets:
    setOfStates = []
    initial_state = [[student_id] for student_id in aset.keys()]
    groups_explored = [initial_state]
    solve(initial_state)
    total_cost += min(setOfStates, key=lambda tup: tup[-1])[1]
    final_groups += min(setOfStates, key=lambda tup: tup[-1])[0]	#merge all groups to find final combination

if len(sets) > 1:    
    setOfStates = []    						#if there were subsets merged
    initial_state = final_groups
    groups_explored = [final_groups]
    solve(initial_state)						#try to see if there is more optimal solution in successors

final_groups,total_cost = min(setOfStates, key=lambda tup: tup[-1])


#end_time = time.time()
#print end_time - start_time

#print output in required fashion
for group in final_groups:
	student_string = ''
	for student in group:
		student_string+=(student+' ')
	print student_string
	
print total_cost


