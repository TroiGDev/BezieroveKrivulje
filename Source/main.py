import pygame
import sys
import os
import math

pygame.init()
screenWidth = 1000
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Krivulje')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

#colors
c_background = (18, 18, 18)

c_end = (255, 0, 0)
c_end_sdw = (150, 0, 0)

c_anchor = (0, 0, 255)
c_anchor_sdw = (0, 0, 150)

c_curveLine = (255, 255 ,255)

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

        self.deleted = False

        self.curveAccuracy = 50

        #initialize bezier points as 2 arrays of each coordinate instead of new point object
        self.bezierPointsX = [0] * self.curveAccuracy
        self.bezierPointsY = [0] * self.curveAccuracy

        for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint2(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.end2.x, self.end2.y)

    def drawSupport(self):
        #draw connection lines
        pygame.draw.line(screen, c_line, (self.end1.x, self.end1.y), (self.anchor1.x, self.anchor1.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor1.x, self.anchor1.y), (self.end2.x, self.end2.y), self.lineWidth)
    
    def drawSupport_sdw(self):
        #draw connection lines floor shadow
        pygame.draw.line(screen, c_floor_sdw, (self.end1.x, self.end1.y + floorHeight), (self.anchor1.x, self.anchor1.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor1.x, self.anchor1.y + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)

    def getBezierPoint2(self, t, end1X, end1Y, anc1X, anc1Y, end2X, end2Y):
        x = (1-t)**2 * end1X + 2*(1-t)*t * anc1X + t**2 * end2X
        y = (1-t)**2 * end1Y + 2*(1-t)*t * anc1Y + t**2 * end2Y
        return x, y

    def updateCurvePoints(self):
        for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint2(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.end2.x, self.end2.y)

    def drawCurve(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[i], self.bezierPointsY[i]), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1]), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1]), (self.end2.x, self.end2.y), self.lineWidth)

    def drawCurve_sdw(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[i], self.bezierPointsY[i] + floorHeight), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1] + floorHeight), self.lineWidth)

        #draw line from last point to end2
        pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1] + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)

class curve3:
    def __init__(self, x, y, end1X, end1Y, anchor1X, anchor1Y, anchor2X, anchor2Y, end2X, end2Y, lineWidth):
        curves.append(self)

        self.x = x
        self.y = y
        self.power = 3

        self.lineWidth = lineWidth

        self.points = []
        self.end1 = point(end1X, end1Y, end_width, c_end, c_end_sdw)
        self.points.append(self.end1)
        self.end1.parentCurve = self

        self.anchor1 = point(anchor1X, anchor1Y, anchor_width, c_anchor, c_anchor_sdw)
        self.points.append(self.anchor1)
        self.anchor1.parentCurve = self

        self.anchor2 = point(anchor2X, anchor2Y, anchor_width, c_anchor, c_anchor_sdw)
        self.points.append(self.anchor2)
        self.anchor2.parentCurve = self

        self.end2 = point(end2X, end2Y, end_width, c_end, c_end_sdw)
        self.points.append(self.end2)
        self.end2.parentCurve = self

        self.deleted = False

        self.curveAccuracy = 50

        #initialize bezier points as 2 arrays of each coordinate instead of new point object
        self.bezierPointsX = [0] * self.curveAccuracy
        self.bezierPointsY = [0] * self.curveAccuracy

        for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint3(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.anchor2.x, self.anchor2.y, self.end2.x, self.end2.y)

    def drawSupport(self):
        #draw connection lines
        pygame.draw.line(screen, c_line, (self.end1.x, self.end1.y), (self.anchor1.x, self.anchor1.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor1.x, self.anchor1.y), (self.anchor2.x, self.anchor2.y), self.lineWidth)
        pygame.draw.line(screen, c_line, (self.anchor2.x, self.anchor2.y), (self.end2.x, self.end2.y), self.lineWidth)
    
    def drawSupport_sdw(self):
        #draw connection lines floor shadow
        pygame.draw.line(screen, c_floor_sdw, (self.end1.x, self.end1.y + floorHeight), (self.anchor1.x, self.anchor1.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor1.x, self.anchor1.y + floorHeight), (self.anchor2.x, self.anchor2.y + floorHeight), self.lineWidth)
        pygame.draw.line(screen, c_floor_sdw, (self.anchor2.x, self.anchor2.y + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)

    def getBezierPoint3(self, t, end1X, end1Y, anc1X, anc1Y, anc2X, anc2Y, end2X, end2Y):
        x = (1-t)**3 * end1X + 3*(1-t)**2*t * anc1X + 3*(1-t)*t**2 * anc2X + t**3 * end2X
        y = (1-t)**3 * end1Y + 3*(1-t)**2*t * anc1Y + 3*(1-t)*t**2 * anc2Y + t**3 * end2Y

        return x, y

    def updateCurvePoints(self):
        for i in range(self.curveAccuracy):
            self.bezierPointsX[i], self.bezierPointsY[i] = self.getBezierPoint3(i/self.curveAccuracy, self.end1.x, self.end1.y, self.anchor1.x, self.anchor1.y, self.anchor2.x, self.anchor2.y, self.end2.x, self.end2.y)

    def drawCurve(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[i], self.bezierPointsY[i]), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1]), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_curveLine, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1]), (self.end2.x, self.end2.y), self.lineWidth)

    def drawCurve_sdw(self):
        #draw lines between the curve points
        for i in range(self.curveAccuracy - 1):
            #draw line between i and i+1
            pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[i], self.bezierPointsY[i] + floorHeight), (self.bezierPointsX[i + 1], self.bezierPointsY[i + 1] + floorHeight), self.lineWidth)
        
        #draw line from last point to end2
        pygame.draw.line(screen, c_floor_sdw, (self.bezierPointsX[self.curveAccuracy-1], self.bezierPointsY[self.curveAccuracy-1] + floorHeight), (self.end2.x, self.end2.y + floorHeight), self.lineWidth)


def updateAllCurvePointsOnAction():
    for curve in curves:
        curve.updateCurvePoints()
    
    #save changes automaticaly
    if hasFileName:
        saveToFile(fileName)

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

def addCurve(power):
    #add quadratic curve at mouse pos
    mPos = pygame.mouse.get_pos()
    mX = mPos[0]
    mY = mPos[1]

    if power == 2:
        curve = curve2(mX, mY, mX - 50, mY + 50, mX, mY, mX + 50, mY - 50, 2)

    if power == 3:
        curve = curve3(mX, mY, mX - 50, mY + 50, mX - 17, mY + 17, mX + 17, mY - 17, mX + 50, mY - 50, 2)

deleteDistance = 50
def deleteCurve():
    #get closest point

    #get mouse pos
    mPos = pygame.mouse.get_pos()
    mX = mPos[0]
    mY = mPos[1]

    #get closest point
    closestMag = 100
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

snapDistance = 25
def snapPoints():
    #get all points in range of mouse position
    mPos = pygame.mouse.get_pos()
    mX = mPos[0]
    mY = mPos[1]

    snappedPoints = []
    for curve in curves:
        for point in curve.points:
            #get distance to mouse pos
            vX = mX - point.x
            vY = mY - point.y

            mag = math.sqrt(vX * vX + vY * vY)

            if mag < snapDistance:
                snappedPoints.append(point)
    
    #set all snapped points pos to mouse
    for point in snappedPoints:
        point.x = mX
        point.y = mY

#---------------------------------------------------------------------------------------------------------
#save file

#ask for file name
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

#-----------------------------------------------------------------------------------------------------
#draw toggles
drawPointShadows = True             #toggle z
drawCurveShadows = True             #toggle u
drawSupportLines = True             #toggle i
drawCurveLines = True               #toggle o
drawPoints = True                   #toggle p
drawInstructions = True             #toggle t

#-----------------------------------------------------------------------------------------------------
#draw controls
font = pygame.font.SysFont('impact', 15)
allstrings = []

# Define text
cont1 = "wasd - move"
cont2 = "up/down/scroll - zoom"
cont3 = "click - grab points"
cont4 = "2 - create new curve2"
cont5 = "3 - create new curve3"
cont6 = "x - delete curve"
cont7 = "q - snap points"
cont8 = "z/u/i/o/p - toggle layers"
cont9 = "t - toggle instructions"

allstrings.append(cont1)
allstrings.append(cont2)
allstrings.append(cont3)
allstrings.append(cont4)
allstrings.append(cont5)
allstrings.append(cont6)
allstrings.append(cont7)
allstrings.append(cont8)
allstrings.append(cont9)

def drawControls():
    if drawInstructions:
        cred = font.render("Gašper Korošec 2.b", True, c_curveLine)
        screen.blit(cred, (5, 5))

        for i in range(len(allstrings)):
            cont = font.render(allstrings[i], True, c_curveLine)
            screen.blit(cont, (5, 50 + 15*i))

#-----------------------------------------------------------------------------------------------------
#file name input field
class TextInputField:
    def __init__(self, x, y, width, height, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False 
        
        # Colors
        self.inactive_color = pygame.Color('gray20')
        self.active_color = pygame.Color('white')
        self.text_color = pygame.Color('white')
        
        # Font setup
        self.font = pygame.font.Font(None, font_size)
        
        # Event handling
        self.return_pressed = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
                
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.return_pressed = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    
    def draw(self, screen):
        # Draw the text input box
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, color, self.rect, 2)
        
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        
        # Show cursor if active
        if self.active:
            cursor_x = self.rect.x + text_surface.get_width() + 10
            pygame.draw.line(screen, self.text_color, 
                           (cursor_x, self.rect.y + 5),
                           (cursor_x, self.rect.y + self.rect.height - 5), 2)
#-----------------------------------------------------------------------------------------------------

clock = pygame.time.Clock()

#load from file on open
inputField = TextInputField(5, 105, 300, 40)
fileName = ""
hasFileName = False

while True:

    #get delta time
    deltaTime = clock.tick(60) # 60 FPS

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

            #snap points
            if keys[pygame.K_q] and hasFileName:
                #delete curve of closest point
                snapPoints()
                updateAllCurvePointsOnAction()  #update all curve points due to change

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

        #zooming in or out with scroll wheel
        elif event.type == pygame.MOUSEWHEEL and hasFileName:
            if event.y > 0:
                zoomIn(zoomSpeed * 100)
                updateAllCurvePointsOnAction()  #update all curve points due to change
            if event.y < 0:
                zoomOut(zoomSpeed * 100)
                updateAllCurvePointsOnAction()  #update all curve points due to change

        #handle input field events
        inputField.handle_event(event)
    
        # Get text when Enter is pressed
        if inputField.return_pressed:
            #if file doesnt exist, create it
            if not os.path.exists(inputField.text):
                with open(inputField.text, 'w') as f:
                    pass
            #else if it exists, load it
            else:
                loadFromFile(inputField.text)

            fileName = inputField.text
            inputField.text = ''  # Clear the input
            inputField.return_pressed = False
            hasFileName = True

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

    #zooming in or out with arrow keys
    if keys[pygame.K_UP]:
        zoomIn(zoomSpeed * deltaTime)
        updateAllCurvePointsOnAction()  #update all curve points due to change
    if keys[pygame.K_DOWN]:
        zoomOut(zoomSpeed * deltaTime)
        updateAllCurvePointsOnAction()  #update all curve points due to change

    ####################################################################

    screen.fill(c_background)

    #if doesnt have file name
    if hasFileName == False:
        inputField.draw(screen)
        instr = font.render("This is a simple scalable vector graphics application\n for drawing using quadratic and qubic bezier curves! \n \n To create a new file enter the desired name followed by .txt \n To open an already existing file enter its name followed by .txt", True, c_curveLine)
        screen.blit(instr, (5, 5))

    #if has file name
    if hasFileName:
        #if holding a point, move it
        if hand.isHolding == True:
            hand.movePoint()
            updateAllCurvePointsOnAction()  #update all curve points due to change
        
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

    pygame.display.flip()
