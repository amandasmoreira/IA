#! /usr/bin/env python3
'''
PyMaze driver class. Makes use of the maze class to parse program arguments.
@author: Paul Miller (github.com/138paulmiller)
adapted by Dino Franklin
'''

import os, sys, random, time, threading
import maze_gbc063 as maze
import gbc063
import gbc063_profundidade
import gbc063_prof_limitada


# defalt ANSI settings from user
COLOR_DEFAULT = u'\u001b[0m'
# foreground colors (text)
COLOR_BLACK = u'\u001b[30m'
COLOR_RED =  u'\u001b[31m'
COLOR_GREEN = u'\u001b[32m'
COLOR_YELLOW = u'\u001b[33m'
COLOR_BLUE  =u'\u001b[34m'
COLOR_MAGENTA = u'\u001b[35m'
COLOR_CYAN = u'\u001b[36m'
COLOR_WHITE = u'\u001b[37m'
# background colors 
COLOR_BG_BLACK = u'\u001b[40m'
COLOR_BG_RED =	u'\u001b[41m'
COLOR_BG_GREEN =  u'\u001b[42m'
COLOR_BG_YELLOW = u'\u001b[43m'
COLOR_BG_BLUE = u'\u001b[44m'
COLOR_BG_MAGENTA =  u'\u001b[45m'
COLOR_BG_CYAN = u'\u001b[46m'
COLOR_BG_WHITE= u'\u001b[47m'

def play_maze(maze_obj, limit,tinkle):
	
	#clear the screen clear if linux, cls if windows
	os.system('clear' if os.name!='nt' else 'cls')	
	
	current = (0,0)
	# em (0,0) pergunta para o labirinto acoes possiveis
	info = maze_obj.move(current)
	current = info[1]
	options = info[2]
	soma = 0.0
	count = 0.0		
	move = 0

	# sai qdo qtde movimentos atingiu limite ou o objetivo foi atingido
	while not (move > limit) and not maze_obj.is_done():
		#ALTERAR AQUI O ALGORITMO QUE VOCÊ QUER UTILIZAR
		#action = gbc063.algoritmo(current, options)
		#action = gbc063_prof_limitada.algoritmo(current, options)
		action = gbc063_profundidade.algoritmo(current, options)

	# para debug: escreve posicao e acoes possiveis
	#	action = algoritmo(current, options)
	#	print('pos:',current,'\noptions\n')
	#	for i in range(len(options)):
	#		print(options[i])
	#	print('action:',action)	
		time.sleep(tinkle)
		info = maze_obj.move(action)
		current = info[1]
		options = info[2]
		# update maze based on algoritmo feedback
		move += 1

	# mostra o labirinto
	print(maze_obj.to_str())	

	# saindo 
	if (move < limit):
		print('Objetivo atingido em ',move,' movimentos.');
		print('Solucao:')
		print(maze_obj.path)
	else:
		print('Objetivo nao atingido em ',move,' movimentos.');


	#teste 100 de rodadas
	for n in range(0, 99):
		if (move < limit):
			soma += move
			count += len(maze_obj.path)

	print('Media de ',soma / 100 ,' movimentos!');
	print('Media de (',count / 100 ,' passos ):')
		

def main():

	# set opcoes
	clock = 0.1
	seed = random.random()*10000		
	width = 10
	height = 10 
	limite = 1000
	is_block = True
	is_color = True
	block_symbol = u'\u2588'#unicode FullBlock
	block_symbols = {
		'start' : u'O',
		'end' : u'X',
		'wall_v' : block_symbol, 
		'wall_h' : block_symbol,
		'wall_c' : block_symbol,
		'visited' : block_symbol,
	}
	color_symbols = {
		'empty_color' : COLOR_DEFAULT,
		'visited_color' : COLOR_WHITE,   # incluido
		'wall_color' : COLOR_BLUE,
		'head_color' : COLOR_RED,
		'tail_color' : COLOR_CYAN,
		'start_bg_color' : COLOR_BG_YELLOW,
		'end_bg_color' : COLOR_BG_YELLOW,
		# if color, full block for player too
		'head' : block_symbol,
		'tail' : block_symbol,
		'visited' : block_symbol,   # incluido
	}
	#default symbols (not unicode or ANSI coloring)
	symbols = {
		# default symbols
		'start' : 'S',
		'end' : 'X',
		'wall_v'  : '|',
		'wall_h' : '-',
		'wall_c' : '+',
		'head' :  '#',
		'tail' : 'o',	
		'empty' : ' ',
		'visited' : 'v',
	}

	# se quiser desenho em blocos - necessary monospaced font
	# se nao, comente com #
	symbols.update(block_symbols)
	symbols.update(color_symbols)
				
	# cria labirinto
	maze_obj = maze.Maze(width, height, seed, symbols)

	# sai do labirinto usando seu algoritmo (gbc063)
	play_maze(maze_obj,limite,clock)


#  main
if __name__ == '__main__':
	main() 
