#! /usr/bin/env python3

import random, sys

class Tree :
	def __init__(self, value, parent, children) :
		self.value = value
		self.parent = parent
		self.children = children
		if(self.parent):
			self.depth = self.parent.depth + 1
		else:
			self.depth = 0

	def __str__(self) :
		s = str(self.value)
		for child in self.children:
	  		s = s + str(child)
		return s
	
	def __eq__(self,obj) :
		if(not hasattr(obj,'value')):
			return False
		return self.value == obj.value

depth_limit = 0
visited = []
actual = Tree((0,0), Tree(None,None,[(0,0)]),[]) 	# creates the initial node, 
													# value equals (0,0) and 
													# parent equals a empty Tree

def depth_first_limited(lista):
	global actual
	global visited
	visited.append(actual.value)
	for neighbor in lista: 							# generate the children
		if((neighbor not in visited) and 			# if a neighbor has already visited, ignore it
		(neighbor not in actual.children) and 		# in case of regression, a neighbor can be one of the children
		(neighbor != actual.parent.value)) :		# cannot compute parent as one child
			new_child = Tree(neighbor,actual,[])
			actual.children.append(new_child)
	
	if(actual.children and actual.depth < depth_limit) : # if has children and the depth limit was'nt overcome
		actual = actual.children[0] 						# go to the left child
	else : 													# if has not
		if(not actual.parent.value):								
			return None										# regressed to the root. None movement could be done
		actual.parent.children.remove(actual) 				# do regression: remove the actual node
		actual = actual.parent 								# and go to the parent node

	return actual.value

def algoritmo(_, lista):
	global depth_limit
	global visited
	global actual
	move = None
	while (not move):						# while a movement coudn't be done
		move = depth_first_limited(lista)	# try again
		if(not move):
			visited = []											#
			actual = Tree((0,0), Tree(None,None,[(0,0)]),[]) 		# restart global variables
			depth_limit = depth_limit + 1							# increase depth_limit
	return move