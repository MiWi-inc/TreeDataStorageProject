import pygame, sys, os, math, time, random
from pygame.math import Vector2

from item import Item
from quadtreeBase import QuadTreeNode


class Game(object):


    def __init__(self):
        
        pygame.init()
        #config
        self.Xres = 1900
        self.Yres = 1010
        self.tps = 100.0
        bgColor = (23, 23, 34)
        self.debugMode = True
        self.appFolder = os.path.dirname(os.path.abspath(__file__))
        self.full_path = os.path.join(self.appFolder, "agency_fb.ttf")
        self.font = pygame.font.Font(self.full_path, 20)
        self.font2 = pygame.font.Font(self.full_path, 15)

        #menu
        self.menuWidth = 400
        self.menuX = self.Xres - self.menuWidth
        self.baseColor = (126, 150, 189)
        self.inactiveColor = (40, 54, 77)
        self.buttonPressed = True
             

        #initialization
        self.screen = pygame.display.set_mode((self.Xres, self.Yres))
        self.tpsClock = pygame.time.Clock()
        self.tpsDelta = 0.0

        self.points = []
 
        self.qt = QuadTreeNode(self, 5, 5, 1000, 1000, 1)

    
        # self.objects.append(Node(self, Vector2(240, 400)))      #0
    
        while True:
            self.screen.fill(bgColor)

            
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
                
                if event.type == pygame.MOUSEMOTION:
                    pass


            #Ticking
            self.tpsDelta += self.tpsClock.tick()/1000.0
            while self.tpsDelta > 1/self.tps:
                self.tick()
                self.tpsDelta -=1/self.tps

            
            self.draw()
            
            pygame.display.flip()

    def tick(self):
        # self.qt = QuadTree2D(self, 0, 0, 1000, 1000, 1)
        # for i in self.points:
        #     self.qt.insertPoint(i)

        # for i in self.points:
        #     i.gravitate(self.qt)
        pass

    def draw(self):

        infoRect = pygame.Rect(self.menuX, 0, self.menuWidth, self.Yres)
        pygame.draw.rect(self.screen, (13, 13, 26), infoRect)

        self.qt.show()
        # self.qt.treeShow(1000, 20)

        for i in self.points:
            pygame.draw.circle(self.screen, i.color, (i.x, i.y), 4)
        
        if self.debugMode:
            text = self.font.render("FPS: " + str(int(self.tpsClock.get_fps())) , True, (0, 255, 0))
            self.screen.blit(text, (10,10))


if __name__ == "__main__":
    Game()
