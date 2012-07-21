# attempting to create a prisoner's dilemma simulation
# game theory from here:  http://www.lifl.fr/IPD/ipd.html.en#cipd
# 17 July 2012

#!/usr/bin/python 

import strategies, random
from pprint import pprint
from collections import namedtuple
import utils
import os
from path import path
import pickle
import plot
from ddd import make_path

#constants
N_AGENTS_ACR = N_AGENTS_DOWN = 100
total_agents = N_AGENTS_ACR * N_AGENTS_DOWN
IT_PER_ROUND = 10
win_width = 4 + N_AGENTS_ACR
win_height = 4 + N_AGENTS_DOWN
num_strats = len(strategies.ALL)
#payoffs
MUTUAL_C = 3
MUTUAL_D = 1
SCREWER = 5
SCREWED = 0
#admin
TIME0UT_RATE = 100 #milliseconds between frames
N_ROUNDS = 500

NEIGHBORS = 4

iteration_count = 0 # 0 == first iteration of the round of iterations
rounds_played = 0 

Edge = namedtuple('Edge', ['agent0','agent1','moves0','moves1'])

POINTS = {
	('C','C'):(MUTUAL_C, MUTUAL_C),
	('D','D'):(MUTUAL_D, MUTUAL_D),
	('D','C'): (SCREWER, SCREWED),
	('C','D'): (SCREWED, SCREWER),
	}
		
class Agent():
	def __init__(self):
		self.points = -5
		self.randomStrat()
		self.neighborhood = [self]
		# store new strategy until calculations are done
		self.newstrat = self.strat
		self.denominator = SCREWER * IT_PER_ROUND * NEIGHBORS
		
	def __repr__(self):
		return 'Agent: %s %s' %(self.points, self.strat.__name__,)

	def randomStrat(self):
		self.strat = random.choice(strategies.SELECTED)

	def pickStrat(self):
#		if random.random() >= 1.1:
#			self.randomStrat()
#			return
		best_neighbor = max(self.neighborhood, 
			key = lambda agent: agent.calcScore())
		self.newstrat = best_neighbor.strat

	def calcScore(self):
		score = float(self.points) / self.denominator
		### RANDOMNESS YO
		#score = score * utils.rand_between(0.9)
		return score
		### RANDOMNESS YO

	def implementNewStrat(self):
		self.strat = self.newstrat

def createAgents():
	agents = [ [Agent() for y in range(N_AGENTS_DOWN)] \
		for x in range(N_AGENTS_ACR) ]
	return agents

def createNetworks(agents):
	conx_acr = len(agents) - 1; conx_down = len(agents[0]) - 1
	# conx = connections
	hz_network = []
	vt_network = []
	for network, horiz, vert, mod_x, mod_y in (
		(hz_network, conx_acr,  N_AGENTS_DOWN, 1, 0),
		(vt_network, N_AGENTS_ACR,  conx_down, 0, 1),
	):
		for x in range(horiz):
			newlist = []
			network.append(newlist)
			for y in range(vert):
				agent0 = agents[x][y]
				agent1 = agents[x+mod_x][y+mod_y]
				edge = Edge(agent0=agent0, agent1=agent1, moves0=[], moves1=[])
				newlist.append(edge)
				agent0.neighborhood.append(agent1)
				agent1.neighborhood.append(agent0)
	return hz_network, vt_network	
	
def playPrisonersDilemma(edge):
	'''one iteration of the prisoner's dilemma between 
	two neighboring agents -- agents C or D'''
	agent0, agent1, moves0, moves1 = edge
	move0 = agent0.strat(iteration_count, agent0, agent1,
				moves0, moves1)
	move1 = agent1.strat(iteration_count, agent1, agent0,
				moves1, moves0)
	moves0.append(move0)
	moves1.append(move1)
	points0, points1 = POINTS[(move0, move1)]
	agent0.points += points0
	agent1.points += points1

def findMoves(agent0, agent1):
	strat0index = agent0.strat
	strat1index = agent1.strat
	move0 = strategies.strategies[strat0index](iteration_count=iteration_count,
		opponent=agent1,player=agent0)
	move1 = strategies.strategies[strat1index](iteration_count=iteration_count,
		opponent=agent0,player=agent1)
	return move0, move1

class Simulation():	
	def __init__(self, figs):
		self.agents = createAgents()
		self.networks = createNetworks(self.agents)
		self.figpath = path(figs)
		if self.figpath.exists():
			self.figpath.move(make_path(self.figpath))
		if not self.figpath.exists():
			self.figpath.mkdir()
		for file in self.figpath.files():
			file.remove()
		
	def playOneIteration(self):
		for network in self.networks:
			for listofedges in network:
				for edge in listofedges:
					playPrisonersDilemma(edge)
	def playOneRound(self):
		global iteration_count
		for iteration_count in range(IT_PER_ROUND):
			print '.',
			self.playOneIteration()
		print
		self.flat_list_of_agents = [agent for lineofagents in self.agents \
			for agent in lineofagents]
		# Agents pick new strategies
		for agent in self.flat_list_of_agents:
			agent.pickStrat()
	def printView(self):
		plot.plotAgents(self.agents)
		self.save()
		
	def prepareNextRound(self):
		for agent in self.flat_list_of_agents:
			agent.points = 0
			agent.implementNewStrat()
		# Reset moves lists in edges
		for network in self.networks:
			for listofedges in network:
				for edge in listofedges:
					edge._replace(moves0 = [])
					edge._replace(moves1 = [])

	def save(self):
		plot.savefig(self.figpath.joinpath('%05d.png' % rounds_played))

	def pickle(self):
		pickle.dump(self.agents, open(self.picklepth.joinpath('%05d.p' % rounds_played),'w'))
	
	def mainLoop(self):
		global rounds_played
		for rounds_played in range(N_ROUNDS):
			print 'round', rounds_played
			self.playOneRound()
			self.printView()
			self.prepareNextRound()


if __name__ == '__main__':
	simulation = Simulation('figs')
	simulation.mainLoop()

