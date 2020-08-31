#! /usr/bin/env python3

import random, sys

class Tree :
	def __init__(self, value, parent, children) :
		self.value = value
		self.parent = parent
		self.children = children

	def __str__(self) :
		s = str(self.value)
		for child in self.children:
	  		s = s + str(child)
		return s
	
	def __eq__(self,obj) :
		if(not hasattr(obj,'value')):
			return False
		return self.value == obj.value

visited = []
actual = Tree((0,0), Tree(None,None,[(0,0)]),[]) 	# creates the initial node, 
													# value equals (0,0) and 
													# parent equals a empty Tree

def depth_first(lista):
	global actual
	global visited
	visited.append(actual.value)
	for neighbor in lista: 							# generate the children
		if((neighbor not in visited) and 			# if a neighbor has already visited, ignore it
		(neighbor not in actual.children) and 		# in case of regression, a neighbor can be one of the children
		(neighbor != actual.parent.value)) :		# cannot compute parent as one child
			new_child = Tree(neighbor,actual,[])
			actual.children.append(new_child)
	
	if(actual.children) : 							# if has children
		actual = actual.children[0] 				# go to the left child
	else : 											# if has not
		actual.parent.children.remove(actual) 		# do regression: remove the actual node
		actual = actual.parent 						# and go to the parent node

	return actual.value

def algoritmo(posic, lista):
	return depth_first(lista)