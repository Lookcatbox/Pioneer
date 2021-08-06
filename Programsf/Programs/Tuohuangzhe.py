import pygame,time,pickle,sys,math
sys.setrecursionlimit(1000000)

import Game
from MathDef import *

gtkey={}

gtkey[96]=['`','~']
gtkey[49]=['1','!']
gtkey[50]=['2','@']
gtkey[51]=['3','#']
gtkey[52]=['4','$']
gtkey[53]=['5','%']
gtkey[54]=['6','^']
gtkey[55]=['7','&']
gtkey[56]=['8','*']
gtkey[57]=['9','(']
gtkey[48]=['0',')']
gtkey[45]=['-','_']
gtkey[61]=['=','+']
gtkey[32]=[' ',' ']
gtkey[91]=['[','{']
gtkey[93]=[']','}']
gtkey[92]=['\\','|']
gtkey[59]=[';',':']
gtkey[39]=['\'','"']
gtkey[44]=[',','<']
gtkey[46]=['.','>']
gtkey[47]=['/','?']
gtkey[256]=['0','0']
gtkey[257]=['1','1']
gtkey[258]=['2','2']
gtkey[259]=['3','3']
gtkey[260]=['4','4']
gtkey[261]=['5','5']
gtkey[262]=['6','6']
gtkey[263]=['7','7']
gtkey[264]=['8','8']
gtkey[265]=['9','9']
gtkey[266]=['.','.']
gtkey[270]=['+','+']
gtkey[269]=['-','-']
gtkey[268]=['*','*']
gtkey[267]=['/','/']
gtkey[97]=['a','A']
gtkey[98]=['b','B']
gtkey[99]=['c','C']
gtkey[100]=['d','D']
gtkey[101]=['e','E']
gtkey[102]=['f','F']
gtkey[103]=['g','G']
gtkey[104]=['h','H']
gtkey[105]=['i','I']
gtkey[106]=['j','J']
gtkey[107]=['k','K']
gtkey[108]=['l','L']
gtkey[109]=['m','M']
gtkey[110]=['n','N']
gtkey[111]=['o','O']
gtkey[112]=['p','P']
gtkey[113]=['q','Q']
gtkey[114]=['r','R']
gtkey[115]=['s','S']
gtkey[116]=['t','T']
gtkey[117]=['u','U']
gtkey[118]=['v','V']
gtkey[119]=['w','W']
gtkey[120]=['x','X']
gtkey[121]=['y','Y']
gtkey[122]=['z','Z']
gtkey[32]=[' ',' ']
#gtkey is Key->Char Dict

#Game Direction Pos:
"""
O------> x
|......
|......
|......
|......
|......
|......
V

y
"""
#Game Face:
"""
\a|
 \|
  o
"""

#

def commsg(msg):
    exec msg
def errorpush(errnum):
    return
#

def gametype_0():
    global gt0_re
    gt0_re=edito(1180,35,fonto_20)
#
def screen_redraw_0():
    screen.fill(bgcol)
    global leftsurface
    blockleast=[fl(Player.x)-13,fl(Player.y)-13]
    for i in xrange(27):
        for j in xrange(27):
            rects=(400+32*(blockleast[0]+i-Player.x),400+32*(blockleast[1]+j-Player.y))
            try:
                b=Game.Blockos[i+blockleast[0]][j+blockleast[1]]
            except:
                b=20
            try:
                leftsurface.blit(blockimg[b],rects)
            except:
                leftsurface.blit(errimg,rects)
    rects=(400+32*(fl(mx)-Player.x),400+32*(fl(my)-Player.y))
    if howdealpoint:
        leftsurface.blit(howdealblocks[howdealpoint],rects)
    for i in xrange(27):
        if blockleast[0]+i not in Game.Entidies:
            continue
        for j in xrange(27):
            if blockleast[1]+j not in Game.Entidies[blockleast[0]+i]:
                continue
            for ent in Game.Entidies[blockleast[0]+i][blockleast[1]+j]:
                scr=pygame.transform.rotate(ent.imgs[ent.img],ent.face)
                scr=scr.convert_alpha()
                rct=scr.get_rect()
                leftsurface.blit(scr,[400+(ent.x-Player.x)*32-rct.width/2,400+(ent.y-Player.y)*32-rct.height/2])
    for i in xrange(27):
        if blockleast[0]+i not in Game.BlockEntidies:
            continue
        for j in xrange(27):
            if blockleast[1]+j not in Game.BlockEntidies[blockleast[0]+i]:
                continue
            ent=Game.BlockEntidies[blockleast[0]+i][blockleast[1]+j]
            scr=pygame.transform.rotate(ent.imgs[ent.img],ent.face)
            scr=scr.convert_alpha()
            rct=scr.get_rect()
            leftsurface.blit(scr,[400+(ent.x-Player.x)*32-rct.width/2,400+(ent.y-Player.y)*32-rct.height/2])
    for i in xrange(10):
        if Player.push==i:
            leftsurface.blit(ltx[i],(TexBarx[i],600))
        else:
            leftsurface.blit(dtx[i],(TexBarx[i],600))
        leftsurface.blit(Game.ItemImgs[Player.bag[i].id][Player.bag[i].img],(TexBarx[i]+1,601))
        if Player.bag[i].cnt>1:
            leftsurface.blit(fonto_10.render(str(Player.bag[i].cnt),True,blcol,bgcol),(TexBarx[i]+24,627))
    screen.blit(leftsurface,[0,0])
TexBarx=(528,240,272,304,336,368,400,432,464,496)
#[240+32*9]+[208+32*i for i in xrange(1,10)]
def screen_redraw_1():
    screen_redraw_0()
    screen.blit(gt1_comup,(1180,23))
    pygame.draw.rect(screen,blcol,(1180,46,350,35),2)
    gt0_re.draw(screen,(1185,54))
#
def push_0(pos,lpos):
    global editos
    editos=0
    dx=fl(mx)-Player.x
    dy=fl(my)-Player.y
    if Game.ItemType[Player.bag[Player.push].id]==2:
        if min(dx*dx,(dx+1)*(dx+1))+min(dy*dy,(dy+1)*(dy+1))<=9.0:#3*3
            bet=(Game.ToBlock[Player.bag[Player.push].id])(fl(mx)+0.5,fl(my)+0.5,0,0)
            if Game.CanPush(bet):
                Game.SetBlockentidy(Game.BlockEntidies,bet)
                Player.bag[Player.push].cnt-=1
                if not Player.bag[Player.push].cnt:
                    Player.bag[Player.push]=Game.Item(0,0)
def push_1(pos,lpos):
    global editos
    push_0(pos,lpos)
    if 1180<=pos[0] and pos[0]<1180+350 and 46<=pos[1] and pos[1]<46+35:
        editos=gt0_re
#
def move(pos):
    global howdealpoint
    dx=fl(mx)-Player.x
    dy=fl(my)-Player.y
    if Game.ItemType[Player.bag[Player.push].id]==2:
        if min(dx*dx,(dx+1)*(dx+1))+min(dy*dy,(dy+1)*(dy+1))<=9.0:#3*3
            howdealpoint=1
        else:
            howdealpoint=2
    else:
        howdealpoint=0
def pmove(pos,lpos,downs):
    return
def push(pos,lpos):
    if gametype==0:
        push_0(pos,lpos)
    elif gametype==1:
        push_1(pos,lpos)
def screen_redraw(gt):
    if gt==0:
        screen_redraw_0()
    elif gt==1:
        screen_redraw_1()
def connect(gt):
    if gt==0:
        gametype_0()
    elif gt==1:
        return
#
class edito:
    def __init__(self,ls,height,fontis):
        self.lside=ls
        self.high=height
        self.string=""
        self.fpos=0
        self.fonto=fontis
    def draw(self,scr,where):
        screen.blit(self.fonto.render(self.string,False,blcol,bgcol),where)
        #screen.draw()
#

def gface(x,y):
    if y==400:
        if x<=400:
            return 90
        else:
            return -90
    return math.atan(float(x-400)/float(y-400))*radp+180*(y>400)
#
pygame.init()

gametype=0
#0~... (0:main 10:sandbox 20:multiplas)

errimg=pygame.image.load("Datas/blockerr.bmp")
blockimg=[errimg for i in xrange(0,100)]
for i in range(1,15)+[17,20]:
    blockimg[i]=pygame.image.load("Datas/block%d.bmp"%(i,))

Gblock=pygame.image.load("Datas/GBlock.bmp")
Bblock=pygame.image.load("Datas/BBlock.bmp")

Gblock.set_alpha(127)
Bblock.set_alpha(127)


bgcol=(255,255,255)
blcol=(0,0,0)

version="Tuohuangzhe Pre-29 With Pygame"

dtx=[]
ltx=[]
for i in xrange(10):
    dtx.append(pygame.image.load("Datas/Tex%d.bmp"%(i,)))
    ltx.append(pygame.image.load("Datas/LTex%d.bmp"%(i,)))
    dtx[-1].set_alpha(127)
    ltx[-1].set_alpha(127)
fonto_10=pygame.font.Font(None,10)
fonto_20=pygame.font.Font(None,20)
gt1_comup=fonto_20.render(version,False,blcol,bgcol)
leftsurface=pygame.Surface((800,800))

mdownpos=[]
ismdown=False#mousekey

issdown=False#shift
isf3down=False#F3
iswdown=False#W

editpos=[0,0]
edith=23
editos=0

bgeditos=[]

howdealpoint=0
howdealblocks={1:Gblock,2:Bblock}

print version+"\n"
sfl=True
while sfl:
    print "Input Seed:"
    sed=raw_input()
    try:
        sed=int(sed)
        sfl=False
    except:
        pass



Game.init(sed)
screen=pygame.display.set_mode((1600,850),pygame.RESIZABLE)#0~1599 0~849
lastgt=lastft=0







connect(gametype)


print "Game Executing"
Player=Game.Steve(63.5,63.5,0,0)
Game.Peoples.append(Player)
Game.Addentidy(Game.Entidies,Player)
Player.push=1
for i in xrange(15):
    TestPig=Game.Pig(63.5,63.5,0,0)
    Game.Addentidy(Game.Entidies,TestPig)
    TestMouse=Game.Mouse(63.5,63.5,0,0)
    Game.Addentidy(Game.Entidies,TestMouse)
    
TestTreeman=Game.Treeman(63.5,63.5,0,0)
Game.Addentidy(Game.Entidies,TestTreeman)
#pygame.mixer.music.load("Datas/Music/Music1.mp3")
#pygame.mixer.music.play(-1)

flag=True
while flag:
    if Player.push==9:
        Player.bag[1]=Game.Item(1,64)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            flag=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mdownpos=[event.pos[0],event.pos[1]]
            ismdown=True
        elif event.type==pygame.MOUSEBUTTONUP:
            push([event.pos[0],event.pos[1]],mdownpos[:])
            ismdown=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                issdown=True
            elif event.key==pygame.K_F3:
                isf3down=True
            elif event.key==pygame.K_w:
                iswdown=True
            elif event.key>=pygame.K_0 and event.key<=pygame.K_9:
                Player.push=event.key-pygame.K_0
            elif event.key>=pygame.K_KP0 and event.key<=pygame.K_KP9:
                Player.push=event.key-pygame.K_KP0
        elif event.type==pygame.KEYUP:
            if editos:
                if event.key==pygame.K_BACKSPACE:
                    if editos.fpos>0:
                        editos.fpos-=1
                        editos.string=editos.string[:editos.fpos]+editos.string[editos.fpos+1:]
                        #print "K_Backspace Pushed Fpos="+str(editos.fpos)+" str="+editos.string
                elif event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                    issdown=False
                elif event.key==pygame.K_DELETE:
                    if editos.fpos<len(editos.string)-1:
                        editos.string=editos.string[:editos.fpos+1]+editos.string[editos.fpos+2:]
                elif event.key==13 or event.key==271:
                    #do some enter
                    print "Commsg:"+editos.string
                    #
                    commsg(editos.string)
                elif event.key in gtkey:
                    editos.fpos+=1
                    editos.string=editos.string+gtkey[event.key][int(issdown)]
            elif event.key==pygame.K_F3:
                isf3down=False
            elif event.key==pygame.K_r:
                if isf3down:
                    if gametype==0:
                        gametype=1
                        connect(1)
                    else:
                        gametype=0
                        connect(0)
            elif event.key==pygame.K_w:
                iswdown=False
                
                        
    mousepos=pygame.mouse.get_pos()
    mousepos=[mousepos[0],mousepos[1]]
    mx=(mousepos[0]-400)/32.0+Player.x
    my=(mousepos[1]-400)/32.0+Player.y
    if not ismdown:
        move(mousepos)
    else:
        pmove(mousepos,mdownpos[:],ismdown)
    ptoface=gface(mousepos[0],mousepos[1])
    #print ptoface
    Player.face=ptoface
    if iswdown:
        Game.move(0.3,Player)
    if time.time()-lastft>=1:
        lastft=time.time()
        Game.frame()
    if time.time()-lastgt>=0.05:
        lastgt=time.time()
        Game.execute()
    screen_redraw(gametype)
    
    pygame.display.flip()

Game.exit()
pygame.quit()
