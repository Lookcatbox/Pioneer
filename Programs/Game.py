import pygame,math,pickle,random,time,struct,os

from EntidyClass import *
from AIDefinition import *
from MathDef import *
import Biome

class Square:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.keep=True
    def close(self):
        global Blockos,Entidies,BlockEntidies
        f=open("Map/m_%d_%d.map" % (self.x,self.y),"wb")
        for dx in xrange(32):
            for dy in xrange(32):
                f.write(struct.pack(">H",Blockos[self.x*32+dx][self.y*32+dy]))
                del Blockos[self.x*32+dx][self.y*32+dy]


        cnt=0
        deltons=[]
        for dx in xrange(32):
            if self.x*32+dx in Entidies:
                for dy in xrange(32):
                    if self.y*32+dy in Entidies[self.x*32+dx]:
                        cnt+=len(Entidies[self.x*32+dx][self.y*32+dy])
                        for ent in Entidies[self.x*32+dx][self.y*32+dy]:
                            deltons.append(ent)
                        Entidies[self.x*32+dx][self.y*32+dy]=set()
        for dx in xrange(32):
            if self.x*32+dx in BlockEntidies:
                for dy in xrange(32):
                    if self.y*32+dy in BlockEntidies[self.x*32+dx]:
                        cnt+=1
                        deltons.append(BlockEntidies[self.x*32+dx][self.y*32+dy])
                        del BlockEntidies[self.x*32+dx][self.y*32+dy]
        f.write(struct.pack(">H",cnt))
        for ent in deltons:
            f.write(ent.Pack())
        f.close()
    def get(self):
        try:
            r=open("Map/m_%d_%d.map" % (self.x,self.y),"rb")
        except:
            Squaremake(self.x/4,self.y/4)
            r=open("Map/m_%d_%d.map" % (self.x,self.y),"rb")
        if self.x*32 not in Blockos:
            for i in xrange(32):
                Blockos[self.x*32+i]={}
        strs=struct.unpack(">1024H",r.read(2048))
        for i in xrange(32):
            for j in xrange(32):
                Blockos[self.x*32+i][self.y*32+j]=strs[i*32+j]
        entnum=struct.unpack(">H",r.read(2))[0]
        for i in xrange(entnum):
            strs=r.read(2)
            entnum=struct.unpack(">H",strs)[0]
            exec "entype=%s" % (EntNames[entnum],)
            strs=strs+r.read(entype.Packsize-2)
            if entnum<=1000:
                Addentidy(Entidies,entype.Dispack(strs))
            else:
                SetBlockentidy(BlockEntidies,entype.Dispack(strs))
        r.close()
def Squaremake(x,y):
    bio,blk,ents=Biome.GetSquare(x,y,seed)
    for i in xrange(4):
        for j in xrange(4):
            r=open("Map/m_%d_%d.map" % (x*4+i,y*4+j),"wb")
            for dx in xrange(32):
                for dy in xrange(32):
                    r.write(struct.pack(">H",blk[i*32+dx][j*32+dy]))
            
            cnt=0
            for xx in xrange(i*32,i*32+32):
                for yy in xrange(j*32,j*32+32):
                    if ents[xx][yy]:
                        cnt+=1
            r.write(struct.pack(">H",cnt))
            for xx in xrange(i*32,i*32+32):
                for yy in xrange(j*32,j*32+32):
                    if ents[xx][yy]:
                        r.write(struct.pack(">HBdd",ents[xx][yy][0],ents[xx][yy][1],x*128+xx+0.5,y*128+yy+0.5))
            r.close()
Peoples=[]
MovementList=[]
def init(_seed):
    global seed,BlockEntidies,Entidies,Blockos,Sqlist,SpeclEntidies
    seed=_seed
    BlockEntidies={}
    SpeclEntidies={}
    Entidies={}
    Blockos={}
    Sqlist={}
    AIDef_init(SpeclEntidies)
def exit():
    for i in Sqlist.keys():
        Sqlist[i].close()
        del Sqlist[i]
    path_data = ".\\Map"
    del_file(path_data)

def del_file(path_data):
    print ("succeed in deleting files:",os.listdir(path_data))
    for i in os.listdir(path_data) :# os.listdir(path_data)
        file_data = path_data + "\\" + i
        os.remove(file_data)

def CanPush(bent):
    iex,iey=fl(bent.x),fl(bent.y)
    try:
        BlockEntidies[iex][iey]
        return False
    except:
        pass
    for dx,dy in CSq5:
        if iex+dx in Entidies and \
           iey+dy in Entidies[iex+dx]:
            for otent in Entidies[iex+dx][iey+dy]:
                if Cross(bent,otent):
                    return False
    return True
def loadsq(x,y):
    if (x,y) not in Sqlist:
        r=Square(x,y)
        r.get()
        Sqlist[(x,y)]=r
    else:
        Sqlist[(x,y)].keep=True
def disloadsq():
    for i in Sqlist.keys():
        if not Sqlist[i].keep:
            Sqlist[i].close()
            del Sqlist[i]
def frame():
    sqx,sqy=fl(Peoples[0].x/32),fl(Peoples[0].y/32)
    for i in Sqlist:
        Sqlist[i].keep=False
    loadsq(sqx,sqy)
    loadsq(sqx+1,sqy)
    loadsq(sqx-1,sqy)
    loadsq(sqx,sqy+1)
    loadsq(sqx+1,sqy+1)
    loadsq(sqx-1,sqy+1)
    loadsq(sqx,sqy-1)
    loadsq(sqx+1,sqy-1)
    loadsq(sqx-1,sqy-1)
    disloadsq()
def execute():
    global MovementList
    LoadObjects=[]
    ipx,ipy=fl(Peoples[0].x),fl(Peoples[0].y)
    for i in xrange(-13,14):
        if ipx+i in Entidies:
            for j in xrange(-13,14):
                if ipy+j in Entidies[ipx+i]:
                    for ent in list(Entidies[ipx+i][ipy+j]):
                        if ent.life<=0:
                            Entidies[ipx+i][ipy+j].remove(ent)
                        else:
                            LoadObjects.append(ent)
    for ent in LoadObjects:
        iex,iey=fl(ent.x),fl(ent.y)
        for dx,dy in CSq5:
            if iex+dx in Entidies and \
               iey+dy in Entidies[iex+dx]:
                for otent in Entidies[iex+dx][iey+dy]:
                    if otent!=ent and \
                       Cross(ent,otent):
                        l=0.0
                        r=0.4
                        while r-l>1e-4:
                            mid=(l+r)/2
                            ent.force+=Triforce(ent.x-otent.x,ent.y-otent.y,mid)
                            ent.x+=ent.force.x
                            ent.y+=ent.force.y
                            if Cross(ent,otent):
                                l=mid
                            else:
                                r=mid
                            ent.x-=ent.force.x
                            ent.y-=ent.force.y
                            ent.force+=Triforce(ent.x-otent.x,ent.y-otent.y,-mid)
                        ent.force+=Triforce(ent.x-otent.x,ent.y-otent.y,l)
                                

    for ent in LoadObjects:
        ent.AI(Peoples[0])
    for i in xrange(-13,14):
        if ipx+i in SpeclEntidies:
            for j in xrange(-13,14):
                if ipy+j in SpeclEntidies[ipx+i]:
                    for ent in list(SpeclEntidies[ipx+i][ipy+j]):
                        ent.AI(Peoples[0])
    for ent in LoadObjects:
        if ent.force.x==0 and ent.force.y==0:
            continue
        slowp=BushCross(ent)
        ent.force.x*=slowp
        ent.force.y*=slowp
        Entidies[fl(ent.x)][fl(ent.y)].remove(ent)
        l=0.0
        r=math.sqrt(ent.force.x*ent.force.x+ent.force.y*ent.force.y)
        while r-l>1e-4:
            crossed=False
            mid=(l+r)/2
            tup=TriConst(ent.force.x,ent.force.y,mid)
            ent.x+=tup[0]
            ent.y+=tup[1]
            for dx,dy in CSq5P2:
                if fl(ent.x)+dx in BlockEntidies and \
                   fl(ent.y)+dy in BlockEntidies[fl(ent.x)+dx] and \
                   Cross(ent,BlockEntidies[fl(ent.x)+dx][fl(ent.y)+dy]):
                    crossed=True
                    break
            ent.x-=tup[0]
            ent.y-=tup[1]
            if crossed:
                r=mid
            else:
                l=mid
        if l:
            tup=TriConst(ent.force.x,ent.force.y,l)
            ent.x+=tup[0]
            ent.y+=tup[1]
        else:
            l=0.0
            r=0.5
            while r-l>1e-4:
                crossed=False
                mid=(l+r)/2.0
                tup=TriConst(ent.force.x,ent.force.y,mid)
                ent.x+=tup[0]
                ent.y+=tup[1]
                crossed=BlockCross(ent)
                ent.x-=tup[0]
                ent.y-=tup[1]
                if crossed:
                    r=mid
                else:
                    l=mid
            tup=TriConst(ent.force.x,ent.force.y,l)
            if r!=0.5:
                ent.x+=tup[0]
                ent.y+=tup[1]
        ent.force=Force()
        Addentidy(Entidies,ent)
    for ent in LoadObjects:
        if ent.turn==0:
            continue
        ent.face+=ent.turn
        if BlockCross(ent):
            ent.face-=ent.turn
        ent.turn=0
    for atk in Peoples[0].atkbl:
         atk.x,atk.y,atk.face=Peoples[0].x-0.5*math.sin(Peoples[0].face/radp),Peoples[0].y-0.5*math.cos(Peoples[0].face/radp),Peoples[0].face
    for ent in LoadObjects:
        iex,iey=fl(ent.x),fl(ent.y)
        for dx,dy in CSq5P2:
            if iex+dx in SpeclEntidies and \
               iey+dy in SpeclEntidies[iex+dx]:
                for spe in SpeclEntidies[iex+dx][iey+dy]:
                    if Cross(ent,spe):
                        spe.crash(ent)
    for i in xrange(-13,14):
        if ipx+i in SpeclEntidies:
            for j in xrange(-13,14):
                if ipy+j in SpeclEntidies[ipx+i]:
                    for ent in list(SpeclEntidies[ipx+i][ipy+j]):
                        ent.life-=1
                        if ent.life<=0:
                            SpeclEntidies[ipx+i][ipy+j].remove(ent)
    for atk in list(Peoples[0].atkbl):
        if atk.life<=0:
            Peoples[0].atkbl.remove(atk)
def BushCross(ent):
    iex,iey=fl(ent.x),fl(ent.y)
    res=1
    for dx,dy in CSq5P2:
        if iex+dx in BlockEntidies and \
           iey+dy in BlockEntidies[iex+dx] and \
           BlockEntidies[iex+dx][iey+dy].type==1003 and \
           ACross(BlockEntidies[iex+dx][iey+dy],ent,BlockEntidies[iex+dx][iey+dy].slgraph):
            res*=BlockEntidies[iex+dx][iey+dy].slnum
            
    return res
def BlockCross(ent):
    iex,iey=fl(ent.x),fl(ent.y)
    for dx,dy in CSq5P2:
        if iex+dx in BlockEntidies and \
           iey+dy in BlockEntidies[iex+dx] and \
           Cross(ent,BlockEntidies[iex+dx][iey+dy]):
            return True
    return False
def Cross(x,y):
    return BCross(x,y,x.graph,y.graph)
def ACross(x,y,xg):
    return BCross(x,y,xg,y.graph)
def BCross(x,y,xg,yg):
    if xg.type==2 and yg.type==2:
        return AngleCross(x,y,xg,yg)
    else:
        return False
def AngleCross(x,y,xg,yg):
    sx=math.sin(x.face/radp)
    cx=math.cos(x.face/radp)
    xx,xy=[],[]
    for p in xg.l:
        xx.append(x.x+p[0]*cx+p[1]*sx)
        xy.append(x.y-p[0]*sx+p[1]*cx)
    sy=math.sin(y.face/radp)
    cy=math.cos(y.face/radp)
    yx,yy=[],[]
    for p in yg.l:
        yx.append(y.x+p[0]*cy+p[1]*sy)
        yy.append(y.y-p[0]*sy+p[1]*cy)
    if min(xx)>max(yx) or max(xx)<min(yx) or \
       min(xy)>max(yy) or max(xy)<min(yy):
        return False
    xl,yl=len(xg.l),len(yg.l)
    for s0 in xrange(xl):
         for s1 in xrange(yl):
             if s0!=s1 and \
                SegmentCross(xx[s0],xy[s0],xx[s0+1 if s0+1<xl else 0],xy[s0+1 if s0+1<xl else 0],\
                             yx[s1],yy[s1],yx[s1+1 if s1+1<yl else 0],yy[s1+1 if s1+1<yl else 0]):
                 return True
    if PointInGraph(xx[0],xy[0],yx,yy,yl) or PointInGraph(yx[0],yy[0],xx,xy,xl):
        return True
    return False
def PointInGraph(x,y,gx,gy,gl):
    #x same ray
    cnt=0
    for i in xrange(gl-1):
        if max(gx[i],gx[i+1])==x:
            cnt+=1
        elif SegmentRayCross(gx[i],gy[i],gx[i+1],gy[i+1],x,y):
            cnt+=1
    if max(gx[gl-1],gx[0])==x:
        cnt+=1
    elif SegmentRayCross(gx[gl-1],gy[gl-1],gx[0],gy[0],x,y):
        cnt+=1
    if cnt%2:
        return True
    return False
def SegmentRayCross(x0,y0,x1,y1,xx,yy):
    if min(x0,x1)>xx or xx>max(x0,x1) or yy>max(y0,y1):
        return False
    return ((x1-x0)*(yy-y0)-(y1-y0)*(xx-x0))*(x1-x0)<=0 and \
           (x0-xx)*(x1-xx)<=0
def SegmentCross(x0,y0,x1,y1,x2,y2,x3,y3):
    if min(x0,x1)>max(x2,x3) or min(x2,x3)>max(x0,x1) or min(y0,y1)>max(y2,y3) or min(y2,y3)>max(y0,y1):
        return False
    return ((x1-x0)*(y2-y0)-(y1-y0)*(x2-x0))* \
           ((x1-x0)*(y3-y0)-(y1-y0)*(x3-x0))<=0 and \
           ((x3-x2)*(y0-y2)-(y3-y2)*(x0-x2))* \
           ((x3-x2)*(y1-y2)-(y3-y2)*(x1-x2))<=0
#raise
