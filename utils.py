import random
def rand_between(x=0.0,y=1.0):
    diff = y-x
    r = random.random()
    return 1 - diff + (r / (1 / diff))

