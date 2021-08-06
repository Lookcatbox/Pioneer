import random

from EntidyClass import *
from MathDef import *

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
def WalkAI(self):
    if not random.randrange(8):
        route((random.random()-0.5)*30,self)
    else:
        move(0.07,self)

def RunAI(self):
    if not random.randrange(6):
        route((random.random()-0.5)*30,self)
    else:
        move(0.35,self)

Pig.AI=WalkAI
Treeman.AI=WalkAI
Mouse.AI=RunAI
