import pygame,time
def pus(pos):
    if pos[1]>=600 and pos[1]<700 and pos[0]<200:
        return True
def main(pg):
    global pygame
    pygame=pg

    pygame.init()
    screen=pygame.display.set_mode((800,800))
    bg=pygame.image.load("Datas10/bg.bmp")
    butn=pygame.image.load("Datas10/butn.bmp")
    butm=pygame.image.load("Datas10/butm.bmp")
    ft=pygame.font.Font(None,50)
    sfs=(ft.render("Start",False,(0,0,0),(153,217,234)),ft.render("Load",False,(0,0,0),(153,217,234)),\
         ft.render("About",False,(0,0,0),(153,217,234)),ft.render("Setting",False,(0,0,0),(153,217,234)))
    for e in sfs:
        e.set_colorkey((153,217,234))
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return True
            elif event.type==pygame.MOUSEBUTTONUP:
                if pus(event.pos):
                    return
        screen.blit(bg,(0,0))
        screen.blit(butn,(0,600))
        screen.blit(butn,(200,600))
        screen.blit(butn,(400,600))
        screen.blit(butn,(600,600))
        pos=pygame.mouse.get_pos()
        if pos[1]>=600 and pos[1]<700:
            screen.blit(butm,(pos[0]/200*200,600))
        for i in (0,1,2,3):
            screen.blit(sfs[i],(100+200*i-sfs[i].get_width()/2,650-sfs[i].get_height()/2))
        pygame.display.flip()
