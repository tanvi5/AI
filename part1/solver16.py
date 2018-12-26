#!/usr/bin/env python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
import heapq
from random import randrange, sample
import sys
import time
import string
import math
import random


# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str(row + 1))


# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col + 1))

# Heuristic to compute number of misplaced tiles
def computeHn_misplaced(state):
    count = 0
    for i in range(len(state)):
        if i != state[i - 1]:
            count += 1
    return count

# Heuristic to compute minimum number of rotations required for a tile to reach correct location
def computeHn_rotations(state):
    count = 0
    for i in range(len(state)):
        no_of_lr_moves = (abs(((i+1)%4) - (state[i]%4))>2)
        no_of_ud_moves = abs(((i+1)/4) - (state[i]/4))
        count+=((1 if(no_of_lr_moves==3) else no_of_lr_moves) + (1 if(no_of_ud_moves==3) else no_of_ud_moves) )
    return count

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j + 4)]))


# return a list of possible successor states
def successors(state):
    return [shift_row(state, i, d) for i in range(0, 4) for d in (1, -1)] + [shift_col(state, i, d) for i in range(0, 4) for d in (1, -1)]

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))


# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


# The solver! - using heapq which pops item with lowest priority
def solve(initial_board):
    # Fringe structure - (fn cost, board, path)
    # f(n) = g(n) + h(n) where g(n) is a path travelled and h(n) is a heuristic generated with combination of misplaced tiles count and minimum moves required to reach goal
    fringe = [(computeHn_rotations(initial_board)+ computeHn_misplaced(initial_board)+computeHn_rotations(initial_board), initial_board, "")]
    heapq.heapify(fringe)
    while len(fringe) > 0:
        cnt = 0
        li= []      # To store all states with lowest cost
        node = heapq.heappop(fringe)
        li.append(node)
        if len(fringe) != 0:
            node2 = heapq.heappop(fringe)
            while(node[0]==node2[0]):
                li.append(node2)
                node2 = heapq.heappop(fringe)
            heapq.heappush(fringe, node2)
        for node in li:
            (Fn, state, route_so_far) = node[0], node[1], node[2]
            if is_goal(state):
                return (route_so_far)

            for (succ, move) in successors(state):
                if visited_nodes.get(succ) is None:     # Check if node is not visited
                    heapq.heappush(fringe, (computeHn_misplaced(succ) + computeHn_rotations(succ)+len(route_so_far) + 3, succ, route_so_far + " " + move))
                    visited_nodes[succ] = len(route_so_far)+3
                elif visited_nodes.get(succ) > len(route_so_far) + 3:
                    visited_nodes[succ] = len(route_so_far) + 3
                    # if present in fringe then update its cost value
                    for (cost, node, moves) in fringe:
                        if node == succ:
                            fringe.remove((cost, node, moves))
                            heapq.heappush(fringe, (computeHn_misplaced(succ) + computeHn_rotations(succ) + len(route_so_far) + 3, succ, route_so_far + " " + move))


    return False

# test cases
start_state = []
board = sys.argv[1]
with open(board , 'r') as file:
    for line in file:
        start_state += [int(i) for i in line.split()]
if len(start_state) != 16:
    print("Error: couldn't parse start state file")
print("Start state: ")
print_board(tuple(start_state))
visited_nodes ={}
visited_nodes[tuple(start_state)] = 0
start_time = time.time()
print("Solving...")
route = solve(tuple(start_state))
end_time = time.time()
print(end_time - start_time)
print("Solution found in " + str(len(route) / 3) + " moves:" + "\n" + route)
