from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

width, height = 500, 500
play, pause, end = True, False, False
score = 0
speed = 100


def convertCoordinate(x, y):
    global width, height
    a = x
    b = height - y
    return a, b

def drawPoints(x, y, color):
    glColor3f(*color)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx >= 0 and dy <= 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx <= 0 and dy >= 0:
            zone = 2
        elif dx <= 0 and dy <= 0:
            zone = 5
        elif dx >= 0 and dy <= 0:
            zone = 6
            
    return zone

def convertZoneN_to_Zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
    
def convertZone0_to_ZoneN(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    
def MPLA(x1, y1, x2, y2, color, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incNE = 2 * (dy - dx)
    incE = 2 * dy
    x, y = x1, y1
    
    while x <= x2:
        orig_x, orig_y = convertZone0_to_ZoneN(x, y, zone)
        drawPoints(orig_x, orig_y, color)
        
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1
        x += 1
        
def eightWaySymmetry(x1, y1, x2, y2, color):
    zone = find_zone(x1, y1, x2, y2)
    x1_z0, y1_z0 = convertZoneN_to_Zone0(x1, y1, zone)
    x2_z0, y2_z0 = convertZoneN_to_Zone0(x2, y2, zone)
    MPLA(x1_z0, y1_z0, x2_z0, y2_z0, color, zone)
    
def drawCatcher():
    global catcher
    
    if end:
        color = (1, 0, 0)         #catcherbox becomes red when gameover
    else:
        color = (1, 1, 1)    
        
    for i in catcher:
        eightWaySymmetry(*catcher[i][0], *catcher[i][1], color)
        
def drawArrow():
    arrow = {"straight": ((10, 470), (50, 470)), "up": ((10, 470), (30, 490)), "down": ((10, 470), (30, 450))}
    
    for i in arrow:
        eightWaySymmetry(*arrow[i][0], *arrow[i][1], (0, 200/255, 1))
        
def drawCross():
    cross = {"line1": ((450, 450), (490, 490)), "line2": ((450, 490), (490, 450))}
    
    for i in cross:
        eightWaySymmetry(*cross[i][0], *cross[i][1], (1, 0, 0))
        
def drawresume():
    global play
    
    resume = {"line1": ((230, 450), (230, 490)), "line2": ((250, 450), (250, 490))}
    
    if play:
        for i in resume:
            eightWaySymmetry(*resume[i][0], *resume[i][1], (1, 162/255, 0))
            
def drawpause():
    global pause
    
    pausee = {"line1": ((225, 450), (225, 490)), "line2": ((225, 450), (255, 470)), "line3": ((225, 490), (255, 470)) }
    
    if pause:
        for i in pausee:
            eightWaySymmetry(*pausee[i][0], *pausee[i][1], (1, 162/255, 0))
            
def drawDiamond():
    global diamond
    
    for i in diamond:
        if i != "color":
            eightWaySymmetry(*diamond[i][0], *diamond[i][1], diamond["color"])
            
t0 = time.time()

def animate():
    global play, end, catcher, diamond, diamond_pos, bl, speed, score, t0
    
    if not end and play:
        t1 = time.time()
        deltaTime = t1 - t0
        t0 = t1
        catcherBox = {"x": bl[0], "y": bl[1], "width": 140, "height": 30}
        
        for i in diamond:
            if i != "color":
                diamond[i] = ((diamond[i][0][0], diamond[i][0][1] - speed * deltaTime), (diamond[i][1][0], diamond[i][1][1] - speed * deltaTime))
                
        diamondBox = {"x": diamond["bottomLeft"][1][0], "y": diamond["bottomLeft"][1][1], "width": 30, "height": 40}            #current position of diamond
        
        if hasCollided(diamondBox, catcherBox):                             #if collides with catcher, earn points
            diamond_pos = random.randint(25, 475)
            diamond = generateDiamond(diamond_pos)
            score += 1
            speed += 20
            print("Score:", score)
        elif diamond["topRight"][0][1] < 0:               #when diamond hits the window bottom. gameover
            print("Game Over! Final Score:", score)
            end = True
            
    glutPostRedisplay()
    
def generateCatcherbox(bl, br, tr, tl):
    return {"base": (bl, br), "leftDiagonal": (tl, bl), "rightDiagonal": (br, tr), "above": (tl, tr)}

def generateDiamond(diamond_pos):
    return {"topRight": ((diamond_pos, 445), (diamond_pos + 15, 425)), "topLeft": ((diamond_pos, 445), (diamond_pos - 15, 425)), "bottomRight": ((diamond_pos + 15, 425),(diamond_pos, 405)), "bottomLeft": ((diamond_pos - 15, 425), (diamond_pos, 405)), "color": (random.uniform(0.4, 1), random.uniform(0.4, 1), random.uniform(0.4, 1))}        #diamond pos shift

def hasCollided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])
    
# box1's left edge is left of box2's right edge
   # box1's right edge is right of box2's left edge
    # box1's bottom edge is below box2's top edge
      # box1's top edge is above box2's bottom edge
      
def specialKeyListener(i, x, y):              #catcherbox movement horizontally left right
    global play, end, bl, br, tr, tl
    
    if i == GLUT_KEY_RIGHT:
        if tr[0] <= 470 and not end and play:            #right move
            bl[0], br[0], tr[0], tl[0] = bl[0] + 10, br[0] + 10, tr[0] + 10, tl[0] + 10
    elif i == GLUT_KEY_LEFT:
        if tl[0] >= 20 and not end and play:            #left move
            bl[0], br[0], tr[0], tl[0] = bl[0] - 10, br[0] - 10, tr[0] - 10, tl[0] - 10
            
    glutPostRedisplay()
    
def mouseListener(button, state, x, y):           #restart play pause terminate
    global pause, play, end, bl, br, tr, tl, speed, score, diamond, catcher
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x, y = convertCoordinate(x, y)
        if 10 <= x <= 50 and 450 <= y <= 490:              #restart
            print("Starting Over!")
            score, speed = 0, 50
            diamond_pos = random.randint(25, 475)
            diamond = generateDiamond(diamond_pos)
            catcher = generateCatcherbox(bl, br, tr, tl)
            play, pause, end = True, False, False
        elif 230 <= x <= 255 and 450 <= y <= 490 and play:     #pause
                play, pause = False, True
        elif 230 <= x <= 255 and 450 <= y <= 490 and pause:      #resume
                play, pause = True, False
        elif 450 <= x <= 490 and 450 <= y <= 490:                  #terminate
            print(f"Goodbye! Final Score: {score}")
            end = True
            
            glutLeaveMainLoop()
            
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    drawCatcher()
    drawDiamond()
    drawArrow()
    drawCross()
    drawresume()
    drawpause()
    
    glutSwapBuffers()
    
    
bl, br, tr, tl = [180, 10], [280, 10], [300, 35], [160, 35]                 #catcherbox coordinates
catcher = generateCatcherbox(bl, br, tr, tl)
diamond_pos = 90                
diamond = generateDiamond(diamond_pos)


glutInit()

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
MPL = glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()