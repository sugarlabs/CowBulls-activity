import random
import pygame, sys
from pygame.locals import *


X = 900
Y = 250
XX = 60
YY = 30
margin = 10
img = pygame.image.load('icons/dialpad/1.png')
img = pygame.transform.smoothscale(img, (70, 70))
XGAP = 10 + img.get_rect().size[0]
YGAP = 10 + img.get_rect().size[1]

mmmp = pygame.image.load('icons/status/cow.png')
mmmp = pygame.transform.smoothscale(mmmp, (50, 50))
XXXGAP = 10+ mmmp.get_rect().size[0]

TRIES = 0
NumberEntered = []

Numbers = {
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_0: '0',
    pygame.K_KP0: '0',
    pygame.K_KP1: '1',
    pygame.K_KP2: '2',
    pygame.K_KP3: '3',
    pygame.K_KP4: '4',
    pygame.K_KP5: '5',
    pygame.K_KP6: '6',
    pygame.K_KP7: '7',
    pygame.K_KP8: '8',
    pygame.K_KP9: '9',
}


class CowBulls:
    def __init__(self):
        self.num = random.randint(100,999)
        self.num = [int(x) for x in str(self.num)]
        self.won = False
        self.lost = False

    def display(self):
        global imgx
        screen = pygame.display.get_surface()
        for y in range(3):
            for x in range(3):
                img = pygame.image.load('icons/dialpad/' + str(1+x + 3*y)+ '.png')
                img = pygame.transform.smoothscale(img, (70, 70))
                screen.blit(img, (X +x*(10+ img.get_rect().size[0]), Y + y*YGAP))
        img = pygame.image.load('icons/dialpad/0.png')
        img = pygame.transform.smoothscale(img, (70, 70))
        print img.get_rect().size[0]
        screen.blit(img, (X +1*(10+ img.get_rect().size[0]), Y + 3*YGAP))

        img2 = pygame.image.load('icons/dialpad/tick.png')
        img2 = pygame.transform.smoothscale(img2, (70, 70))
        screen.blit(img2, (X, Y + 3*YGAP))

        img3 = pygame.image.load('icons/dialpad/cancel.png')
        img3 = pygame.transform.smoothscale(img3, (70, 70))
        screen.blit(img3, (X +2*(10+ img.get_rect().size[0]), Y + 3*YGAP))

        for x in range(3):
            img3 = pygame.image.load('icons/dialpad/entry.png')
            img3 = pygame.transform.smoothscale(img3, (70, 20))
            screen.blit(img3, (X +x*(10+ img.get_rect().size[0]), Y - 0.7*YGAP))

        for x in range(3):
            img3 = pygame.image.load('icons/entries/question.png')
            img3 = pygame.transform.smoothscale(img3, (50, 50))
            screen.blit(img3, (XX +x*(10+ img3.get_rect().size[0]), YY))
            imgx = pygame.image.load('icons/dialpad/entry.png')
            imgx = pygame.transform.smoothscale(imgx, (50, 10))
            screen.blit(imgx, (XX +x*(10+ img3.get_rect().size[0]), YY + (img3.get_rect().size[1])))

            img4 = pygame.image.load('icons/status/bull.png')
            img4 = pygame.transform.smoothscale(img4, (50, 50))
            screen.blit(img4, (XX +(3.5+x)*(10+ img4.get_rect().size[0]), YY))
            
    def get_input(self, key):
        if key in Numbers:
            return Numbers[key]
        else:
            return None

    def put_num(self, valy):
        if len(NumberEntered)<3:
            img3 = pygame.image.load('icons/dialpad/' + valy + '.png')
            img3 = pygame.transform.smoothscale(img3, (70, 70))
            screen.blit(img3, (X + len(NumberEntered)*(10+ img3.get_rect().size[0]), Y - 1.6*YGAP))
            NumberEntered.append(int(valy))

    def delete(self):
        if (len(NumberEntered)!=0):
            pygame.draw.rect(pygame.display.get_surface(), (200,200,200), (X + (len(NumberEntered)-1)*(XGAP), Y - 1.6 * YGAP, img.get_rect().size[1],img.get_rect().size[1]))
            NumberEntered.pop()

    def do_button(self, pos):
        pos = ((pos[0]-X)/XGAP), ((pos[1]-Y)/YGAP)
        num = (pos[1]*3 + pos[0] + 1)
        if num > 0 and num <= 9:
            self.put_num(str(num))
        elif num == 10:
            self.enter()
        elif num == 11:
            self.put_num(str(0))
        elif num == 12:
            self.delete()

    def try_display(self):
        global TRIES
        tt = TRIES + 1
        for x in range(3):
            img3 = pygame.image.load('icons/entries/' + str(NumberEntered[x])+'.png')
            img3 = pygame.transform.smoothscale(img3, (50, 50))
            screen.blit(img3, (XX +x*(10+ img3.get_rect().size[0]), YY + tt*(10+ img3.get_rect().size[1])))
            if self.num[x] == NumberEntered[x]:
                img3 = pygame.image.load('icons/status/bull.png')
                img3 = pygame.transform.smoothscale(img3, (50, 50))
                screen.blit(img3, (XX +(3.5+x)*(XXXGAP), YY + tt*(XXXGAP)))
            elif NumberEntered[x] in self.num:
                img3 = pygame.image.load('icons/status/cow.png')
                img3 = pygame.transform.smoothscale(img3, (50, 50))
                screen.blit(img3, (XX +(3.5+x)*(XXXGAP), YY + tt*(XXXGAP)))
            else:
                img3 = pygame.image.load('icons/status/cancel.png')
                img3 = pygame.transform.smoothscale(img3, (50, 50))
                screen.blit(img3, (XX +(3.5+x)*(XXXGAP), YY + tt*(XXXGAP)))


    def enter(self):
        global TRIES
        if len(NumberEntered)!=3:
            pass
        else:
            self.try_display()
            TRIES=TRIES + 1
            screen = pygame.display.get_surface()
            if NumberEntered == self.num:
                img3 = pygame.image.load('icons/won.png')
                screen.blit(img3, (550,50))
                self.won = True
            elif TRIES==5:
                screen.set_alpha(100)
                screen.fill((200,200,200, 100))
                img3 = pygame.image.load('icons/lost.png')
                screen.blit(img3, (550,50))
                self.lost = True
            [self.delete() for x in range(3)]
                


    def run(self):
        self.display()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif not (self.won or self.lost):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.do_button(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        valy = self.get_input(event.key)
                        if valy:
                            self.put_num(valy)
                        elif event.key == pygame.K_BACKSPACE:
                            self.delete()
                        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            self.enter()
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1200, 700))
    pygame.display.set_caption('CowBulls')
    screen = pygame.display.get_surface()
    screen.fill((200,200,200))
    game = CowBulls()
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
