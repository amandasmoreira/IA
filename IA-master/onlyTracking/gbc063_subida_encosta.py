#! /usr/bin/env python3
# distance function developt in the last exercise
import numpy as np


start = (0,0)					# the initial position
end = (10,10)					# objective position to calculate distance from.
								# This could be altered to get the positions non-hard-coded from run_labirinto.py
								# width and height of the maze, doing it a global object
def minkowsky_distance(X,Y, r):
  '''Calculate minkowsky distance
      of two points
      
      #Arguments
        X (tuple): the first point object to calculate distance of;
        Y (tuple): the second point object to calculate distance of;
		r (integer): the norm of minkowsky formula;
      #Returns
        minkowsky_distance (float): the minkowsky distance of the objects.
  '''
  #transform to np.ndarray if is not
  y = np.array(Y)
  x = X
  minkowsky_distance = np.power(np.sum(np.power(np.abs(x-y),r)),1/r)
  return minkowsky_distance
def manhattan_distance(X,Y):
	'''Calculate manhattan distance
      of a point and an array of points
      
      #Arguments
        X (tuple): the point object to calculate distance of;
        Y (np.ndarray or list): the vector object to calculate distance of.
      #Returns
        euclidian_distance (float): the euclidian distance of the objects.
  	'''
	distances = []
	for point in Y :
		distances.append(minkowsky_distance(X,point,1))
	return distances

actual_distance = manhattan_distance(end,[start])[0]
def algoritmo(posic, lista):
	global actual_distance
	distances = manhattan_distance(end,lista)
	pos_minimal_distance = np.argmin(distances)
	minimal_distance = distances[pos_minimal_distance]
	if(minimal_distance < actual_distance):
		actual_distance = minimal_distance
		return lista[pos_minimal_distance]
	return posic