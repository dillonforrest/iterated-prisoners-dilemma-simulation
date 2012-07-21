from pylab import *
from pprint import pprint
import strategies

def plotAgents(agents):
    figure(1)
    #pprint(agents)
    scores = [[strategies.ALL.index(agent.strat) for agent in row] \
			for row in agents]
    #maxscore = max(score for row in scores for score in row)
    #ags = [[float(score)/maxscore for score in row] for row in scores]
    #legend([f.__name__ for f in strategies.ALL])
#    legend()
    imshow(scores, interpolation='nearest')
    
#    show()
    grid(True)
#    exit()

