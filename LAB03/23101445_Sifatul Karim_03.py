import math
import random

from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


cameraPos = [0, 500, 500]
cameraRot = 0


fpView = False
gunViewState = False
fovY = 120
GRID_LENGTH = 600 
rand_var = 423


num_enemy = 5
enemy_lst = []
enemy_change = [1]*num_enemy
enemyRadius = 55

player_life = 5
game_score = 0
bullets_miss = 0

game_flag = False



for i in range(num_enemy) :
    while True:
        x = random.randint(-470, 470)
        y = random.randint(-470, 470)
        if abs(x) >= 150 or abs(y) >= 150:
            enemy_lst.append([x, y, 0])
            break

def dist(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    dz = pos1[2] - pos2[2]
    
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18) :
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()


    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_grid():
    glBegin(GL_QUADS)

    square_size = 100
    grid_size = 600
    x_start = grid_size
    y_start = - grid_size

    for i in range(12):
        x = x_start
        for c in range(12):
            if (i + c) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 1)

            glVertex3f(x - square_size, y_start + square_size, 0)
            glVertex3f(x, y_start + square_size, 0)
            glVertex3f(x, y_start, 0)
            glVertex3f(x - square_size, y_start, 0)

            x -= square_size
        y_start += square_size
        
    glEnd()
    
    
def floor():
    glBegin(GL_QUADS)

    border = 600
    height = 200
    walls = [(0.18, 1, 0.204), ((0.18, 0.957, 1)), ((0, 0, 1)), ((1, 1, 1))]


    glColor3f(*walls[0])
    glVertex3f(-border,  border, height)
    glVertex3f(-border,  border, 0)
    glVertex3f(-border, -border, 0)
    glVertex3f(-border, -border, height)


    glColor3f(*walls[1])
    glVertex3f(-border, -border, height)
    glVertex3f(-border, -border, 0)
    glVertex3f( border, -border, 0)
    glVertex3f( border, -border, height)


    glColor3f(*walls[2])
    glVertex3f(border,  border, height)
    glVertex3f(border, -border, height)
    glVertex3f(border, -border, 0)
    glVertex3f(border,  border, 0)


    glColor3f(*walls[3])
    glVertex3f(-border, border, height)
    glVertex3f( border, border, height)
    glVertex3f( border, border, 0)
    glVertex3f(-border, border, 0)

    glEnd()
    
def draw_player():
    glPushMatrix()
    glTranslatef(*playerPos)  
    
    if game_flag:
        glRotatef(-90, 1, 0, 0)            #player lie down when game over
    else:
        glRotatef(gunAngle, 0, 0, 1)           
        
    if fpView:
        draw_gun(color = (0.75, 0.75, 0.75), pos_z = 100)
    else:
        draw_body()
        draw_head()
        draw_leg()
        draw_gun(color = (0.75, 0.75, 0.75), pos_z = 100)
        draw_hand()

    glPopMatrix()

def draw_gun(color, pos_z):
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(0, 0, pos_z)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 7, 80, 10, 10)
    glPopMatrix()

def draw_body():
    glColor3f(0.333, 0.42, 0.184)
    glPushMatrix()
    glTranslatef(0, 0, 90)
    glutSolidCube(60)
    glPopMatrix()

def draw_head():
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 150)
    gluSphere(gluNewQuadric(), 25, 10, 10)
    glPopMatrix()

def draw_leg():
    leg_color = (0, 0, 1)

    glColor3f(*leg_color)
    glPushMatrix()
    glTranslatef(-20, -15, 0)
    gluCylinder(gluNewQuadric(), 7, 12, 60, 10, 10)
    glPopMatrix()

    glColor3f(*leg_color)
    glPushMatrix()
    glTranslatef(-20, 15, 0)
    gluCylinder(gluNewQuadric(), 7, 12, 60, 10, 10)
    glPopMatrix()

def draw_hand():
    hand_color = (1, 0.878, 0.741)

    glColor3f(*hand_color)
    glPushMatrix()
    glTranslatef(-20, -15, 100)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 6, 30, 10, 10)
    glPopMatrix()

    glColor3f(*hand_color)
    glPushMatrix()
    glTranslatef(-20, 15, 100)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 6, 30, 10, 10)
    glPopMatrix()
    
def draw_enemies():
        for i in range(len(enemy_lst)):
            enemy_pos = enemy_lst[i]      
            scale = enemy_change[i]     
            
            glPushMatrix() 
            
            glTranslatef(enemy_pos[0], enemy_pos[1], enemy_pos[2])

            glScalef(scale, scale, scale)

            glColor3f(1, 0, 0) 
            body_radius = 60
            gluSphere(gluNewQuadric(), body_radius, 20, 20)

            glColor3f(0, 0, 0) 
            head = 70   
            h_radius = 30
            glTranslatef(0, 0, head)
            gluSphere(gluNewQuadric(), h_radius, 20, 20)

            glPopMatrix()  


def draw_bullet():
    glColor3f(1, 0, 0)
    for bullet in bullet_lst:
        glPushMatrix()
        glTranslatef(*bullet['position'])
        glutSolidCube(10)
        glPopMatrix()
        
playerPos = [0, 0, 0]
gunAngle = 90
movAngle = 90
playerSpeed = 12
playerRadius = 35

bullet_lst = []
bullet_size = 20
bullet_speed = 12
b_limit = 10

def fire():
    global bullet_lst, gunAngle, playerPos, cheatMode, enemy_lst

    gun_length = 70
    gun_offset_x = -math.cos(math.radians(gunAngle)) * gun_length
    gun_offset_y = -math.sin(math.radians(gunAngle)) * gun_length


    bullet_pos = [
        playerPos[0] + gun_offset_x,
        playerPos[1] + gun_offset_y,
        playerPos[2] + 100
    ]

    bullet_vel = [
        -math.cos(math.radians(gunAngle)) * bullet_speed,
        -math.sin(math.radians(gunAngle)) * bullet_speed,
        0
    ]

    target_index = -1
    if cheatMode:
        target_index = next(
            (i for i, enemy_pos in enumerate(enemy_lst) if isEnemyInRange(enemy_pos)), -1)

    bullet_lst.append({
        'position': bullet_pos,
        'direction': bullet_vel,
        'active': True,
        'target': cheatMode and target_index != -1,
        'idx': target_index
    })

def isEnemyInRange(enemy_pos):

    dx = enemy_pos[0] - playerPos[0]
    dy = enemy_pos[1] - playerPos[1]
    distance = dx*dx + dy*dy

    if distance < 1:
        return False

    enemy_angle = math.degrees(math.atan2(-dy, -dx)) % 360

    gun_angle_norm = gunAngle % 360

    angle_diff = abs(gun_angle_norm - enemy_angle)
    angle_diff = min(angle_diff, 360 - angle_diff)

    return angle_diff <= 16


def keyboardListener(key, x, y):
    global gunAngle, playerPos, playerSpeed, game_flag, cheatMode, movAngle, gunViewState, fpView

    if key == b'c':
        cheatMode = not cheatMode
        movAngle = gunAngle 

    if key == b'v' and not cheatMode:
        fpView = not fpView
        if fpView:
            gunViewState = True

    playerRotate(key)
    playerMove(key)

    if game_flag:
        if key == b'r':
            gameReset()
        return

    glutPostRedisplay()

def playerRotate(key):
    global gunAngle, movAngle, cheatMode

    if not cheatMode:
        if key == b'a':
            gunAngle += 5
            if gunAngle >= 360:
                gunAngle -= 360
            movAngle = gunAngle

        if key == b'd':
            gunAngle -= 5
            if gunAngle < 0:
                gunAngle += 360
            movAngle = gunAngle

def playerMove(key):
    global playerPos, playerSpeed, movAngle, gunAngle, cheatMode

    if cheatMode:
        moveDirection = movAngle
    else:
        moveDirection = gunAngle

    if key == b'w':
        dx = playerSpeed * math.cos(math.radians(moveDirection))
        dy = playerSpeed * math.sin(math.radians(moveDirection))

        currX = playerPos[0] - dx
        currY = playerPos[1] - dy
        if -500 <= currX <= 500 and -500 <= currY <= 500:
            playerPos[0] = currX
            playerPos[1] = currY

    if key == b's':
        dx = -(playerSpeed * math.cos(math.radians(moveDirection)))
        dy = -(playerSpeed * math.sin(math.radians(moveDirection)))

        currX = playerPos[0] - dx
        currY = playerPos[1] - dy
        if -500 <= currX <= 500 and -500 <= currY <= 500:
            playerPos[0] = currX
            playerPos[1] = currY


def specialKeyListener(key, x, y):
    global cameraPos, cameraRot, fpView
    
    if fpView:
        glutPostRedisplay()
        return

    camX, camY, camZ = cameraPos

    if key == GLUT_KEY_UP:
        camZ = min(camZ + 20, 800)

    elif key == GLUT_KEY_DOWN:
        camZ = max(camZ - 20, 200)

    elif key == GLUT_KEY_LEFT:
        cameraRot = (cameraRot + 5) % 360

    elif key == GLUT_KEY_RIGHT:
        cameraRot = (cameraRot - 5) % 360

    cameraPos = (camX, camY, camZ)
    glutPostRedisplay()
    
def mouseListener(button, state, x, y) :
    global game_flag, fpView

    if game_flag:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire()
        glutPostRedisplay()

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fpView = not fpView
        glutPostRedisplay()


def setupCamera() :
    global fpView, playerPos, gunAngle, cameraPos, cameraRot, gunViewState

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if fpView:
        gluPerspective(100, 1.25, 0.1, 1500)
    else:
        gluPerspective(fovY, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if fpView:
        eX, eY, eZ = playerPos[0], playerPos[1], playerPos[2] + 150

        if cheatMode and not gunViewState:
            x = eX - math.cos(math.radians(90)) * 100
            y = eY - math.sin(math.radians(90)) * 100
        else:
            x = eX - math.cos(math.radians(gunAngle)) * 100
            y = eY - math.sin(math.radians(gunAngle)) * 100

        z = eZ

        gluLookAt(eX, eY, eZ,
                  x, y, z,
                  0, 0, 1)
    else:
        x, y, z = cameraPos
        radius = 450
        x = radius * math.cos(math.radians(cameraRot))
        y = radius * math.sin(math.radians(cameraRot))

        gluLookAt(x, y, z,
                  0, 0, 0,
                  0, 0, 1)

def idle() :
    global enemy_lst, bullet_lst, game_score, bullets_miss, player_life, enemy_change, game_flag
    global scaleIncrease, scaleStatus, sTimer, scaleMin, scaleMax
    global gunAngle, cheatMode, autoFire

    if game_flag :
        glutPostRedisplay()

        return

    if cheatMode:
        gunAngle += auto_rotation_speed % 360

        autoFire += 1
        if autoFire >= autoFireTimeSpan:
            for i in range(len(enemy_lst)):
                if isEnemyInRange(enemy_lst[i]):
                    dx = enemy_lst[i][0] - playerPos[0]
                    dy = enemy_lst[i][1] - playerPos[1]
                    gunAngle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
                    fire()
                    autoFire = 0
                break

    updateEnemyScaling()
    moveEnemiesAndCheckCollisions()
    manageBullets()


cheatMode = False
auto_rotation_speed = 2
autoFire = 0
autoFireTimeSpan = 15

scaleMin = 0.5
scaleMax = 1
steps = 20
scaleIncrease =  0.025
scaleStatus = 1
sTimer = 0
scaleSpan = 100

def moveEnemiesAndCheckCollisions():
    global enemy_lst, bullet_lst, game_score, player_life, game_flag, enemy_change

    enemy_speed = 0.1
    player_radius = 35

    for i in range(len(enemy_lst)):
        dx = playerPos[0] - enemy_lst[i][0]
        dy = playerPos[1] - enemy_lst[i][1]


        if dx != 0 or dy != 0:
            inv_length = 1.0 / math.sqrt(dx*dx + dy*dy)
            dx *= inv_length
            dy *= inv_length


        enemy_lst[i][0] += dx * enemy_speed 
        enemy_lst[i][1] += dy * enemy_speed

        enemy_radius = 60 * enemy_change[i]
        dist_x = playerPos[0] - enemy_lst[i][0]
        dist_y = playerPos[1] - enemy_lst[i][1]
        dist_z = playerPos[2] - enemy_lst[i][2]
        dist_sq = dist_x*dist_x + dist_y*dist_y + dist_z*dist_z

        if dist_sq < (enemy_radius + player_radius)**2:
            player_life -= 1
            while True:
                x = random.randint(-470, 470)
                y = random.randint(-470, 470)
                if abs(x) >= 150 or abs(y) >= 150:
                    enemy_lst[i] = [x, y, 0]
                    break

            if player_life <= 0:
                game_flag = True
                return


def manageBullets():
    global bullet_lst, enemy_lst, game_score, bullets_miss, player_life, game_flag, cheatMode

    bullet_speed = 1.5
    limit = 600
    en_height = 30
    hit_range = 100

    bullets_to_remove = []

    for i in range(len(bullet_lst)):
        bullet = bullet_lst[i]
        if not bullet['active']:
            bullets_to_remove.append(i)
            continue


        if cheatMode and bullet.get('target', False):
            target_index = bullet.get('idx', -1)
            if 0 <= target_index < len(enemy_lst):
                idx = enemy_lst[target_index]
                dx = idx[0] - bullet['position'][0]
                dy = idx[1] - bullet['position'][1]
                dz = en_height - bullet['position'][2]


                length = math.sqrt(dx*dx + dy*dy + dz*dz)
                if length > 0:
                    bullet['direction'] = [
                        dx/length * bullet_speed * bullet_speed,
                        dy/length * bullet_speed * bullet_speed,
                        dz/length * bullet_speed
                    ]


        bullet['position'][0] += bullet['direction'][0]
        bullet['position'][1] += bullet['direction'][1]
        bullet['position'][2] += bullet['direction'][2]


        if (abs(bullet['position'][0]) > limit or
                abs(bullet['position'][1]) > limit):
            if not cheatMode:
                bullets_miss += 1
                if bullets_miss >= b_limit:
                    game_flag = True
            bullet['active'] = False
            bullets_to_remove.append(i)
            continue


        for c in range(len(enemy_lst)):
            enemy = enemy_lst[c]
            dx = bullet['position'][0] - enemy[0]
            dy = bullet['position'][1] - enemy[1]
            dist = math.sqrt(dx*dx + dy*dy)
            height_diff = abs(bullet['position'][2] - en_height)

            if dist < 60 * enemy_change[c] and height_diff < hit_range:
                game_score += 1
                bullet['active'] = False
                bullets_to_remove.append(i)

                while True:
                    x = random.randint(-470, 470)
                    y = random.randint(-470, 470)
                    if abs(x) >= 150 or abs(y) >= 150:
                        enemy_lst[c] = [x, y, 0]
                        break
                break


    for i in sorted(bullets_to_remove, reverse=True):
        if i < len(bullet_lst):
            bullet_lst.pop(i)

    glutPostRedisplay()
    

def updateEnemyScaling():
    global enemy_change, scaleStatus, sTimer, scaleMin, scaleMax, scaleIncrease

    sTimer += 1
    if sTimer >= scaleSpan // steps:
        sTimer = 0

        for i in range(len(enemy_change)):

            newScale = enemy_change[i] + (scaleIncrease * scaleStatus)

            if newScale > scaleMax:
                newScale = scaleMax
                scaleStatus = -1
            elif newScale < scaleMin:
                newScale = scaleMin
                scaleStatus = 1

            enemy_change[i] = newScale

def gameReset():
    global playerPos, gunAngle, movAngle, game_score, bullets_miss, player_life
    global bullet_lst, game_flag, enemy_lst, enemy_change
    global scaleStatus, sTimer, fpView, cameraPos, cameraRot, cheatMode


    playerPos = [0, 0, 0]
    gunAngle = 90
    movAngle = 90
    cameraPos = (0, 500, 500)
    cameraRot = 0


    game_score = 0
    bullets_miss = 0
    player_life = 5
    game_flag = False
    cheatMode = False
    fpView = False
    scaleStatus = 1

    bullet_lst.clear()
    enemy_lst.clear()
    enemy_change.clear()

    for i in range(num_enemy):
        while True:
            x = random.randint(-470, 470)
            y = random.randint(-470, 470)
            if abs(x) >= 150 or abs(y) >= 150:
                enemy_lst.append([x, y, 0])
                enemy_change.append(1.0)
                break


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()
    draw_grid()
    floor()
    draw_player()
    draw_bullet()
    draw_enemies()

    if not game_flag:
        draw_text(10, 570, f"Player Life Remaining: {player_life}")
        draw_text(10, 540, f"Game game_score : {game_score}")
        draw_text(10, 510, f"Player Bullets Missed: {bullets_miss}")
    else:
        draw_text(10, 570, f"Game Over. Final score: {game_score}")
        draw_text(10, 540, "Press 'R' to RESTART the Game")

    glutSwapBuffers()
    

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 600) 
    glutInitWindowPosition(0, 0) 
    game = glutCreateWindow(b"3D Game")  

    glutDisplayFunc(showScreen)  
    glutKeyboardFunc(keyboardListener) 
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  

    glutMainLoop()  

if __name__ == "__main__":
    main()


