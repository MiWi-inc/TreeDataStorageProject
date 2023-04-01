import pygame, sys, os, math
from pygame.math import Vector2

class QuadTreeNode:

    def __init__(self, app, parent, x, y, w, h, lvl):

        self.app = app

        self.parent = parent
        self.subNodes = []
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.lvl = lvl

        self.content = None
        self.divided = False
        

    def intersect(self, area):
        if self.x > area[0]+area[2] or self.x+self.w < area[0] or self.y > area[1]+area[3] or self.y+self.h < area[1]:
            return False
        else:
            return True

    def contain(self, point):
        if point[0] > self.x and point[0] <= self.x+self.w and point[1] > self.y and point[1] <= self.y+self.h:
            return True
        else: 
            return False
    
    def dist(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)

    def divide(self):
        self.subNodes.append(QuadTreeNode(self.app, self, self.x, self.y, self.w/2, self.h/2, self.lvl-1))
        self.subNodes.append(QuadTreeNode(self.app, self, self.x+self.w/2, self.y, self.w/2, self.h/2, self.lvl-1))
        self.subNodes.append(QuadTreeNode(self.app, self, self.x, self.y+self.h/2, self.w/2, self.h/2, self.lvl-1))
        self.subNodes.append(QuadTreeNode(self.app, self, self.x+self.w/2, self.y+self.h/2, self.w/2, self.h/2, self.lvl-1))
        self.divided = True

    def insert(self, point, data, lvl):
        
        if self.contain(point):
            if self.divided and self.lvl > lvl:
                for i in self.subNodes:
                    i.insert(point, data, lvl)
            elif(self.lvl == lvl):
                self.content = data
                self.subNodes = []
                self.divided = False
                self.updateParent()
            elif(self.lvl == 0):
                self.content = data
                self.updateParent()
            elif(not self.divided and self.lvl > lvl and self.lvl > 0):
                self.divide()
                self.content = None
                for i in self.subNodes:
                    i.insert(point, data, lvl)

    def findPoints(self, area, target = []):
        if self.intersect(area):
            if self.divided:
                for i in self.subNodes:
                    i.findPoints(area, target)
            else:
                for i in self.content:
                    if area.collidepoint(i.x, i.y):
                        target.append(i)
        return target

    def updateParent(self):
        if(self.divided):
            for i in self.subNodes:
                if(i.content != self.subNodes[0].content):
                    return
            self.content = self.subNodes[0].content
            self.divided = False
            self.subNodes = []
        if(self.parent != None):
            self.parent.updateParent()

    def show(self):
        if self.divided:
            rect = pygame.Rect(self.x, self.y, self.w, self.h)
            pygame.draw.rect(self.app.screen, (255, 255, 255), rect, width=1)
            for i in self.subNodes:
                i.show()
        else:
            rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if(self.content != None):
                pygame.draw.rect(self.app.screen, (255, 0, 0), rect)
            pygame.draw.rect(self.app.screen, (255, 255, 255), rect, width=1)

    def treeShow(self, x, y, w=800, layer = 0, sub = 0):

        xOld = x

        if self.divided:

            if layer == 0:
                x = x+(w/2)
            else:
                x = x + (sub-2)*24

            for index, i in enumerate(self.subNodes):
                i.treeShow(x, y, w, (layer+1), index)
            if layer != 0:
                pygame.draw.line(self.app.screen, (255, 255, 255), (xOld, y+35*(layer-1)), (x, y+35*layer))
            pygame.draw.circle(self.app.screen, (200, 200, 200), (x, y+35*layer), 12)
            pygame.draw.circle(self.app.screen, (255, 255, 255), (x, y+35*layer), 12, width=1)
            text = self.app.font2.render(str(self.M) , True, (255, 0, 0))
            self.app.screen.blit(text, (x, y+35*layer-10))
        else:
            xOld = x
            if layer == 0:
                x = x+(w/2)
            else:
                x = x + (sub-2)*20
            if len(self.content) > 0:
                color = (217, 105, 74)
            else:
                color = (200, 200, 200)
            if layer != 0:
                pygame.draw.line(self.app.screen, (255, 255, 255), (xOld, y+35*(layer-1)), (x, y+35*layer))
            pygame.draw.circle(self.app.screen, color, (x, y+35*layer), 12)
            pygame.draw.circle(self.app.screen, (255, 255, 255), (x, y+35*layer), 12, width=1)
            text = self.app.font2.render(str(self.M) , True, (255, 0, 0))
            self.app.screen.blit(text, (x, y+35*layer-10))
