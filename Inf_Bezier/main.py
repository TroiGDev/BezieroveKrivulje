import pygame
import sys
import math

pygame.init()
screenWidth = 600
screenHeight = 400
screen = pygame.display.set_mode((screenWidth, screenHeight))

#colors
c_background = (18, 18, 18)

c_end = (255, 0, 0)
c_end_sdw = (150, 0, 0)

c_anchor = (0, 0, 255)
c_anchor_sdw = (0, 0, 150)

c_line = (150, 150, 150)

c_floor_sdw = (0, 0, 0)

#---------------------------------------------------------------------------------------------------------

class point:
    def __init__(self, x, y, pointWidth, color, sdw_color):

        self.x = x
        self.y = y

        self.pointWidth = pointWidth
        self.color = color
        self.sdw_color = sdw_color

    def draw(self):
        #draw point circle
        pygame.draw.circle(screen, self.sdw_color, (self.x, self.y + self.pointWidth/2), self.pointWidth)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.pointWidth)

    def draw_sdw(self):
        #draw floor shadow
        pygame.draw.circle(screen, c_floor_sdw, (self.x, self.y + floorHeight), self.pointWidth)


class curve:
    def __init__(self, x, y, lineWidth):
        curves.append(self)

        self.x = x
        self.y = y

        self.lineWidth = lineWidth

        self.points = []
        self.end1 = point(self.x - 50, self.y + 50, end_width, c_end, c_end_sdw)
        self.points.append(self.end1)
        self.anchor1 = point(self.x, self.y, anchor_width, c_anchor, c_anchor_sdw)
        self.points.append(self.anchor1)
        self.end2 = point(self.x + 50, self.y - 50, end_width, c_end, c_end_sdw)
        self.points.append(self.end2)

    def draw(self):
        #draw circle shadows
        self.anchor1.draw_sdw()
        self.end1.draw_sdw()
        self.end2.draw_sdw()

        #draw connection lines floor shadow
        pygame.draw.line(screen, c_floor_sdw, (self.end1.x, self.end1.y + floorHeight), (self.anchor1.x, self.anchor1.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor1.x, self.anchor1.y + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)

        #draw connection lines
        pygame.draw.line(screen, c_line, (self.end1.x, self.end1.y), (self.anchor1.x, self.anchor1.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor1.x, self.anchor1.y), (self.end2.x, self.end2.y), self.lineWidth)

        #draw circles
        self.anchor1.draw()
        self.end1.draw()
        self.end2.draw()
#-------------------------------------------------------------------------------------------------------------

class mousePointMover:
    def __init__(self):
        self.isHolding = False
        self.grabDistance = 25
        self.grabbedPoint = None

    def grabPoint(self):
        #get mouse pos
        mPos = pygame.mouse.get_pos()
        mX = mPos[0]
        mY = mPos[1]

        #get closest point
        closestMag = self.grabDistance
        closestPoint = None
        for curve in curves:
            for point in curve.points:
                #get distance to point
                vX = mX - point.x
                vY = mY - point.y

                mag = math.sqrt(vX * vX + vY * vY)
                
                #comapare distances
                if mag < closestMag and mag < self.grabDistance:
                    closestMag = mag
                    closestPoint = point
    
        #if found point
        if closestPoint != None and self.isHolding == False:
            self.grabbedPoint = closestPoint
            self.isHolding = True

    def movePoint(self):
        #get mouse pos
        mPos = pygame.mouse.get_pos()
        mX = mPos[0]
        mY = mPos[1]

        #set grabbed points pos to mouse pos
        self.grabbedPoint.x = mX
        self.grabbedPoint.y = mY

    def dropPoint(self):
        #clear grabbed point, set isholding to false
        self.grabbedPoint = None
        self.isHolding = False

#initialize mouse mover
hand = mousePointMover()

#-----------------------------------------------------------------------------------------------------
#move camera
cameraSpeed = 0.1

def moveCamera(xdif, ydif):
    #get every point and move it opposite
    for curve in curves:
        for point in curve.points:
            point.x -= xdif * cameraSpeed
            point.y -= ydif * cameraSpeed

#-----------------------------------------------------------------------------------------------------

#initialize curves
end_width = 7
anchor_width = 6
floorHeight = 30
curves = []

curve1 = curve(screenWidth/2, screenHeight/2, 2)

#-----------------------------------------------------------------------------------------------------

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #handle point movement with mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                hand.grabPoint()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                hand.dropPoint()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moveCamera(0, -1)
    if keys[pygame.K_a]:
        moveCamera(-1, 0)
    if keys[pygame.K_s]:
        moveCamera(0, 1)
    if keys[pygame.K_d]:
        moveCamera(1, 0)

####################################################################

    screen.fill(c_background)

    #if holding a point, move it
    if hand.isHolding == True:
        hand.movePoint()

    #udpate all curves
    for i in range(len(curves)):
        curves[i].draw()
    
    pygame.display.flip()