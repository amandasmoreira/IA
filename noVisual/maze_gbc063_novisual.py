#! /usr/bin/env python3

'''
Random Maze Generator
Makes use of a radomized version of Kruskal's Minimum Spanning Tree (MST) 
algorithm to generate a randomized mazes!
	@author: Paul Miller (github.com/138paulmiller)
'''

import os, sys, random, time, threading
# defined in disjointSet.py
import disjointSet as ds

class Maze:

	def __init__(self, width, height, seed):
		
		assert width > 0; assert height > 0
		self.count = 0
		self.width = width
		self.height = height
		self.seed = seed
		self.path = [] # current path taken
		self.player = (0,0) # players position
		
		self.grid = [[(width*row + col) \
			for row in range(0,height)]\
				for col in range(0, width)]
		# portals[key] = {keys of neighbors}
		self.portals = {}
		# generate the maze by using a kruskals algorithm 
		self.kruskalize()	
	

	
	def kruskalize(self):
		# edge = ((row1, col1), (row2, col2)) such that grid[row][col] = key
		edges_ordered = [ ]
		# First add all neighboring edges into a list
		for row in range(0, self.height):
			for col in range(0, self.width):	
				cell = (col, row)
				left_cell = (col-1, row)
				down_cell = (col, row-1)
				near = []
				if col > 0:
					near.append((left_cell, cell))
				if row > 0:
					near.append( (down_cell, cell))
				edges_ordered.extend(near)	
		# seed the random value
		random.seed(self.seed)
		edges = []
		# shuffle the ordered edges randomly into a new list 
		while len(edges_ordered) > 0:			
			# randomly pop an edge
			edges.append(edges_ordered.pop(random.randint(0,len(edges_ordered))-1))
		disjoint_set = ds.DisjointSet()
		for row in range(0, self.height):
			for col  in range(0,self.width):
				# the key is the cells unique id
				key = self.grid[col][row]
				# create the singleton 
				disjoint_set.make_set(key)
				# intialize the keys portal dict
				self.portals[key] = {}
		edge_count = 0
		# eulers formula e = v-1, so the
		# minimum required edges is v for a connected graph!
		# each cell is identified by its key, and each key is a vertex on the MST
		key_count = self.grid[self.width-1][self.height-1] # last key	
		while edge_count < key_count:
			# get next edge ((row1, col1), (row2,col2))
			edge = edges.pop()
			# get the sets for each vertex in the edge
			key_a = self.grid[edge[0][0]][edge[0][1]]
			key_b = self.grid[edge[1][0]][edge[1][1]]
			set_a = disjoint_set.find(key_a)
			set_b = disjoint_set.find(key_b)
			# if they are not in the same set they are not in the 
			# same region in the maze
			if set_a != set_b:
				# add the portal between the cells, 
				# graph is undirected and will search
				# [a][b] or [b][a]
				edge_count+=1	
				self.portals[key_a][key_b] = True 
				self.portals[key_b][key_a] = True 
				disjoint_set.union(set_a, set_b)
			# criado portais adicionais (10%) 	1+ caminhos
			elif random.randint(0,10) > 9:
				#edge_count+=1	
				self.portals[key_a][key_b] = True 
				self.portals[key_b][key_a] = True 
				disjoint_set.union(set_a, set_b)
				

	def move(self, direction):
		new_move = direction
		valid = False
		# if new move is not within grid
		if new_move[0] < 0 or new_move[0] >= self.width or\
			new_move[1] < 0 or new_move[1] >= self.height:
			# inserido
			player = (self.player[0] , self.player[1] )
			player_key = self.width*self.player[1] + self.player[0]
			lista_return = []
			lista_return.append(valid)
			lista_return.append(player)
			l = []
			for posit in self.portals[player_key]:
				output = (posit%self.width , posit//self.width)
				l.append(output)
			lista_return.append(l)
			# inserido
			return lista_return    # originalmente return valid
		player_key = self.width*self.player[1] + self.player[0]
		move_key = self.width*new_move[1] + new_move[0]	
 		#if theres a portal between player and newmove
		if move_key in self.portals[player_key]:
			self.is_moving = True
			# if new move is backtracking to last move then sets player pos to top of path and remove path top
			if len(self.path) > 0 and new_move == self.path[-1]:
				# move cursor to player and color tail, move cursor to player and color empty
				self.player = self.path.pop()
			# else move progresses path, draws forward and adds move to path
			else:
				self.path.append(self.player)
				self.player = new_move
				#move cursor to position to draw if ANSI		
				valid = True # successfully moved forward between portals
			# adicionado
			lista_return = []
			lista_return.append(valid)
			player = (self.player[0] , self.player[1] )
			player_key = self.width*self.player[1] + self.player[0]
			lista_return.append(player)
		#	print(len(self.portals[player_key]))	
			l = []
			for posit in self.portals[player_key]:
				output = (posit%self.width , posit//self.width)
				l.append(output)
			lista_return.append(l)
			# adicionado
			self.is_moving = False
		# adicionado	
		lista_return = []
		lista_return.append(valid)
		player = (self.player[0] , self.player[1] )
		player_key = self.width*self.player[1] + self.player[0]
		lista_return.append(player)	
		l = []
		for posit in self.portals[player_key]:
			output = (posit%self.width , posit//self.width)
			l.append(output)
		lista_return.append(l)
		
		return lista_return
	
	def is_done(self):
		return self.player == (self.width-1, self.height-1)
