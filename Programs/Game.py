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
        f.write(struct.pack(">H",cnt))
        for ent in deltons:
            f.write(struct.pack(">Hddff",ent.type,ent.x,ent.y,ent.face,ent.life))


        cnt=0
        deltons=[]
        for dx in xrange(32):
            if self.x*32+dx in BlockEntidies:
                for dy in xrange(32):
                    if self.y*32+dy in BlockEntidies[self.x*32+dx]:
                        cnt+=1
                        deltons.append(BlockEntidies[self.x*32+dx][self.y*32+dy])
                        del BlockEntidies[self.x*32+dx][self.y*32+dy]
        f.write(struct.pack(">H",cnt))
        for ent in deltons:
            f.write(struct.pack(">HBdd",ent.type,ent.img,ent.x,ent.y))
    def get(self):
        print "Get "+str(self.x)+" "+str(self.y)
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
            ges=struct.unpack(">Hddff",r.read(26))
            exec "ent=%s(%f,%f,%f,0,%d)" % (EntNames[ges[0]],ges[1],ges[2],ges[3],ges[4])#...
            Addentidy(Entidies,ent)
        entnum=struct.unpack(">H",r.read(2))[0]
        for i in xrange(entnum):
            ges=struct.unpack(">HBdd",r.read(19))
            exec "ent=%s(%f,%f,0,%d)" % (EntNames[ges[0]],ges[2],ges[3],ges[1])#...
            SetBlockentidy(BlockEntidies,ent)
        r.close()
def Squaremake(x,y):
    bio,blk,ents=Biome.GetSquare(x,y,seed)
    for i in xrange(4):
        for j in xrange(4):
            r=open("Map/m_%d_%d.map" % (x*4+i,y*4+j),"wb")
            for dx in xrange(32):
                for dy in xrange(32):
                    r.write(struct.pack(">H",blk[i*32+dx][j*32+dy]))
            r.write(b'\x00\x00')
            
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
def exit():
    for i in Sqlist.keys():
        Sqlist[i].close()
        del Sqlist[i]
    path_data = ".\\Map"
    del_file(path_data)

def del_file(path_data):
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
    del ipx,ipy
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
        x=ent.AI()
        
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
    for ent in LoadObjects:
        iex,iey=fl(ent.x),fl(ent.y)
        for dx,dy in CSq5P2:
            if iex+dx in SpeclEntidies and \
               iey+dy in SpeclEntidies[iex+dx]:
                for spe in SpeclEntidies[iex+dx][iey+dy]:
                    if Cross(ent,spe):
                        spe.crash(ent)
                        print "Attack Hurt one!"
                
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

"""def RectCross(x,y,xg,yg):
    rhs=xg.rh*math.sin(x.face/radp)
    rhc=xg.rh*math.cos(x.face/radp)
    rws=xg.rw*math.sin(x.face/radp)
    rwc=xg.rw*math.cos(x.face/radp)
    x0=x.x-rhs-rwc
    y0=x.y-rhc+rws
    x1=x.x-rhs+rwc
    y1=x.y-rhc-rws
    x2=x.x+rhs+rwc
    y2=x.y+rhc-rws
    x3=x.x+rhs-rwc
    y3=x.y+rhc+rws
    rrhs=yg.rh*math.sin(y.face/radp)
    rrhc=yg.rh*math.cos(y.face/radp)
    rrws=yg.rw*math.sin(y.face/radp)
    rrwc=yg.rw*math.cos(y.face/radp)
    xx0=y.x-rrhs-rrwc
    yy0=y.y-rrhc+rrws
    xx1=y.x-rrhs+rrwc
    yy1=y.y-rrhc-rrws
    xx2=y.x+rrhs+rrwc
    yy2=y.y+rrhc-rrws
    xx3=y.x+rrhs-rrwc
    yy3=y.y+rrhc+rrws
    a=((x0,y0,x1,y1),(x1,y1,x2,y2),(x2,y2,x3,y3),(x3,y3,x0,y0))
    b=((xx0,yy0,xx1,yy1),(xx1,yy1,xx2,yy2),(xx2,yy2,xx3,yy3),(xx3,yy3,xx0,yy0))
    if min(x0,x1,x2,x3)>max(xx0,xx1,xx2,xx3) or max(x0,x1,x2,x3)<min(xx0,xx1,xx2,xx3) or \
       min(y0,y1,y2,y3)>max(yy0,yy1,yy2,yy3) or max(y0,y1,y2,y3)<min(yy0,yy1,yy2,yy3):
        return False
    for seg,segg in ((0,1),(0,2),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,0),(3,1),(3,2)):
        if SegmentCross(a[seg][0],a[seg][1],a[seg][2],a[seg][3],b[segg][0],b[segg][1],b[segg][2],b[segg][3]):
            return True
    if PointInGraph(x0,y0,b) or PointInGraph(xx0,yy0,a):
        return True
    return False"""
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
