import random


P ={1:(1.5/512,),2:(4.0/256,2.0/256),3:(128.0/256,30.0/256),4:(),5:(2.5/1024,1.5/1024),6:(),7:(1.5/256,1.0/256),8:(),9:(5.0/256,10.0/256) ,10:(7.5/256,7.5/256),\
    101:(),102:(),103:(60.0/1024,15.0/1024),11:(),12:(2.5/256,1.0/256),21:(),22:(),1001:()}
Pl={1:(1003,)   ,2:(1003,1001)      ,3:(1001,1003)         ,4:(),5:(1003,1001)        ,6:(),7:(1003,(1001,1))  ,8:(),9:((1001,2),(1003,1)),10:(1001,1003)      ,\
    101:(),102:(),103:(1001,1003)          ,11:(),12:(1003,1001)      ,21:(),22:(),1001:()}
biometo={1001:10}
biomeblk={1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:13,12:14,101:17,102:11,103:12,21:17,22:17,1001:17}

BiomeKinds=12
SquareEight=((-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1))
szs=(128,32,8,2)
szmx=szs[0]
szmn=szs[-1]
def Gpt(x,y,wdseed,sz,m):
    alph=x*31+y*53+wdseed*71+sz*113
    random.seed(alph)
    return random.randrange(m)
#input:x,y position and world seed
#output:three tuples
#first is biome
#second is block
#third is blockentidy
def GetSquare(x0,y0,wdseed):
    las={}
    rbiome=[[] for j in xrange(szmx)]
    rblk=[[] for j in xrange(szmx)]
    rent=[[0 for i in xrange(szmx)] for j in xrange(szmx)]
    for sz in szs:
        now=[[0 for i in xrange(-2,szmx/sz+2)] for j in xrange(-2,szmx/sz+2)]
        for i in xrange(-2,szmx/sz+2):
            for j in xrange(-2,szmx/sz+2):
                if sz==szmx:
                    now[i][j]=(Gpt(i*sz+x0*szmx,j*sz+y0*szmx,wdseed,sz,sz)+i*sz,Gpt(i*sz+x0*szmx,j*sz+y0*szmx,wdseed*50,sz,sz)+j*sz,Gpt(i*sz+x0*szmx,j*sz+y0*szmx,wdseed,sz,BiomeKinds)+1)
                else:
                    ibg,jbg=i*sz/szlas,j*sz/szlas
                    sqxmin,xbk=4*szmx*szmx,0
                    rtx,rty=Gpt(i*sz+x0*szmx,j*sz+y0*szmx,wdseed,sz,sz)+i*sz,Gpt(i*sz+x0*szmx,j*sz+y0*szmx,wdseed*50,sz,sz)+j*sz
                    for dx,dy in SquareEight:
                        tx,ty,bk=las[ibg+dx][jbg+dy]
                        sqtmp=(tx-rtx)*(tx-rtx)+(ty-rty)*(ty-rty)
                        if sqtmp<sqxmin:
                            sqxmin=sqtmp
                            xbk=bk
                    if sz==32:
                        if ((xbk in (2,3,5,8,9,12)) and random.random()<0.015) or (xbk==10 and random.random()<0.05):
                            if xbk==3 and random.randrange(10)==0:
                               xbk=102
                            else:
                               xbk=101
                        elif xbk==5 and random.randrange(10)==0:
                            xbk=103
                    elif sz==8 and xbk==10 and random.random()<20/256.0:
                         xbk=1001
                    elif sz==2 and xbk==10 and random.random()<20/4096.0:
                         xbk=1001
                    now[i][j]=(rtx,rty,xbk)
        las=now
        szlas=sz
    for i in xrange(0,szmx):
        for j in xrange(0,szmx):
            ibg,jbg=i/szmn,j/szmn
            sqxmin,xbk=4*szmx*szmx,0
            for dx,dy in SquareEight:
                tx,ty,bk=now[ibg+dx][jbg+dy]
                sqtmp=(tx-i)*(tx-i)+(ty-j)*(ty-j)
                if sqtmp<sqxmin:
                    sqxmin=sqtmp
                    xbk=bk
            if xbk>=1000:
                rbiome[i].append(biometo[xbk])
            else:
                rbiome[i].append(xbk)
            rblk[i].append(biomeblk[xbk])
            mults=1.0
            for ch in xrange(len(P[xbk])):
                if random.random()<P[xbk][ch]/mults:
                    if type(Pl[xbk][ch])==tuple:
                        rent[i][j]=Pl[xbk][ch]
                    else:
                        rent[i][j]=Pl[xbk][ch],0
                    break
                else:
                    mults*=(1-P[xbk][ch])
    return rbiome,rblk,rent
