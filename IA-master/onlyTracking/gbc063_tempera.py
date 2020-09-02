#! /usr/bin/env python3

import random, sys
# ALGORITMO: Tempera simulada

import math
import random

# Heuristica: h
def h(position, target):
    # Distância de Manhattan
    y = abs(position[0] - target[0])
    x = abs(position[1] - target[1])
    h = x + y
    return h

temperatura = 1
final = (10,10)

def exp_prog(k=20, lam=0.005, limit=100):
    #Uma possível função de programação para tempera
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)


def tempera_Simulada(atual, vizinho, prog=exp_prog()):
	global temperatura
	T = prog(temperatura)
	temperatura +=1
	if T == 0:
		return atual
	if not vizinho:
		return atual
	prox = random.choice(vizinho)
	delta_e = h(prox, final) - h(atual, final)
	if delta_e > 0 or math.exp(delta_e / T) > random.random():
		atual = prox
	return atual



def algoritmo(posic, lista):
	return tempera_Simulada(posic,lista)