import random

from EntidyClass import *
from MathDef import *

def AIDef_init(speclent):
    global SpeclEnt
    SpeclEnt=speclent
#
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
def ChaseAI(self,player):
    SpeclEnt[fl(self.x)][fl(self.y)].remove(self)
    self.face=gface(player.x-self.x,player.y-self.y)
    self.x=0.9*self.x+0.1*player.x
    self.y=0.9*self.y+0.1*player.y
    Addentidy(SpeclEnt,self)
def WalkAI(ch,sp):
    def Temp(self,player):
        if random.random()<ch:
            move(sp,self)
        else:
            route((random.random()-0.5)*30,self)
    return Temp

Pig.AI=WalkAI(0.875,0.07)
Treeman.AI=WalkAI(0.875,0.07)
Mouse.AI=WalkAI(1.0/6.0,0.35)
Cat.AI=ChaseAI

def PeopleGetItem(self,dritem):
    for nm in (1,2,3,4,5,6,7,8,9,0):
        d=self.bag[nm]
        if not d.id:
            d.id=dritem.save.id
        if d.id==dritem.save.id:
            if d.cnt+dritem.save.cnt>ItemHeap[d.id]:
                dritem.save.cnt=d.cnt+dritem.save.cnt-ItemHeap[d.id]
                d.cnt=ItemHeap[d.id]
            else:
                d.cnt+=dritem.save.cnt
                dritem.save.cnt=0
                break
    if dritem.save.cnt==0:
        dritem.life=0
Steve.GetItem=PeopleGetItem