#!/usr/bin/python
import random

def tit4tat(iteration_count, player, oppo, player_moves, oppo_moves):
	"""C first, then plays opponent's last move"""
	if iteration_count == 0: return 'C'
	opp_last_move = oppo_moves[-1]
	if opp_last_move == 'C': return 'C'
	elif opp_last_move == 'D': return 'D'

def alwaysC(iteration_count, player, oppo, player_moves, oppo_moves): 
	return 'C'
def alwaysD(iteration_count, player, oppo, player_moves, oppo_moves): 
	return 'D'

def spiteful(iteration_count, player, oppo, player_moves, oppo_moves):
	"""plays C until opponent plays D, then always D"""
	if iteration_count == 0: return 'C'
	if oppo_moves.count('D') > 0: return 'D'
	else: return 'C'

def soft_majo(iteration_count, player, oppo, player_moves, oppo_moves):
	"""return opponent's majority move, but plays C if equal"""
	num_C = oppo_moves.count('C'); num_D = oppo_moves.count('D')
	if num_D > num_C: return 'D'
	else: return 'C'

def hard_majo(iteration_count, player, oppo, player_moves, oppo_moves):
	"""plays opponent's majority move, if equal then plays 'D'"""
	num_C = oppo_moves.count('C'); num_D = oppo_moves.count('D')
	if num_C > num_D: return 'C'
	else: return 'D'

def per_ddc(iteration_count, player, oppo, player_moves, oppo_moves):
	"""rotate D, D, C"""
	if len(oppo_moves) % 3 == 0: return 'C'
	else: return 'D'

def per_ccd(iteration_count, player, oppo, player_moves, oppo_moves):
	"""rotate C, C, D"""
	if len(oppo_moves) % 3 == 0: return 'D'
	else: return 'C'

def mistrust(iteration_count, player, oppo, player_moves, oppo_moves):
	"""defects first, then plays opponent's last move"""
	if iteration_count == 0: return 'D'
	opp_last_move = oppo_moves[-1]
	if opp_last_move == 'C': return 'C'
	elif opp_last_move == 'D': return 'D'

def per_cd(iteration_count, player, oppo, player_moves, oppo_moves):
	"""rotate C, D"""
	if iteration_count % 2 == 0: return 'C'
	else: return 'D'

def pavlov(iteration_count, player, oppo, player_moves, oppo_moves):
	"""C if both opponents had same move on last move"""
	if iteration_count == 0: return 'C'
	player_last_move = player_moves[-1]; opp_last_move = oppo_moves[-1]
	if player_last_move == opp_last_move: return 'C'
	else: return 'D'

def tit4tat2(iteration_count, player, oppo, player_moves, oppo_moves):
	"""C except if opponent plays D twice consecutively"""
	if iteration_count < 2: return 'C'
	opp_last_2moves = oppo_moves[-2:]
	if opp_last_2moves == ['D','D']: return 'D'
	else: return 'C'

def hard_t4t(iteration_count, player, oppo, player_moves, oppo_moves):
	"""C except if opponent played D at least once in last 2 moves"""
	if iteration_count == 0: return 'C'
	if iteration_count == 1 and oppo_moves[-1] == 'D': return 'D'
	opp_last2moves_Dcount = oppo_moves[-2:].count('D')
	if opp_last2moves_Dcount > 0: return 'D'
	else: return 'C'

def soft_t4t(iteration_count, player, oppo, player_moves, oppo_moves):
	"""round 0 and 1 will be C, then if opponent has same move 2 consec turns, follows"""
	if iteration_count < 2: return 'C'
	opp_last_2moves = oppo_moves[-2:]
	if opp_last_2moves == ['D','D']: return 'D'
	else: return 'C'

def rando(iteration_count, player, oppo, player_moves, oppo_moves):
	"""50/50 chance for C/D"""
	n = random.randint(1,2)
	if n == 1: return 'C'
	else: return 'D'


ALL = [
	tit4tat,  alwaysC,	 alwaysD,
	spiteful,	soft_majo, hard_majo,
	per_ddc,  per_ccd,	 mistrust,
	per_cd,		pavlov,	   tit4tat2,
	hard_t4t,	soft_t4t,	 rando,
]
