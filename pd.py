# attempting to create a prisoner's dilemma simulation
# game theory from here:  http://www.lifl.fr/IPD/ipd.html.en#cipd
# 17 July 2012

#!/usr/bin/python

import strategies, random
from pprint import pprint
from collections import namedtuple

#constants
N_AGENTS_ACR = 4; N_AGENTS_DOWN = 4; total_agents = N_AGENTS_ACR * N_AGENTS_DOWN
IT_PER_ROUND = 10
win_width = 4 + N_AGENTS_ACR
win_height = 4 + N_AGENTS_DOWN
num_strats = len(strategies.strategies)
#payoffs
MUTUAL_C = 3;     MUTUAL_D = 1
SCREWER = 5;      SCREWED = 0
#admin
TIME0UT_RATE = 100 #milliseconds between frames

iteration_count = 0 # 0 == first iteration of the round of iterations

Edge = namedtuple('Edge', ['agent0','agent1','moves'])

class Agent():
	def __init__(self):
		self.points = int()
		self.moves = []
		self.strat = random.randint(0,num_strats-1)
		self.neighborhood = [self]
		self.newstrat = self.strat # store new strategy until calculations are done
	def __repr__(self):
		return 'Agent: %s %s %s' %(self.points, self.strat, len(self.moves))
	def pickStrat(self):
		best_neighbor = max(self.neighborhood, key = lambda agent: agent.calcScore())
		self.newstrat = best_neighbor.strat
	def calcScore(self):
		denominator =  SCREWER * IT_PER_ROUND * (len(self.neighborhood)-1)
		return float(self.points) / denominator
	def implementNewStrat(self):
		self.strat = self.newstrat

def createAgents():
	agents = [ [Agent() for y in range(N_AGENTS_DOWN)] \
		for x in range(N_AGENTS_ACR) ]
	return agents

def createNetworks(agents):
	conx_acr = len(agents) - 1; conx_down = len(agents[0]) - 1 # conx = connections
	hz_network = []; vt_network = []
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
				edge = Edge(agent0=agent0, agent1=agent1, moves=[])
				newlist.append(edge)
				agent0.neighborhood.append(agent1)
				agent1.neighborhood.append(agent0)
	return hz_network, vt_network	
	
	
'''
	for x in range(conx_acr):
		newlist = []
		hz_network.append(newlist)
		for y in range(N_AGENTS_DOWN):
			agent0 = agents[x][y]; agent1 = agents[x+1][y]
			newlist.append( (agent0,agent1) )
			agent0.neighborhood.append(agent1)
			agent1.neighborhood.append(agent0)
	for x in range(N_AGENTS_ACR):
		newlist = []
		vt_network.append(newlist)
		for y in range(conx_down):
			agent0 = agents[x][y]; agent1 = agents[x][y+1]
			newlist.append( (agent0,agent1) )
			agent0.neighborhood.append(agent1)
			agent1.neighborhood.append(agent0)
	return hz_network, vt_network

for y in range(N_AGENTS_DOWN):
		newlist = []
		hz_network.append(newlist)
		for x in range(conx_acr):
			newlist.append( (agents[ )
def oldCreateNetwork(agents):
	conx_acr = len(agents) - 1; conx_down = len(agents[0]) - 1 # conx = connections
	hz_network = [ [ (agents[x][y],agents[x+1][y]) for y in range(N_AGENTS_DOWN) ] \
		for x in range(conx_acr) ]
	vt_network = [ [ (agents[x][y],agents[x][y+1]) for y in range(conx_down) ] \
		for x in range(N_AGENTS_ACR) ]
	return hz_network, vt_network

'''	

def playPrisonersDilemma(edge):
		'''one iteration of the prisoner's dilemma between 
		two neighboring agents -- agents C or D'''
		agent0, agent1, moves = edge
		move0, move1 = findMoves(agent0, agent1)
		points0, points1 = awardPoints(move0, move1)
		moves.append( (move0,move1) )
		agent0.points += points0; agent1.points += points1

def playPrisonersDilemma(edge):
	move0, move1 = findMoves(edge)
	

def findMoves(agent0, agent1):
	strat0index = agent0.strat; strat1index = agent1.strat
	move0 = strategies.strategies[strat0index](iteration_count=iteration_count,
		opponent=agent1,player=agent0)
	move1 = strategies.strategies[strat1index](iteration_count=iteration_count,
		opponent=agent0,player=agent1)
	return move0, move1

def awardPoints(move0, move1):	
	if move0 == 'C' and move1 == 'C': return MUTUAL_C, MUTUAL_C
	elif move0 == 'D' and move1 == 'D': return MUTUAL_D, MUTUAL_D
	elif move0 == 'D' and move1 == 'C': return SCREWER, SCREWED
	elif move0 == 'C' and move1 == 'D': return SCREWED, SCREWER


class Simulation():	
	def __init__(self):
		self.agents = createAgents()
		self.networks = createNetworks(self.agents)
	def playOneIteration(self):
		for network in self.networks:
			for listofedges in network:
				for edge in listofedges:
					playPrisonersDilemma(edge)
	def playOneRound(self):
		global iteration_count
		for iteration_count in range(IT_PER_ROUND):
			self.playOneIteration()
		for lineofagents in self.agents:
			for agent in lineofagents:
				agent.pickStrat()
		for lineofagents in self.agents:
			for agent in lineofagents:
				agent.points = 0
				agent.implementNewStrat()
				# reset all agents' movelists to []
	
	def mainLoop(self):
		while True:
			self.playOneRound()
			pprint(self.agents)
			exit()

if __name__ == '__main__':
	simulation = Simulation()
	simulation.mainLoop()

