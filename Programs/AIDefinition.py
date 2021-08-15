import random

from EntidyClass import *
from MathDef import *

def AIDef_init(speclent):
    global SpeclEnt
    SpeclEnt=speclent
def ride(f,peo):
    ent.force.x+=f.x
    ent.force.y+=f.y
    
def route(f,peo):
    peo.turn=f

def move(speed,ent):
    #speed=lis[0]#meter per gametick
    ent.force.x-=speed*math.sin(ent.face/radp)
    ent.force.y-=speed*math.cos(ent.face/radp)
#
def RandomMoveAI(self,player):
    if not random.randrange(8):
        route((random.random()-0.5)*30,self)
    else:
        move(self.speed,self)

def ChaseAI(self,player):
    SpeclEnt[fl(self.x)][fl(self.y)].remove(self)
    self.face=gface(player.x-self.x,player.y-self.y)
    self.x=0.9*self.x+0.1*player.x
    self.y=0.9*self.y+0.1*player.y
    Addentidy(SpeclEnt,self)


Pig.AI=RandomMoveAI
Treeman.AI=RandomMoveAI
Mouse.AI=RandomMoveAI
Cat.AI=ChaseAI