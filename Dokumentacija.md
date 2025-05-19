### Bezierove Krivulje
Bezierova krivulja je "gladka" krivulja, ki se pogosto uporablja v računalniški (vektorski) grafiki.
[Bezier curve](https://en.wikipedia.org/wiki/B%C3%A9zier_curve)
Glavni princip bezierove krivulje je to, da preko linearne interpolacije med dvema točkama dobimo novo točko, s katero nadaljujemo verigo interpolacij dokler ne dobimo končne točke.
#### Programski jezik in knjižnice
Za mojo implementacijo sem uporabil programski jezik Python in grafični prikazovalnik Pygame. Za dodatno zmogljivost in funkcije pa sem uporabil ```math``` in ```sys``` ter ```os``` za shranjevanje podatkov.
```
import pygame
import sys
import os
import math
```
### Koda
Najprej inicializiramo Pygame okno z širino ```screenWidth``` in višino ```screenHeight```.
```
pygame.init()
screenWidth = 1000
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Krivulje')
```
Nato se v globalnem obsegu inicializirajo vse barve, za katere sem uporabil RGB format.
```
c_end = (255, 0, 0)
c_end_sdw = (150, 0, 0)
c_anchor = (0, 0, 255)
c_anchor_sdw = (0, 0, 150)
c_curveLine = (255, 255 ,255)
c_line = (150, 150, 150)
c_floor_sdw = (0, 0, 0)
```
#### - Objekti
Nadaljujemo z definiranjem glafnih razredeov, kot so točka in kvadratna ter kubična krivulja.

Preprosta točka ima pozicijo v ravnini, širino narisanega kroga, barvo narisanega kroga in barvo sence narisanega kroga.
Za lažje sklicevanje je vsaki točki določena tudi starševska krivulja.
```
class point:
    def __init__(self, x, y, pointWidth, color, sdw_color):

        self.x = x
        self.y = y

        self.pointWidth = pointWidth
        self.color = color
        self.sdw_color = sdw_color

        self.parentCurve = None
```
Točko narišemo tako, da narižemo vsak sloj ločeno, zato definiramo fuknciji draw in drawSdw (risanje sence).
```
    def draw(self):
        #draw point circle
        pygame.draw.circle(screen, self.sdw_color, (self.x, self.y + self.pointWidth/2), self.pointWidth)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.pointWidth)

    def draw_sdw(self):
        #draw floor shadow
        pygame.draw.circle(screen, c_floor_sdw, (self.x, self.y + floorHeight), self.pointWidth)
```
Bolj kompleksni strukturi pa sta kvadratna krivulja (curve2) in kubična krivulje (curve3), ki ju definiramo ločeno, čeprav med njima ni velike razlike.
Vsaki krivulji določamo širino črte, seznam točk, ki sestavljajo krivuljo, konstruktorske točke (konec krivulje, omejitvene točke, ter drugi konec krivulje)
Tukaj je potrebno omeniti način risanja krivulj. Vsaka krivulja je sestavljena iz ravnih črt med dvema sosednjima točkama, število teh točk predstavlja natančnost prikaza krivulje.
```
class curve2:
    def __init__(self, x, y, end1X, end1Y, anchor1X, anchor1Y, end2X, end2Y, lineWidth):
        curves.append(self)

        self.x = x
        self.y = y
        self.power = 2

        self.lineWidth = lineWidth

        self.points = []
        self.end1 = point(end1X, end1Y, end_width, c_end, c_end_sdw)
        self.points.append(self.end1)
        self.end1.parentCurve = self

        self.anchor1 = point(anchor1X, anchor1Y, anchor_width, c_anchor, c_anchor_sdw)
        self.points.append(self.anchor1)
        self.anchor1.parentCurve = self

        self.end2 = point(end2X, end2Y, end_width, c_end, c_end_sdw)
        self.points.append(self.end2)
        self.end2.parentCurve = self
```
Mogoče ste opazili tudi funkcijo append, katero uporabimo za pripenjanje objekta v seznam, iz katerega sklicujemo funkcije vsakega elementa v zanki.
Ko inicializiramo krivulje pa se inicializirajo tudi vse njene točke.
```
for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint2(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.end2.x, self.end2.y)
```
Ko premikamo konstruktivne točke krivulje, moramo tudi posodobiti pozicijo vseh njenih točk, tukaj uporabimo funkcijo ```updateCurvePoints```, ki za vsako točko preračuna novo pozicijo.
```
    def updateCurvePoints(self):
        for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint2(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.end2.x, self.end2.y)
```
Za izračun nove pozicije točke pa uporabimo funkciji ```getBezierPoint2``` in ```getBezierPoint3``` (getBezierPoint2 za kvadratne krivulje in getBezierPoint3 za kubične).
```
    def getBezierPoint2(self, t, end1X, end1Y, anc1X, anc1Y, end2X, end2Y):
        x = (1-t)**2 * end1X + 2*(1-t)*t * anc1X + t**2 * end2X
        y = (1-t)**2 * end1Y + 2*(1-t)*t * anc1Y + t**2 * end2Y
        return x, y
```
```
    def getBezierPoint3(self, t, end1X, end1Y, anc1X, anc1Y, anc2X, anc2Y, end2X, end2Y):
        x = (1-t)**3 * end1X + 3*(1-t)**2*t * anc1X + 3*(1-t)*t**2 * anc2X + t**3 * end2X
        y = (1-t)**3 * end1Y + 3*(1-t)**2*t * anc1Y + 3*(1-t)*t**2 * anc2Y + t**3 * end2Y
        return x, y
```
Tako kot pri točkah, moramo črte in sence vsake krivulje narisati po slojih. 
```
    def drawCurve(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[i], self.bezierPointsY[i]), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1]), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1]), (self.end2.x, self.end2.y), self.lineWidth)
```
```
    def drawCurve_sdw(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[i], self.bezierPointsY[i] + floorHeight), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1] + floorHeight), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1] + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)
```
```
    def drawSupport(self):
        #draw connection lines
        pygame.draw.line(screen, c_line, (self.end1.x, self.end1.y), (self.anchor1.x, self.anchor1.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor1.x, self.anchor1.y), (self.anchor2.x, self.anchor2.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor2.x, self.anchor2.y), (self.end2.x, self.end2.y), self.lineWidth)
```
```
    def drawSupport_sdw(self):
        #draw connection lines floor shadow
        pygame.draw.line(screen, c_floor_sdw, (self.end1.x, self.end1.y + floorHeight), (self.anchor1.x, self.anchor1.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor1.x, self.anchor1.y + floorHeight), (self.anchor2.x, self.anchor2.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor2.x, self.anchor2.y + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)
```

#### - dodatno - premikanje točk, kamera
Za glavni vnos (premikanje konstruktivnih točk krivulj z miško) uporabimo objekt ```mousePointMover```, s katerim 
upravljamo katera točka je prijeta ob pritisku, kako to točko premaknemo in kako spustimo.
```
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
```
Za premikanje in povečavo kamere ne uporabimo objekta, ker kadar premikamo kamero, v resnici premikamo vse drugo v nasprotno smer, za kar ne potrebujemo objekta, potrebujemo pa fukncije.

```
#move camera
cameraSpeed = 0.1

def moveCamera(xdif, ydif):
    #get every point and move it opposite
    for curve in curves:
        for point in curve.points:
            point.x -= xdif * cameraSpeed
            point.y -= ydif * cameraSpeed

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
```

#### - While loop

Glavna zanka while je zanka, ki omogoča da program teče dokler ga ne ustavimo. V njej se izvede vse kar se tiče uporabnikovega vnosa, posodobitve objektov in risanja na zaslon.

V zanki je zaporedje izvedbe operacij zelo pomembno. Na začetku je vnos, v katerem se izvede tudi posodobitev in šele nato risanje.

Možnosti vnosa so razdeljene na 2 glavni skupini, vnos, ki se zgodi prvi "frame" po tem ko je tipka pritisnjena in vnos, ki se zgodi vsak "frame" kadar je tipka pritisnjena.

//input

//move held points

//draw layers

//remove deleted curves


