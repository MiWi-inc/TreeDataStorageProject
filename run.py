import pygame, sys, os, math, time, random
from pygame.math import Vector2

from quadtreeBase import QuadTreeNode


class Game(object):


    def __init__(self):
        
        pygame.init()
        #config
        self.Xres = 1900
        self.Yres = 1010
        self.w = self.Xres
        self.h = self.Yres
        self.tps = 100.0
        bgColor = (23, 23, 34)
        self.debugMode = True
        self.appFolder = os.path.dirname(os.path.abspath(__file__))
        self.full_path = os.path.join(self.appFolder, "agency_fb.ttf")
        self.font = pygame.font.Font(self.full_path, 20)
        self.font2 = pygame.font.Font(self.full_path, 15)
        self.font3 = pygame.font.Font(self.full_path, 18)

        #menu
        self.menuWidth = 400
        self.menuX = self.Xres - self.menuWidth
        self.baseColor = (126, 150, 189)
        self.inactiveColor = (40, 54, 77)

        #initialization
        self.screen = pygame.display.set_mode((self.Xres, self.Yres))
        self.tpsClock = pygame.time.Clock()
        self.tpsDelta = 0.0

        self.maxLvl = 7
 
        self.qt = QuadTreeNode(self, None, 5, 5, 1000, 1000, self.maxLvl)

        self.placementLvl = 0
        # self.objects.append(Node(self, Vector2(240, 400)))      #0

        self.quadtreeNodeMemory = 44.125 # B
        self.nodeCount = 0

        self.color = (0, 0, 0)
        self.R = 0
        self.G = 0
        self.B = 0

        self.barY = 150
        self.barLen = 255
        self.barSpacing=30
        self.radius = 0
        self.moved = False
    
        while True:
            self.screen.fill(bgColor)
            self.color = (self.R, self.G, self.B)
            
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.placeDataPoint(pygame.mouse.get_pos(), self.color, self.placementLvl)

                            
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
                
                if event.type == pygame.MOUSEMOTION:
                    pass
                    if pygame.mouse.get_pressed()[0]:
                        self.placeDataPoint(pygame.mouse.get_pos(), self.color, self.placementLvl)

            if pygame.mouse.get_pressed() == (1, 0, 0):
                if pygame.mouse.get_pos()[1] > self.barY+3-self.barSpacing/2 and pygame.mouse.get_pos()[1] < self.barY+28-self.barSpacing/2 and pygame.mouse.get_pos()[0] >= self.w-self.menuWidth+54 and pygame.mouse.get_pos()[0] <= self.w-self.menuWidth+54+self.barLen:
                    self.R = (pygame.mouse.get_pos()[0] - (self.w-self.menuWidth+54))
                if pygame.mouse.get_pos()[1] > self.barY+3+self.barSpacing-self.barSpacing/2 and pygame.mouse.get_pos()[1] < self.barY+28+self.barSpacing-self.barSpacing/2 and pygame.mouse.get_pos()[0] >= self.w-self.menuWidth+54 and pygame.mouse.get_pos()[0] <= self.w-self.menuWidth+54+self.barLen:
                    self.G = (pygame.mouse.get_pos()[0] - (self.w-self.menuWidth+54))
                if pygame.mouse.get_pos()[1] > self.barY+3+2*self.barSpacing-self.barSpacing/2 and pygame.mouse.get_pos()[1] < self.barY+28+2*self.barSpacing-self.barSpacing/2 and pygame.mouse.get_pos()[0] >= self.w-self.menuWidth+54 and pygame.mouse.get_pos()[0] <= self.w-self.menuWidth+54+self.barLen:
                    self.B = (pygame.mouse.get_pos()[0] - (self.w-self.menuWidth+54))     
                if pygame.mouse.get_pos()[1] > self.barY+3+3*self.barSpacing-self.barSpacing/2 and pygame.mouse.get_pos()[1] < self.barY+28+3*self.barSpacing-self.barSpacing/2 and pygame.mouse.get_pos()[0] >= self.w-self.menuWidth+54 and pygame.mouse.get_pos()[0] <= self.w-self.menuWidth+54+self.barLen:
                    self.radius = (pygame.mouse.get_pos()[0] - (self.w-self.menuWidth+54))*self.maxLvl/255
                    self.placementLvl = round(self.radius)


            #Ticking
            self.tpsDelta += self.tpsClock.tick()/1000.0
            while self.tpsDelta > 1/self.tps:
                self.tpsDelta -=1/self.tps

            
            self.draw()
            
            pygame.display.flip()

    def placeDataPoint(self, point, data, lvl):
        self.qt.insert(point, data, lvl)
        self.nodeCount = self.qt.countNodes()


    def draw(self):

        infoRect = pygame.Rect(self.menuX, 0, self.menuWidth, self.Yres)
        pygame.draw.rect(self.screen, (13, 13, 26), infoRect)

        self.qt.show()
        #self.qt.treeShow(1000, 20)
        
        if self.debugMode:
            text = self.font.render("FPS: " + str(int(self.tpsClock.get_fps())) , True, (0, 255, 0))
            self.screen.blit(text, (10,10))

        text = self.font.render("Memory used: " + str((self.quadtreeNodeMemory * self.nodeCount)/1024) + " KiB" , True, (0, 255, 0))
        self.screen.blit(text, (1030,10))

        pygame.draw.circle(self.screen, (self.R, self.G, self.B), (self.w-self.menuWidth/2, 40), (1000/(2**(self.maxLvl - self.placementLvl)))/2)

        textR = self.font3.render('R: ' + str(self.R), True, (146, 146, 178))
        self.screen.blit(textR,(self.w-self.menuWidth+10, 141))
        textG = self.font3.render('G: ' + str(self.G) , True, (146, 146, 178))
        self.screen.blit(textG,(self.w-self.menuWidth+10, 171))
        textB = self.font3.render('B: ' + str(self.B) , True, (146, 146, 178))
        self.screen.blit(textB,(self.w-self.menuWidth+10, 201))
        textR = self.font3.render('S: ' + str(self.placementLvl) , True, (146, 146, 178))
        self.screen.blit(textR,(self.w-self.menuWidth+10, 231))

        pygame.draw.line(self.screen, (72, 72, 82), (self.w-self.menuWidth+54, self.barY), (self.w-self.menuWidth+54+self.barLen, self.barY), width=2)
        pygame.draw.line(self.screen, (72, 72, 82), (self.w-self.menuWidth+54, self.barY+self.barSpacing), (self.w-self.menuWidth+54+self.barLen, self.barY+self.barSpacing), width=2)
        pygame.draw.line(self.screen, (72, 72, 82), (self.w-self.menuWidth+54, self.barY+2*self.barSpacing), (self.w-self.menuWidth+54+self.barLen, self.barY+2*self.barSpacing), width=2)
        pygame.draw.line(self.screen, (72, 72, 82), (self.w-self.menuWidth+54, self.barY+3*self.barSpacing), (self.w-self.menuWidth+54+self.barLen, self.barY+3*self.barSpacing), width=2)

        br = pygame.Rect((self.w-self.menuWidth+54)+self.R, self.barY+3-self.barSpacing/2,  5, 25)
        bg = pygame.Rect((self.w-self.menuWidth+54)+self.G, self.barY+3+self.barSpacing-self.barSpacing/2,  5, 25)
        bb = pygame.Rect((self.w-self.menuWidth+54)+self.B, self.barY+3+2*self.barSpacing-self.barSpacing/2,  5, 25)
        brad = pygame.Rect((self.w-self.menuWidth+54)+self.placementLvl*255/self.maxLvl, self.barY+3+3*self.barSpacing-self.barSpacing/2,  5, 25)

        pygame.draw.rect(self.screen, (191, 0, 61), br)
        pygame.draw.rect(self.screen, (0, 176, 93), bg)
        pygame.draw.rect(self.screen, (0, 124, 178), bb)
        pygame.draw.rect(self.screen, (72, 72, 82), brad)


if __name__ == "__main__":
    Game()
