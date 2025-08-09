# #Task_01

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

def draw_house():
    glBegin(GL_TRIANGLES)
    
    glColor3f(104 / 255, 51 / 255, 255 / 255)
    glVertex2f(250, 400) 
    glVertex2f(140, 300) 
    glVertex2f(360, 300)  

    glColor3f(179 / 255, 180 / 255, 186 / 255)
    glVertex2f(160, 300)
    glVertex2f(160, 150)
    glVertex2f(340, 300)

    glVertex2f(340, 300)
    glVertex2f(160, 150)
    glVertex2f(340, 150)

    
    glColor3f(51 / 255, 141 / 255, 255 / 255)
    glVertex2f(235, 150)
    glVertex2f(265, 150)
    glVertex2f(265, 240)

    glVertex2f(265, 240)
    glVertex2f(235, 150)
    glVertex2f(235, 240)

    
    glVertex2f(295, 240)
    glVertex2f(295, 200)
    glVertex2f(315, 200)

    glVertex2f(315, 200)
    glVertex2f(315, 240)
    glVertex2f(295, 240)

    glVertex2f(205, 240)
    glVertex2f(205, 200)
    glVertex2f(185, 200)

    glVertex2f(185, 200)
    glVertex2f(185, 240)
    glVertex2f(205, 240)

    glEnd()

def draw_raindrop():
    global raindrop, angle

    glBegin(GL_LINES)
    flag = True 

    for drop in raindrop:
        x, y = drop

        if flag:
            glColor3f(0, 0, 1)  
            flag = False
        else:
            flag = True
            glColor3f(179 / 255, 174 / 255, 170 / 255)  

        glVertex2f(x, y)
        glVertex2f(x + angle, y - 20)

    glEnd()

def animate():
    global raindrop

    for drop in raindrop:
        drop[0] += angle
        drop[1] -= 5
        if drop[0] < 0:
            drop[0] = width + drop[0]
        elif drop[0] > width:
            drop[0] = drop[0] - width

        if drop[1] < 0: #bottom exceed
            drop[1] = height
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global brightness
#brightness
    if key == b'd':
        brightness = max(0.0, brightness - 0.1)
    elif key == b'l':
        brightness = min(0.8, brightness + 0.1)
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global angle
#rain direction
    if key == GLUT_KEY_LEFT and angle > -30:
        angle -= 1
    elif key == GLUT_KEY_RIGHT and angle < 30:
        angle += 1
    glutPostRedisplay()
    

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClearColor(brightness, brightness, brightness, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_house()
    draw_raindrop()
    glutSwapBuffers()


width, height = 500, 500
brightness = 0.9

raindrop, angle = [], 0.0
#raindrop create
for i in range(100):
    x = random.uniform(0, width)
    y = random.uniform(0,height)
    raindrop.append([x, y])

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) 
glutInitWindowPosition(0, 0)
task1 = glutCreateWindow(b"House with a raindrop") 

glutIdleFunc(animate)
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)


glutMainLoop()





#Task_02


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

arr = []
speed = random.uniform(0.5, 1)
freeze = False
blink = False


def convert_coordinate(x, y):
    global width, height
    a = x - (width / 2)
    b = (height / 2) - y 

    return a, b

def draw_point(x, y):
    glPointSize(7) 
    glBegin(GL_POINTS)
    glVertex2f(x, y) 

    glEnd()

def update_point():
    global arr, freeze, speed
    for i in arr:
        if not freeze:
            if i['x'] >= 250 or i['x'] <= -250:
                i['dx'] *= -1
            i['x'] += i['dx'] * speed

            if i['y'] >= 250 or i['y'] <= -250:
                i['dy'] *= -1
            i['y'] += i['dy'] * speed

def specialKeyListener(key, x, y):
    global speed

    if freeze == False:
        if key == GLUT_KEY_UP:
            speed *= 2
            print("Speed Increased")
        if key == GLUT_KEY_DOWN:	
            speed /= 2
            print("Speed Decreased")
    glutPostRedisplay()

def keyBoardListener(key, x, y) :
    global freeze

    if key == b' ' :
        if freeze == True:
            freeze = False
            print("Unfreeze")
        else:
            freeze  = True
            print("Freeze")

def mouseListener(button, state, x, y):
    global blink, freeze

    if freeze == False:
        if state == GLUT_DOWN:
            if button == GLUT_RIGHT_BUTTON:
                arr.append({'x': random.randint(-200, 200), 'y': random.randint(-200, 200), 'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]), 'color': [random.random(), random.random(), random.random()]})
                print("Point created")

            if button == GLUT_LEFT_BUTTON:
                blink = True
                print("Blink")
        else:
            blink = False
            print("blink off")

def animate():
    global freeze

    if freeze == False:
        glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0); 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)
    glVertex2d(-250, -250)
    glVertex2d(250, -250)
    glVertex2d(250, -250)
    glVertex2d(250, 250)
    glVertex2d(250, 250)
    glVertex2d(-250, 250)
    glVertex2d(-250, 250)
    glVertex2d(-250, -250)
    glEnd()
    
    update_point()

    glPointSize(7)
    glBegin(GL_POINTS)

    for i in arr:
        x = i['x']
        y = i['y']
        if not blink:
            glColor3f(*i['color']) 
        else:
            glColor3f(0.0, 0.0, 0.0)  
            
        glVertex2f(x, y)

    glEnd()
    glutSwapBuffers()




def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1, 1000.0)


width, height = 500, 500

glutInit()
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
task2 = glutCreateWindow(b"Amazing box")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)	

glutKeyboardFunc(keyBoardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		