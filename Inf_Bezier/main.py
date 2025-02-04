import pygame
import sys
import math

pygame.init()
screenWidth = 1000
screenHeight = 500
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

        self.parentCurve = None

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
        self.end1.parentCurve = self

        self.anchor1 = point(self.x, self.y, anchor_width, c_anchor, c_anchor_sdw)
        self.points.append(self.anchor1)
        self.anchor1.parentCurve = self

        self.end2 = point(self.x + 50, self.y - 50, end_width, c_end, c_end_sdw)
        self.points.append(self.end2)
        self.end2.parentCurve = self

        self.deleted = False

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

#zoom
zoomSpeed = 0.001
def zoomIn(zoomSpeed):
    #for every point
    for curve in curves:
        for point in curve.points:
            #get point vector from mouse
            mPos = pygame.mouse.get_pos()
            mX = mPos[0]
            mY = mPos[1]

            vX = point.x - mX
            vY = point.y - mY

            #set new x and y to vector * 1-zoomspeed
            point.x = mX + vX * (1+zoomSpeed)
            point.y = mY + vY * (1+zoomSpeed)

def zoomOut(zoomSpeed):
    #for every point
    for curve in curves:
        for point in curve.points:
            #get point vector from mouse
            mPos = pygame.mouse.get_pos()
            mX = mPos[0]
            mY = mPos[1]

            vX = point.x - mX
            vY = point.y - mY

            #set new x and y to vector * 1+zoomspeed
            point.x = mX + vX * (1-zoomSpeed)
            point.y = mY + vY * (1-zoomSpeed)

#-----------------------------------------------------------------------------------------------------

#initialize curves
end_width = 7
anchor_width = 6
floorHeight = 30
curves = []

curve1 = curve(screenWidth/2, screenHeight/2, 2)

def addCurve(power):
    #add quadratic curve at mouse pos
    mPos = pygame.mouse.get_pos()
    mX = mPos[0]
    mY = mPos[1]

    if power == 2:
        curve2 = curve(mX, mY, 2)

deleteDistance = 50
def deleteCurve():
    #get closest point

    #get mouse pos
    mPos = pygame.mouse.get_pos()
    mX = mPos[0]
    mY = mPos[1]

    #get closest point
    closestMag = 50
    closestPoint = None
    for curve in curves:
        for point in curve.points:
            #get distance to point
            vX = mX - point.x
            vY = mY - point.y
            mag = math.sqrt(vX * vX + vY * vY)
            #comapare distances
            if mag < closestMag and mag < deleteDistance:
                closestMag = mag
                closestPoint = point
    
    #delete the parent curve of obtained point
    if closestPoint != None:
        #set parents curve deletion
        closestPoint.parentCurve.deleted = True

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

        #key events that happen only on the first frame of button down
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            #adding curves
            if keys[pygame.K_2]:
                #add quadratic curve
                addCurve(2)

            #deleting curves
            if keys[pygame.K_x]:
                #delete curve of closest point
                deleteCurve()

        #zooming in or out with scroll wheel
        elif event.type == pygame.MOUSEWHEEL:
            # event.y > 0 --> up
            # event.y < 0 --> down
            if event.y > 0:
                zoomIn(zoomSpeed * 100)
            if event.y < 0:
                zoomOut(zoomSpeed * 100)

    #key events that happen every frame
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moveCamera(0, -1)
    if keys[pygame.K_a]:
        moveCamera(-1, 0)
    if keys[pygame.K_s]:
        moveCamera(0, 1)
    if keys[pygame.K_d]:
        moveCamera(1, 0)

    #zooming in or out with arrow keys
    if keys[pygame.K_UP]:
        zoomIn(zoomSpeed)
    if keys[pygame.K_DOWN]:
        zoomOut(zoomSpeed)

####################################################################

    screen.fill(c_background)

    #if holding a point, move it
    if hand.isHolding == True:
        hand.movePoint()

    #udpate all curves
    for i in range(len(curves)):
        curves[i].draw()
    
    #remove any deleted curves and their points
    newCurves = []
    newPoints = []
    for curv in curves:
        for pont in curv.points:
            if pont.parentCurve.deleted != True:
                newPoints.append(pont)
        if curv.deleted != True:
            newCurves.append(curv)

    #ovveride prev arrays with new ones with missing deleted elements
    curves = newCurves
    points = newPoints

    pygame.display.flip()
