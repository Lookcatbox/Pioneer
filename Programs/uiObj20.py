import pygame,time
class edito:
    def __init__(self,ls,height,fontis):
        self.lside=ls
        self.high=height
        self.string=""
        self.fpos=0
        self.fonto=fontis
    def draw(self,scr,where):
        scr.blit(self.fonto.render(self.string,False,(0,0,0),(255,255,255)),where)
        #screen.draw()
def main(pg,gtkey):
    global pygame,editpos,editos,edith
    pygame=pg

    pygame.init()
    screen=pygame.display.set_mode((800,800))
    bg=pygame.image.load("Datas20/bg.bmp")

    editium=edito(100,100,pygame.font.Font(None,50))
    editpos=[0,0]
    edith=23
    editos=0
    issdown=False
    
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return True
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.pos[0]>=100 and event.pos[0]<700 and event.pos[1]>=600 and event.pos[1]<700:
                    editos=editium
                else:
                    editos=0
            #...
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                    issdown=True
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
                        try:
                            return int(editos.string)
                        except:
                            pass
                    elif event.key in gtkey:
                        editos.fpos+=1
                        editos.string=editos.string+gtkey[event.key][int(issdown)]
        pos=pygame.mouse.get_pos()
        screen.blit(bg,(0,0))
        pygame.draw.rect(screen,(0,0,0),(100,600,600,100),10)
        if editos:
            editos.draw(screen,(125,625))
        pygame.display.flip()
