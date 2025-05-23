### Bezierove Krivulje
Bezierova krivulja je "gladka" krivulja, ki se pogosto uporablja v računalniški (vektorski) grafiki.

[Bézier curve](https://en.wikipedia.org/wiki/B%C3%A9zier_curve)

Glavni princip funkcije bezierove krivulje je to, da preko linearne interpolacije med dvema točkama dobimo novo točko, s katero nadaljujemo verigo interpolacij dokler ne dobimo končne točke.

Tukaj je primer bezierove krivulje, kjer so definirano konstruktorske točke ```p0, p1, p2``` (v moji implementaciji ```p0 = end1, p1 = anc1, p2 = end2```).
Kot parameter ,ki razlikuje dve poljubni točki v določeni krivulji, pa je definiran tudi variabilen ```t``` - realna vrednost med 0 in 1.

![<Gif bezierove krivulje>](Extra/Bézier_2_big.gif)

To je primer bezierove krivulje četrte stopnje:

![<Gif bezierove krivulje>](Extra/Bézier_4_big.gif)

### Kazalo
- [Programski jezik in knjižnice](#Programski-jezik-in-knjižnice)
- [Koda](#Koda)
- [Inicializacija okna](#Inicializacija-okna)
- [Razredi in objekti](#Razredi-in-objekti)
- [Konstruktorska Točka](#Konstruktorska-točka)
- [Krivulja](#Krivulja)
- [Dodatno](#Dodatno)
- [Premikanje točk z miško](#Premikanje-točk-z-miško)
- [Kamera, premikanje in povečava](#Kamera-premikanje-in-povečava)
- [Obstojnost podatkov v datotekah](#Obstojnost-podatkov-v-datotekah)
- [While zanka](#While-zanka)
- [Uporabnikov vnos](#Uporabnikov-vnos)
- [Risanje](#Risanje)
- [Brisanje](#Brisanje)
- [Zaključek](#Zaključek)

### Programski jezik in knjižnice
Za mojo implementacijo sem uporabil programski jezik Python in grafični prikazovalnik Pygame. Za dodatno zmogljivost in funkcije pa sem uporabil ```math``` in ```sys``` ter ```os``` za shranjevanje podatkov.
```py
import pygame
import sys
import os
import math
```
### Koda
#### Inicializacija okna
Najprej inicializiramo Pygame okno s širino ```screenWidth``` in višino ```screenHeight```.
```py
pygame.init()
screenWidth = 1000
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Krivulje')
```
Nato v globalnem obsegu inicializiramo vse barve, za katere uporabimo 0-255 RGB format.
```py
c_end = (255, 0, 0)
c_end_sdw = (150, 0, 0)
c_anchor = (0, 0, 255)
c_anchor_sdw = (0, 0, 150)
c_curveLine = (255, 255 ,255)
c_line = (150, 150, 150)
c_floor_sdw = (0, 0, 0)
```
#### Razredi in objekti
Nadaljujemo z definiranjem glavnih razredeov, kot so konstruktorska točka in kvadratna ter kubična krivulja.

##### Konstruktorska točka
Preprosta konstruktorska točka ima pozicijo v ravnini ```x, y```, širino narisanega kroga ```pointWidth```, barvo narisanega kroga ```color``` in barvo sence narisanega kroga ```sdw_color```.
Za lažje sklicevanje je vsaki točki določena tudi starševska krivulja ```parentCurve```.
```py
class point:
    def __init__(self, x, y, pointWidth, color, sdw_color):

        self.x = x
        self.y = y

        self.pointWidth = pointWidth
        self.color = color
        self.sdw_color = sdw_color

        self.parentCurve = None
```
Točko narišemo tako, da narišemo vsak sloj ločeno, zato definiramo funkciji ```draw``` in ```draw_sdw``` (risanje sence).
```py
    def draw(self):
        #draw point circle
        pygame.draw.circle(screen, self.sdw_color, (self.x, self.y + self.pointWidth/2), self.pointWidth)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.pointWidth)

    def draw_sdw(self):
        #draw floor shadow
        pygame.draw.circle(screen, c_floor_sdw, (self.x, self.y + floorHeight), self.pointWidth)
```

##### Krivulja
Bolj kompleksni strukturi pa sta kvadratna krivulja ```curve2``` in kubična krivulja ```curve3```, ki ju definiramo ločeno, čeprav med njima ni velike razlike.

Vsaki krivulji določimo konstruktorske točke (konec krivulje ```end1```, omejitvene točke ```anchor1, anchor2```, ter drugi konec krivulje ```end2```)
in dva seznama ```bezierPointsX, bezierPointsY```, kjer i-ti element vsakega seznama predstavlja koordinati i-te točke.
Tukaj poudarjam, da je razlikovanje med konstruktorsko točko in točko, s katero narišemo krivuljo, pomembno za razumevanje razlage in programa.

Potrebno je omeniti tudi način risanja krivulj. Vsaka krivulja je sestavljena iz ravnih črt med dvema sosednjima točkama, število teh točk predstavlja natančnost prikaza krivulje ```curveAccuracy```.

Za vizualne lastnosti vsaki krivulji določimo tudi širino črt ```lineWidth```.

```py
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

        self.curveAccuracy = 50
```

(dodatna konstruktorska točka pri kubični krivulji)
```py
        self.anchor2 = point(anchor2X, anchor2Y, anchor_width, c_anchor, c_anchor_sdw)
        self.points.append(self.anchor2)
        self.anchor2.parentCurve = self
```

Ko inicializiramo krivulje pa se inicializirajo tudi vse njene točke.
```py
for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint2(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.end2.x, self.end2.y)
```
Ko premikamo konstruktorske točke krivulje, moramo tudi posodobiti pozicijo vseh njenih točk, tukaj uporabimo funkcijo ```updateCurvePoints```, ki za vsako točko preračuna novo pozicijo.
```py
    def updateCurvePoints(self):
        for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint2(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.end2.x, self.end2.y)
```
Za posodabljanje vseh krivulj, kadar uporabnik nekaj spremeni npr. premakne kamero ali poveča, uporabimo funkcijo ```updateAllCurvePointsOnAction```.
```py
def updateAllCurvePointsOnAction():
    for curve in curves:
        curve.updateCurvePoints()
```
        
Za izračun nove pozicije točke pa uporabimo funkciji ```getBezierPoint2``` in ```getBezierPoint3``` (getBezierPoint2 za kvadratne krivulje in getBezierPoint3 za kubične krivulje).
```py
    def getBezierPoint2(self, t, end1X, end1Y, anc1X, anc1Y, end2X, end2Y):
        x = (1-t)**2 * end1X + 2*(1-t)*t * anc1X + t**2 * end2X
        y = (1-t)**2 * end1Y + 2*(1-t)*t * anc1Y + t**2 * end2Y
        return x, y
```
```py
    def getBezierPoint3(self, t, end1X, end1Y, anc1X, anc1Y, anc2X, anc2Y, end2X, end2Y):
        x = (1-t)**3 * end1X + 3*(1-t)**2*t * anc1X + 3*(1-t)*t**2 * anc2X + t**3 * end2X
        y = (1-t)**3 * end1Y + 3*(1-t)**2*t * anc1Y + 3*(1-t)*t**2 * anc2Y + t**3 * end2Y
        return x, y
```
Tako kot pri točkah, moramo črte in sence vsake krivulje narisati po slojih. 
```py
    def drawCurve(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[i], self.bezierPointsY[i]), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1]), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1]), (self.end2.x, self.end2.y), self.lineWidth)
```
```py
    def drawCurve_sdw(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[i], self.bezierPointsY[i] + floorHeight), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1] + floorHeight), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1] + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)
```
```py
    def drawSupport(self):
        #draw connection lines
        pygame.draw.line(screen, c_line, (self.end1.x, self.end1.y), (self.anchor1.x, self.anchor1.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor1.x, self.anchor1.y), (self.anchor2.x, self.anchor2.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor2.x, self.anchor2.y), (self.end2.x, self.end2.y), self.lineWidth)
```
```py
    def drawSupport_sdw(self):
        #draw connection lines floor shadow
        pygame.draw.line(screen, c_floor_sdw, (self.end1.x, self.end1.y + floorHeight), (self.anchor1.x, self.anchor1.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor1.x, self.anchor1.y + floorHeight), (self.anchor2.x, self.anchor2.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor2.x, self.anchor2.y + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)
```

#### Dodatno

##### Premikanje točk z miško
Za glavni vnos (premikanje konstruktorskih točk krivulj z miško) uporabimo objekt ```mousePointMover```, s katerim 
upravljamo prijem točke ob pritisku ```grabPoint```, kako to točko premaknemo ```movePoint``` in kako izpustimo ```dropPoint```.
```py
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
##### Kamera premikanje in povečava
Za premikanje in povečavo kamere ne uporabimo objekta, saj kadar premikamo kamero v resnici premikamo vse ostalo v nasprotno smer, potrebujemo pa fukncije ```moveCamera, zoomIn, zoomOut```.

```py
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

##### Obstojnost podatkov v datotekah

Shranjevanje podatkov v podatkovno bazo kot npr. v ```.txt``` datoteko je sestavljeno iz 2 glavnih funkcij, shranjevanje v datoteko in nalaganje iz datoteke.

Ampak najprej potrebujemo način sklicevanja datoteke, s katere želimo nalagati/na katero želimo shranjevati. Za to uporabimo ```InputField```(dodatni objekt, o keterem nisem napisal dokumentacije, ker je nekoliko nepotreben), vnosno polje v katerega uporabnik vpiše ime datoteke.

```py
#load from file on open
inputField = TextInputField(5, 105, 300, 40)
fileName = ""
hasFileName = False
```

Ko uporabnik vpiže ime datoteke, program iz nje naloži podatke in iz njih ustvari "nove" krivulje - uporabimo funkcijo ```loadFromFile```.

Tukaj je primer formata, ki ga uporabimo za shranjevanje in nalaganje krivulj. Vsaka vrstica predstavja eno krivuljo. Prva števka (vedno ```2``` ali ```3```) predstavlja stopnjo krivulje (kvadratna ali kubična), 
vsaki 2 naslednji števili pa ponazarjata ```x``` in ```y``` koordinati konstruktivne točke. Prvi par števil za ```end1```, naslednji par za ```anc1``` (v kubični krivulji 2 para za ```anc1``` in ```anc2```) in zadnji par za ```end2```.
```
2 430 423 434 367 449 361
3 440 335 490 257 447 194 506 121
```

```py
def loadFromFile(fileName):

    with open(fileName, 'r') as file:
        content = file.readlines()

        #divide data and use it to initialize new curves
        for line in content:
            #remove newlines
            line = line.replace("\n", "")
            print(line)

            #seperate line by spaces, format
            data = line.split(" ")
            cPower = int(data[0])

            #continue by format depeding on power
            if cPower == 2:
                end1X = int(data[1])
                end1Y = int(data[2])
                anchor1X = int(data[3])
                anchor1Y = int(data[4])
                end2X = int(data[5])
                end2Y = int(data[6])

                curve = curve2(0, 0, end1X, end1Y, anchor1X, anchor1Y, end2X, end2Y, cPower)

            elif cPower == 3:
                end1X = int(data[1])
                end1Y = int(data[2])
                anchor1X = int(data[3])
                anchor1Y = int(data[4])
                anchor2X = int(data[5])
                anchor2Y = int(data[6])
                end2X = int(data[7])
                end2Y = int(data[8])

                curve = curve3(0, 0, end1X, end1Y, anchor1X, anchor1Y, anchor2X, anchor2Y, end2X, end2Y, cPower)
```

Trenutno stanje krivulj pa se shrani na 2 načina, avtomatsko po vsake nekaj sekund, ali ročno (ob pritisku na tipko "e") - uporabimo funkcijo ```saveToFile```.

```py
def saveToFile(fileName):
    with open(fileName, 'w') as file:
        #for each curve
        for curve in curves:
            #write curves info to file line
            if curve.power == 2:
                string = str(round(curve.power)) + " " + str(round(curve.end1.x)) + " " + str(round(curve.end1.y)) + " " + str(round(curve.anchor1.x)) + " " + str(round(curve.anchor1.y)) + " " + str(round(curve.end2.x)) + " " + str(round(curve.end2.y))
                file.write(string + "\n")
            
            if curve.power == 3:
                string = str(round(curve.power)) + " " + str(round(curve.end1.x)) + " " + str(round(curve.end1.y)) + " " + str(round(curve.anchor1.x)) + " " + str(round(curve.anchor1.y)) + " " + str(round(curve.anchor2.x)) + " " + str(round(curve.anchor2.y)) + " " + str(round(curve.end2.x)) + " " + str(round(curve.end2.y))
                file.write(string + "\n")
```

#### While zanka

Glavna zanka ```while``` je zanka, ki omogoča da program teče dokler ga ne ustavimo. V njej se izvede vse kar se tiče uporabnikovega vnosa, posodobitve objektov in risanja na zaslon.

V zanki je zaporedje izvedbe operacij zelo pomembno. Na začetku je vnos, v katerem se izvede tudi posodobitev in šele nato risanje.

##### Uporabnikov vnos
Možnosti vnosa so razdeljene na 2 glavni skupini, vnos, ki se zgodi prvi "frame" po tem ko je tipka pritisnjena in vnos, ki se zgodi vsak "frame" kadar je tipka pritisnjena.

```py
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #handle point movement with mouse
        elif event.type == pygame.MOUSEBUTTONDOWN and hasFileName:
            if event.button == 1:  # Left mouse button
                hand.grabPoint()

        elif event.type == pygame.MOUSEBUTTONUP and hasFileName:
            if event.button == 1:  # Left mouse button
                hand.dropPoint()

        #key events that happen only on the first frame of button down
        elif event.type == pygame.KEYDOWN and hasFileName:
            keys = pygame.key.get_pressed()

            #adding curves
            if keys[pygame.K_2] and hasFileName:
                #add quadratic curve
                addCurve(2)
            if keys[pygame.K_3] and hasFileName:
                #add qubic curve
                addCurve(3)

            #deleting curves
            if keys[pygame.K_x] and hasFileName:
                #delete curve of closest point
                deleteCurve()

            #draw toggles
            if keys[pygame.K_z] and hasFileName:
                if drawPointShadows:
                    drawPointShadows = False
                else:
                    drawPointShadows = True

            if keys[pygame.K_u] and hasFileName:
                if drawCurveShadows:
                    drawCurveShadows = False
                else:
                    drawCurveShadows = True

            if keys[pygame.K_i] and hasFileName:
                if drawSupportLines:
                    drawSupportLines = False
                else:
                    drawSupportLines = True

            if keys[pygame.K_o] and hasFileName:
                if drawCurveLines:
                    drawCurveLines = False
                else:
                    drawCurveLines = True

            if keys[pygame.K_p] and hasFileName:
                if drawPoints:
                    drawPoints = False
                else:
                    drawPoints = True

            if keys[pygame.K_t] and hasFileName:
                if drawInstructions:
                    drawInstructions = False
                else:
                    drawInstructions = True

            #manual save
            if keys[pygame.K_e] and hasFileName:
                saveToFile(fileName)

        #zooming in or out with scroll wheel
        elif event.type == pygame.MOUSEWHEEL and hasFileName:
            if event.y > 0:
                zoomIn(zoomSpeed * 100)
                updateAllCurvePointsOnAction()  #update all curve points due to change
            if event.y < 0:
                zoomOut(zoomSpeed * 100)
                updateAllCurvePointsOnAction()  #update all curve points due to change
```

```py
    #key events that happen every frame
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moveCamera(0, -1 * deltaTime)
        updateAllCurvePointsOnAction()  #update all curve points due to change
    if keys[pygame.K_a]:
        moveCamera(-1 * deltaTime, 0)
        updateAllCurvePointsOnAction()  #update all curve points due to change
    if keys[pygame.K_s]:
        moveCamera(0, 1 * deltaTime)
        updateAllCurvePointsOnAction()  #update all curve points due to change
    if keys[pygame.K_d]:
        moveCamera(1 * deltaTime, 0)
        updateAllCurvePointsOnAction()  #update all curve points due to change

    #constant snap points
    if keys[pygame.K_q]:
        snapPoints()
        updateAllCurvePointsOnAction()  #update all curve points due to change

    #zooming in or out with arrow keys
    if keys[pygame.K_UP]:
        zoomIn(zoomSpeed * deltaTime)
        updateAllCurvePointsOnAction()  #update all curve points due to change
    if keys[pygame.K_DOWN]:
        zoomOut(zoomSpeed * deltaTime)
        updateAllCurvePointsOnAction()  #update all curve points due to change
```
##### Risanje

Nazadnje pa še risanje, kjer se v zaporedju rišejo sloji.
```py
        #draw all shadows
        for curve in curves:
            #draw every curvs shadow
            if drawCurveShadows:
                curve.drawCurve_sdw()

            if drawPointShadows:
                curve.drawSupport_sdw()
                for pont in curve.points:
                    #draw every points shadow
                    pont.draw_sdw()

        #draw all tops
        for curve in curves:
            if drawSupportLines:
                curve.drawSupport()

            if drawCurveLines:
                curve.drawCurve()

            if drawPoints:
                for pont in curve.points:
                    #draw every points shadow
                    pont.draw()
        
        #draw controls and credits
        drawControls()
```
##### Brisanje

Dodatno pa se upravlja tudi odstranjevanje objektov, kjer objekt dodamo v novi seznam za naslednji "frame", če ta objekt ni bil izbirsan trenutni "frame".
```py
        #remove any deleted curves and their points
        newCurves = []
        newPoints = []
        for curve in curves:
            for pont in curve.points:
                if pont.parentCurve.deleted != True:
                    newPoints.append(pont)
            if curve.deleted != True:
                newCurves.append(curve)

        #ovveride prev arrays with new ones with missing deleted elements
        curves = newCurves
        points = newPoints
```

### Zaključek
Trenutna dokumentacija ne obsega vsega, saj preskoči vodilno besedilo za kontrole in manjše detajle.

Napisana je v obliki predstavitve in ne realistične dokumentacije, ki bi jo nekdo morda hotel uporabiti za modifikacijo in gradnjo lastne verzije.

(Zavedam se tudi, da bi se dalo kodo izboljšati in polepšati, kot npr. več datotek kode namesto samo main.py, implementacija bezierove krivulje s parametrom stopnje, torej tudi krivulje nad kubičnimi, boljši sistem shranjevanja podatkov, lepši uporabniški vmesnik itd.)

