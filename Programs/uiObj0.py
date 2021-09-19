import time,pickle,sys,math,random,os,AIDefinition,EntidyClass
sys.setrecursionlimit(1000000)

import Game
from MathDef import *
def Int_tSurface(num):
    l=len(str(num))
    res=pygame.Surface((4*l-1,5))
    res.fill((127,127,127))
    pos=4*l-4
    if num<0:
       res.blit(fontonege,(0,0))
       num=-num
    elif num==0:
       res.blit(fontonum[0],(0,0))
    while num:
        res.blit(fontonum[num%10],(pos,0))
        pos-=4
        num/=10
    res.set_colorkey((127,127,127))
    return res


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
    leftsurface=screen
    blockleast=[fl(Player.x)-13,fl(Player.y)-13]
    leftsurface.fill((255,255,255))
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
    for i in xrange(27):
        if blockleast[0]+i not in Game.SpeclEntidies:
            continue
        for j in xrange(27):
            if blockleast[1]+j not in Game.SpeclEntidies[blockleast[0]+i]:
                continue
            for ent in Game.SpeclEntidies[blockleast[0]+i][blockleast[1]+j]:
                scr=pygame.transform.rotate(ent.imgs[ent.img],ent.face)
                scr=scr.convert_alpha()
                rct=scr.get_rect()
                leftsurface.blit(scr,[400+(ent.x-Player.x)*32-rct.width/2,400+(ent.y-Player.y)*32-rct.height/2])
    rects=(400+32*(fl(mx)-Player.x),400+32*(fl(my)-Player.y))
    if howdealpoint:
        leftsurface.blit(howdealblocks[howdealpoint],rects)
    for i in xrange(10):
        if Player.push==i:
            leftsurface.blit(ltx[i],(TexBarx[i],600))
        else:
            leftsurface.blit(dtx[i],(TexBarx[i],600))
        leftsurface.blit(Game.ItemImgs[Player.bag[i].id][Player.bag[i].img],(TexBarx[i]+1,601))
        if Player.bag[i].cnt>1:
            leftsurface.blit(Int_tSurface(Player.bag[i].cnt),(TexBarx[i]+24,625))
    #32*200
    pygame.draw.rect(leftsurface,(0,0,0),(765,0,34,202),1)
    pygame.draw.rect(leftsurface,(128,128,128),(766,1,32,200),0)
    if fl(Player.life*2)>0:
        pygame.draw.rect(leftsurface,(255,127,127),(766,1,32,fl(Player.life*2)),0)
    nur=Int_tSurface(fl(Player.life))
    nur=pygame.transform.scale2x(nur)
    leftsurface.blit(nur,(782-nur.get_width()/2,102-nur.get_height()/2))
    #16*100
    pygame.draw.rect(leftsurface,(0,0,0),(747,0,18,102),1)
    pygame.draw.rect(leftsurface,(128,128,128),(748,1,16,100),0)
    if Game.ItemType[Player.bag[Player.push].id]==4 and Player.hunger<=100.0 and fl(Player.hunger+Game.EatGet[Player.bag[Player.push].id])>0:
        pygame.draw.rect(leftsurface,(255,220,55),(748,1,16,fl(Player.hunger+Game.EatGet[Player.bag[Player.push].id])),0)
    if fl(Player.hunger)>0:
        pygame.draw.rect(leftsurface,(255,165,0),(748,1,16,fl(Player.hunger)),0)

TexBarx=(528,240,272,304,336,368,400,432,464,496)
#[240+32*9]+[208+32*i for i in xrange(1,10)]
def screen_redraw_1():
    screen_redraw_0()
    screen.blit(gt1_comup,(1180,23))
    pygame.draw.rect(screen,blcol,(1180,46,350,35),2)
    gt0_re.draw(screen,(1185,54))
    xsf=Int_tSurface(fl(Player.x/32))
    ysf=Int_tSurface(fl(Player.y/32))
    xsf=pygame.transform.scale2x(xsf)
    xsf=pygame.transform.scale2x(xsf)
    ysf=pygame.transform.scale2x(ysf)
    ysf=pygame.transform.scale2x(ysf)
    screen.blit(xsf,(0,0))
    screen.blit(ysf,(xsf.get_width()+16,0))
#
def decrease_bag(which):
    Player.bag[which].cnt-=1
    if not Player.bag[which].cnt:
        Player.bag[which]=Game.Item(0,0)
def push_0(pos,lpos):
    global editos
    editos=0
    flmx=fl(mx)
    flmy=fl(my)
    dx=flmx-Player.x
    dy=flmy-Player.y
    if Game.ItemType[Player.bag[Player.push].id]==1:
        if min(dx*dx,(dx+1)*(dx+1))+min(dy*dy,(dy+1)*(dy+1))<=9.0:#3*3
            bet=(Game.ToBlock[Player.bag[Player.push].id])(flmx+0.5,flmy+0.5,0,0)
            if Game.CanPush(bet):
                Game.SetBlockentidy(Game.BlockEntidies,bet)
                decrease_bag(Player.push)
    elif Game.ItemType[Player.bag[Player.push].id]==2:
        atk=Game.Attack(Player.x-0.35*math.sin(Player.face/radp),Player.y-0.35*math.cos(Player.face/radp),Player.face,0,0.3,1e6,1)
        Player.atkbl.add(atk)
        Game.Addentidy(Game.SpeclEntidies,atk)
        #res=Game.Cat(Player.x-10*math.sin(Player.face/radp),Player.y-10*math.cos(Player.face/radp))
        #Game.Addentidy(Game.SpeclEntidies,res)
        #1tick=0.05s
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
    if Game.ItemType[Player.bag[Player.push].id] in (1,3):
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
def pushend(pos,lpos):
    global digtime
    digtime=0
def tickdo():
    global digtime,digpos,eattime
    flmx=fl(mx)
    flmy=fl(my)
    flpx=fl(Player.x)
    flpy=fl(Player.y)
    if Player.life>=0 and Game.Blockos[flpx][flpy] in {6,9}:
        Player.life-=2.5
    dx=flmx-Player.x
    dy=flmy-Player.y
    if ismdown:
        if Game.ItemType[Player.bag[Player.push].id]==3 and \
           min(dx*dx,(dx+1)*(dx+1))+min(dy*dy,(dy+1)*(dy+1))<=9.0 and \
           flmx in Game.BlockEntidies and \
           flmy in Game.BlockEntidies[flmx] and \
           Player.bag[Player.push].id in Game.BlockEntidies[flmx][flmy].CanBroke:
            if digpos==(flmx,flmy):
                digtime+=1
                if digtime*Game.PickaxeSpeed[Player.bag[Player.push].id]>=Game.BlockEntidies[flmx][flmy].Hardnum:
                    Game.Addentidy(Game.SpeclEntidies,Game.Dropitem(flmx+random.random()*1.5-0.25,flmy+random.random()*1.5-0.25,Game.Item(Game.ToItem[Game.BlockEntidies[flmx][flmy].type],1)))
                    del Game.BlockEntidies[flmx][flmy]
                    digtime=0
            else:
                digpos=(flmx,flmy)
                digtime=0
        elif Game.ItemType[Player.bag[Player.push].id]==4 and \
             Player.hunger<=100.0:
            eattime+=1
            if eattime>=Game.EatTime[Player.bag[Player.push].id]:
                Player.hunger+=Game.EatGet[Player.bag[Player.push].id]
                decrease_bag(Player.push)
                eattime=0
def spawnblock(x,y):
    if Game.Blockos[x][y]==2:
        if random.random()<0.2:
            Game.Addentidy(Game.Entidies,Game.Pig(x+.5,y+.5,0,0))
            Game.Addentidy(Game.Entidies,Game.Pig(x+.5,y+.5,0,0))
            Game.Addentidy(Game.Entidies,Game.Pig(x+.5,y+.5,0,0))
def Spawndo():
    flpx=fl(Player.x)
    flpy=fl(Player.y)
    cnt=0
    for dx in xrange(-20,21):
        if dx in Game.Entidies:
            for dy in xrange(-20,21):
                if dy in Game.Entidies[dx]:
                    cnt+=len(Game.Entidies[dx][dy])
    if cnt<50:
        r=random.random()
        spawnblock(flpx+(r<0.5)*random.randint(-20,-13),flpy+(0.75<=r or r<0.25)*random.randint(-20,-13))
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
def main(pg,gtkey,sed):
    global gametype,errimg,blockimg,GBlock,BBlock,bgcol,blcol,dtx,ltx,fontonum, \
fontonege,fonto_10,fonto_20,gt1_comup,howdealpoint,howdealblocks,mx,my,Player, \
ismdown,digtime,digpos,screen,pygame,editpos,editos,edith,eattime
    pygame=pg
    pygame.init()
    AI_class_decide=1
    gametype=0
    #0~... (0:main 10:sandbox 20:multiplas)

    errimg=pygame.image.load("Datas/Block/blockerr.bmp")
    blockimg=[errimg for i in xrange(0,100)]
    for i in range(1,15)+[17,20]:
        blockimg[i]=pygame.image.load("Datas/Block/block%d.bmp"%(i,))
    
    Gblock=pygame.image.load("Datas/GBlock.bmp")
    Bblock=pygame.image.load("Datas/BBlock.bmp")

    Gblock.set_alpha(127)
    Bblock.set_alpha(127)


    bgcol=(255,255,255)
    blcol=(0,0,0)

    version="Tuohuangzhe Pre-40 With Pygame"

    dtx=[]
    ltx=[]
    for i in xrange(10):
        dtx.append(pygame.image.load("Datas/Tex%d.bmp"%(i,)))
        ltx.append(pygame.image.load("Datas/LTex%d.bmp"%(i,)))
        dtx[-1].set_alpha(127)
        ltx[-1].set_alpha(127)
    fontonum=[]
    for i in xrange(10):
        fontonum.append(pygame.image.load("Datas/Font/Font%d.bmp"%(i,)))
    fontonege=pygame.image.load("Datas/Font/Nege.bmp")
    fonto_10=pygame.font.Font(None,10)
    fonto_20=pygame.font.Font(None,20)
    gt1_comup=fonto_20.render(version,False,blcol,bgcol)
    
    mdownpos=[]
    ismdown=False#mousekey
    
    issdown=False#shift
    iswdown=False#W
    isedown=False#E

    editpos=[0,0]
    edith=23
    editos=0

    bgeditos=[]

    howdealpoint=0
    howdealblocks={1:Gblock,2:Bblock}

    Game.init(sed)
    screen=pygame.display.set_mode((800,800))#0~799 0~799
    lastgt=lastft=lastht=0
    ecnt=0
    digtime=0
    digpos=(0.5,0.5)






    connect(gametype)


    print "Game Executing"
    Player=Game.Steve(63.5,63.5,0,0)
    Game.Peoples.append(Player)
    Game.Addentidy(Game.Entidies,Player)
    Player.push=1
    for i in xrange(15):
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
            Player.bag[2]=Game.Item(233,1)
            Player.bag[3]=Game.Item(234,1)
            Player.bag[4]=Game.Item(235,1)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                Game.exit()
                return True
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mdownpos=[event.pos[0],event.pos[1]]
                push([event.pos[0],event.pos[1]],mdownpos[:])
                ismdown=True
            elif event.type==pygame.MOUSEBUTTONUP:
                pushend([event.pos[0],event.pos[1]],mdownpos[:])
                ismdown=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                    issdown=True
                elif event.key==pygame.K_w:
                    iswdown=True
                elif event.key==pygame.K_e:
                    isedown=True
                elif event.key>=pygame.K_0 and event.key<=pygame.K_9:
                    Player.push=event.key-pygame.K_0
                    digtime=eattime=0
                elif event.key>=pygame.K_KP0 and event.key<=pygame.K_KP9:
                    Player.push=event.key-pygame.K_KP0
                    digtime=eattime=0
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
                    if gametype==0:
                        gametype=1
                        connect(1)
                    else:
                        gametype=0
                        connect(0)
                elif event.key==pygame.K_r:
                    Game.Addentidy(Game.Entidies,Game.tmpNPC(1,Player.x+5,Player.y+5,0,0))
                elif event.key==pygame.K_w:
                    iswdown=False
                elif event.key==pygame.K_e:
                    isedown=False

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
        elif isedown:
            Game.move(0.15,Player)
        tme=time.time()
        if tme-lastft>=1:
            lastft=tme
            Game.frame()
            #while 1:
            #    f=random.random()*360-180
            #    if min(f+360-Player.face,Player.face+360-f,abs(f-Player.face))>=60:
            #        break
            #res=Game.Cat(Player.x-15*math.sin(f/radp),Player.y-15*math.cos(f/radp))
            #Game.Addentidy(Game.SpeclEntidies,res)
        if tme-lastht>=5:
           AI_class_decide=-AI_class_decide
           if AI_class_decide == 1 :
               AIDefinition.Pig.AI=AIDefinition.BackAI(0.875,0.07)
           if AI_class_decide == -1 :
               EntidyClass.Pig.AI=AIDefinition.WalkAI(0.875,0.07)
           lastht=tme
           Player.hunger-=2.5
           if Player.hunger<=0:
               Player.life+=Player.hunger*0.2
           Spawndo()
        if tme-lastgt>=0.05:
            lastgt=tme
            tickdo()
            Game.execute()
        screen_redraw(gametype)
        pygame.display.flip()
    Game.exit()
    return