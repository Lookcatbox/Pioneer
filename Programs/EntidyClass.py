import pygame,math,random

from MathDef import *


class Graph:
    def __init__(self,tpe=0):
        self.type=tpe
class GrNil(Graph):
    def __init__(self):
        Graph.__init__(self,0)
class GrRect(Graph):
    def __init__(self,rw,rh):
        Graph.__init__(self,1)
        self.rw=rw
        self.rh=rh
class Force:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    def __add__(self,another):
        return Force(self.x+another.x,self.y+another.y)
    def __iadd__(self,another):
        self.x=self.x+another.x
        self.y=self.y+another.y
        return self
def Triforce(x,y,sz):
    spsz=math.sqrt(x*x+y*y)
    if spsz==0:
        return Force()
    else:
        return Force(sz/spsz*x,sz/spsz*y)
def TriConst(x,y,sz):
    spsz=math.sqrt(x*x+y*y)
    if spsz==0:
        return (0,0)
    else:
        return (sz/spsz*x,sz/spsz*y)
#
#
class Entidy:
    def __init__(self,x,y,tpe,fce,img,lfe):
        self.x=x
        self.y=y
        self.type=tpe
        self.face=fce
        self.img=img
        self.life=lfe
        self.force=Force()
        self.turn=0
    graph=Graph()
    imgs=[]
class MoveEntidy(Entidy):
    def __init__(self,x,y,tpe,fce,img,lfe):
        Entidy.__init__(self,x,y,tpe,fce,img,lfe)
    def AI(self):
        pass
class BlockEntidy(Entidy):
    def __init__(self,x,y,tpe,fce,img):
        Entidy.__init__(self,x,y,tpe,fce,img,1)
class SpeclEntidy(Entidy):
    def __init__(self,x,y,tpe,fce,img):
        Entidy.__init__(self,x,y,tpe,fce,img,1)
    def crash():
        pass
#
class Steve(MoveEntidy):
    def __init__(self,x,y,fce,img,lfe=1e5):
        MoveEntidy.__init__(self,x,y,1,fce,img,lfe)
        self.bag=[Item(0,0) for i in xrange(10)]
        self.push=0
    graph=GrRect(0.3,0.3)
    imgs=[]
class Pig(MoveEntidy):
    def __init__(self,x,y,fce,img,lfe=5.0):
        MoveEntidy.__init__(self,x,y,11,fce,img,lfe)
    graph=GrRect(0.5,1)
    imgs=[]
class Treeman(MoveEntidy):
    def __init__(self,x,y,fce,img,lfe=1e2):
        MoveEntidy.__init__(self,x,y,12,fce,img,lfe)
    graph=GrRect(1.5,1.5)
    imgs=[]
class Mouse(MoveEntidy):
    def __init__(self,x,y,fce,img,lfe=1.0):
        MoveEntidy.__init__(self,x,y,13,fce,img,lfe)
    graph=GrRect(0.3,0.3)
    imgs=[]
EntNames={1:"Steve",11:"Pig",12:"Treeman",13:"Mouse",1001:"Tree",1002:"Stone",1003:"Bush",2001:"Attack"}
#
class Tree(BlockEntidy):
    def __init__(self,x,y,fce,img):
        BlockEntidy.__init__(self,x,y,1001,fce,img)
    graph=GrRect(0.4,0.4)
    imgs=[]
class Bush(BlockEntidy):
    def __init__(self,x,y,fce,img):
        BlockEntidy.__init__(self,x,y,1003,fce,img)
    graph=GrNil()
    slnum=0.5
    slgraph=GrRect(0.4,0.4)
    imgs=[]
class Stone(BlockEntidy):
    def __init__(self,x,y,fce,img):
        BlockEntidy.__init__(self,x,y,1002,fce,img)
    graph=GrRect(0.5,0.5)
    imgs=[]
#
class Attack(SpeclEntidy):
    def __init__(self,x,y,fce,img,lrge,ht):
        SpeclEntidy.__init__(self,x,y,2001,fce,img)
        self.graph=GrRect(lrge,lrge)
        self.ht=ht
    def crash(self,ent):
        ent.life-=self.ht
    imgs=[]
#
class Item:
    def __init__(self,idd,cnt):
        self.id=idd
        self.cnt=cnt
        self.img=0
ItemHeap={0:1,1:64,233:1}
ItemType={0:0,1:2,233:1}#0:Sth. Like Pickaxe and Axe 1:Sword 2:Block
ToBlock={1:Stone}
ItemImgs={0:[],1:[],233:[]}

LoadEntImgs={"Steve":1,"Pig":1,"Treeman":1,"Mouse":1,"Tree":3,"Stone":1,"Bush":2}

for r in LoadEntImgs:
    if LoadEntImgs[r]==1:
        scr=pygame.image.load("Datas/Entidy/%s.bmp" % (r,))
        scr.set_colorkey((127,127,127))
        exec "%s.imgs.append(scr)" % (r,)
    else:
        for i in xrange(LoadEntImgs[r]):
            scr=pygame.image.load("Datas/Entidy/%s/%s%d.bmp" % (r,r,i))
            scr.set_colorkey((127,127,127))
            exec "%s.imgs.append(scr)" % (r,)

for i in (0,1,233):
    scr=pygame.image.load("Datas\Item\Item%d.bmp" % (i,))
    scr.set_colorkey((127,127,127))
    ItemImgs[i].append(scr)

#
def Addentidy(lis,ent):
    ix,iy=fl(ent.x),fl(ent.y)
    if ix not in lis:
        lis[ix]={}
    if iy not in lis[ix]:
        lis[ix][iy]=set()
    lis[ix][iy].add(ent)
def SetBlockentidy(lis,ent):
    ix=fl(ent.x)
    if ix not in lis:
        lis[ix]={}
    lis[ix][fl(ent.y)]=ent
#
