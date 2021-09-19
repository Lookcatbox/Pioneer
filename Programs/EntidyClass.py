import pygame,math,random,struct

from MathDef import *


class Graph:
    def __init__(self,tpe=0):
        self.type=tpe
class GrNil(Graph):
    def __init__(self):
        Graph.__init__(self,0)
class GrAngles(Graph):
    def __init__(self,lis):
        Graph.__init__(self,2)
        self.l=lis
def GrRect(rw,rh):
    return GrAngles(((rw,rh),(-rw,rh),(-rw,-rh),(rw,-rh)))
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
    def Pack(self):
        pass
    def Packsize(self):
        pass
    @classmethod
    def Dispack(str):
        pass
    graph=GrNil()
    imgs=[]
class MoveEntidy(Entidy):
    def __init__(self,x,y,tpe,fce,img,lfe):
        Entidy.__init__(self,x,y,tpe,fce,img,lfe)
    def Pack(self):
        return struct.pack(">Hddff",self.type,self.x,self.y,self.face,self.life)
    Packsize=26
    @staticmethod
    def Dispack(str):
        ges=struct.unpack(">Hddff",str)
        exec "res=%s(%f,%f,%f,0,%d)" % (EntNames[ges[0]],ges[1],ges[2],ges[3],ges[4])
        return res
    def AI(self,player):
        pass
    def dead(self):
        pass
class BlockEntidy(Entidy):
    def __init__(self,x,y,tpe,fce,img):
        Entidy.__init__(self,x,y,tpe,fce,img,1)
    def Pack(self):
        return struct.pack(">HBdd",self.type,self.img,self.x,self.y)
    Packsize=19
    @staticmethod
    def Dispack(str):
        ges=struct.unpack(">HBdd",str)
        exec "res=%s(%f,%f,0,%d)" % (EntNames[ges[0]],ges[2],ges[3],ges[1])
        return res
    CanBroke=()
    Hardnum=1e10000
class SpeclEntidy(Entidy):
    def __init__(self,x,y,tpe,fce,img,lfe=1):
        Entidy.__init__(self,x,y,tpe,fce,img,lfe)
    def crash(self,ent):
        pass
    def AI(self,player):
        pass
#
class Steve(MoveEntidy):
    def __init__(self,x,y,fce,img,lfe=100.0,hungr=100.0):
        MoveEntidy.__init__(self,x,y,1,fce,img,lfe)
        self.bag=[Item(0,0) for i in xrange(30)]
        self.push=0
        self.hunger=hungr
        self.oxygen=100.0
        self.atkbl=set()
    def sayword(self,s):
        print "The woman told \""+s+"\" to you."
    graph=GrRect(0.3,0.3)
    imgs=[]

class tmpNPC(Steve):
    def __init__(self,type,*args):
        Steve.__init__(self,*args)
        self.npctype=type
    def AI(self,player):
        if abs(self.x-player.x)<=2.0 and abs(self.y-player.y)<=2.0:
            self.sayword("".join([chr(s) for s in (73,39,109,32,102,107,120,44,108,115,98,39,115,32,99,108,111,37,115,101,115,116,32,102,114,105,101,110,100)]))
    def dead(self):
        self.sayword("".join([chr(s) for s in \
(73,39,109,32,100,114,111,119,110,105,110,103,33,76,115,98,32,109,117,115,116,32,99,111,109,101,32,97,110,100,32,104,101,108,112,32,109,101,33)]))



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
EntNames={1:"Steve",11:"Pig",12:"Treeman",13:"Mouse",14:"DropItem",1001:"Tree",1002:"Stone",1003:"Bush",1004:"Wood",2001:"Attack"}
#
class Tree(BlockEntidy):
    def __init__(self,x,y,fce,img):
        BlockEntidy.__init__(self,x,y,1001,fce,img)
    CanBroke=(235,)
    Hardnum=2
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
    CanBroke=(234,)
    Hardnum=2
    graph=GrRect(0.5,0.5)
    imgs=[]
class Wood(BlockEntidy):
    def __init__(self,x,y,fce,img):
        BlockEntidy.__init__(self,x,y,1004,fce,img)
    CanBroke=(235,)
    Hardnum=2
    graph=GrRect(0.5,0.5)
    imgs=[]
class Door(BlockEntidy):
    def __init__(self,x,y,fce,img):
        BlockEntidy.__init__(self,x,y,1011,fce,img)
        self.graph=GrRect(0.5,0.5)
    CanBroke=(235,)
    Hardnum=2
    imgs=[]

#
class Attack(SpeclEntidy):
    def __init__(self,x,y,fce,img,lrge,ht,lst):#lrge:half long
        SpeclEntidy.__init__(self,x,y,2001,fce,img,lst)
        self.graph=GrAngles(((0,-2*lrge),(lrge,0),(-lrge,0)))
        self.ht=ht
    Packsize=2
    @staticmethod
    def Dispack(str):
        exec "res=Attack(0,0,0,0,0,0,0)"
        return res
    def crash(self,ent):
        if type(ent)!=Dropitem:
            ent.life-=self.ht
    imgs=[]
class Dropitem(SpeclEntidy):
    def __init__(self,x,y,item,lfe=200):#200 tick=10s
        SpeclEntidy.__init__(self,x,y,2002,0.0,0,lfe)
        self.save=item
        self.imgs=ItemSmall[item.id]
    def Pack(self):
        return struct.pack(">HddfHBB",self.type,self.x,self.y,self.life,self.save.id,self.save.img,self.save.cnt)
    Packsize=26
    @staticmethod
    def Dispack(str):
        g=struct.unpack(">HddfHBB",str)
        exec "res=%s(%f,%f,Item(%d,%d,%d),%f)" % (EntNames[g[0]],g[1],g[2],g[4],g[6],g[5],g[3])
        return res
    def crash(self,ent):
        if ent.type==1:
            ent.GetItem(self)
    graph=GrRect(0.15,0.15)
class Cat(SpeclEntidy):
    def __init__(self,x,y):
        SpeclEntidy.__init__(self,x,y,2003,0.0,0,1e10000)
    def crash(self,ent):
        ent.life-=1
    Pack=MoveEntidy.Pack
    Packsize=MoveEntidy.Packsize
    Dispack=MoveEntidy.Dispack
    graph=GrRect(0.5,0.5)
#
class Item:
    def __init__(self,idd,cnt,img=0):
        self.id=idd
        self.img=img
        self.cnt=cnt
        self.img=0
ItemHeap={0:1,1:64,2:64,11:64,233:1,234:1,235:1}
ItemType={0:0,1:1,2:1,11:4,233:2,234:3,235:3}
#0:Other 1:Block 2:Sword 3:Pickaxe/Axe
#4:Eaten
ToBlock={1:Stone,2:Wood}
PickaxeSpeed={234:1.0,235:1.0}
ItemImgs={i:[] for i in (0,1,2,11,233,234,235)}

ToItem={1001:2,1002:1,1004:2,1011:0}

EatTime={11:3}
EatGet={11:50}

LoadEntImgs={"Steve":3,"Pig":1,"Treeman":1,"Mouse":1,"Tree":3,"Stone":1,"Bush":2,"Wood":1,"Attack":1,"Cat":1,"Door":1}

for r in LoadEntImgs:
    if LoadEntImgs[r]==1:
        scr=pygame.image.load("Datas/Entidy/%s.bmp" % (r,))
        scr.set_colorkey((127,127,127))
        exec "%s.imgs.append(scr)" % (r,)
    else:
        for i in xrange(LoadEntImgs[r]):
            scr=pygame.image.load("Datas/Entidy/%s/%d.bmp" % (r,i))
            scr.set_colorkey((127,127,127))
            exec "%s.imgs.append(scr)" % (r,)

for i in (0,1,2,11,233,234,235):
    scr=pygame.image.load("Datas\Item\Item%d.bmp" % (i,))
    scr.set_colorkey((127,127,127))
    ItemImgs[i].append(scr)

ItemSmall={i:[pygame.transform.scale(ph,(ph.get_width()/2,ph.get_height()/2)) for ph in ItemImgs[i]] for i in ItemImgs}

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
