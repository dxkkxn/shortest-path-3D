#!/usr/bin/env python3

from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
# from Image import open
from PIL import Image
from math import cos, sin
from copy import deepcopy
from spa import dijkstra_sd


def display_grid():
    glBegin(GL_LINES);

    n = 90
    for i in range(-n, n):
        # x, y
        glColor3f (1.0, 1.0, 1.0);
        glVertex3f(i, -n, 0.0);
        glVertex3f(i, n, 0.0);

        glColor3f (1.0, 1.0, 1.0);
        glVertex3f(-n, i, 0.0);
        glVertex3f(n, i, 0.0);

        #x, z
        glColor3f (1.0, 1.0, 1.0);
        glVertex3f(i, 0.0, -n);
        glVertex3f(i, 0.0, n);

        glColor3f (1.0, 1.0, 1.0);
        glVertex3f(-n, 0.0, i);
        glVertex3f(n, 0.0, i);

        #y, z
        glColor3f (1.0, 1.0, 1.0);
        glVertex3f(0.0, i, -n);
        glVertex3f(0.0, i, n);

        glColor3f (1.0, 1.0, 1.0);
        glVertex3f(0.0, -n, i);
        glVertex3f(0.0, n, i);

    glEnd()
    return


###############################################################
#
x_pos, y_pos, z_pos = 0, 10, 10
DISPLAY_GRID = False
GRID = None
PATH = None
D3 = False
N = 20
START = (3, 0)
TARGET = (N-1, N-1)

def init():
    # clear color to black
    glClearColor(0.0, 0.0, 0.0, 0.0)
    diffuse = [0.7, 0.7, 0.7, 1.0]
    specular = [0.001, 0.001, 0.001, 1.0]
    pos = [0, 0, 1.5, 0]
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glDepthFunc(GL_LESS)
    glClearDepth(1)

    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glLightfv(GL_LIGHT0, GL_POSITION, pos)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    init_random_grid(N)
    glEnable(GL_COLOR_MATERIAL)
    return

def calcul_color(i, j):
    # color = (255-GRID[i][j])/255
    color = (GRID[i][j])/255
    if color ==float('inf'):
        color = 0.0
    return color

def calcul_height(i, j):
    y = (GRID[i][j])/255 * 10
    if y == float('inf'):
        y = 0
    return y


def calculate_sense(p1, p2):
    x = p2[0]-p1[0]
    y = p2[1]-p1[1]
    if abs(x) == 1 and abs(y) == 1:
        return "diagonal"
    if y > 0 and x == 0:
        return "horizontal"
    return "vertical"


    return
def display():
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    gluLookAt(x_pos, y_pos, z_pos, #pos camera
              0+x_pos, -10+y_pos, -10+z_pos, # look at
              0, 1, 0) #up vector

    if DISPLAY_GRID :
        display_grid()

    for i in range(len(GRID)):
        for j in range(len(GRID[0])):
            x, z = (j, i)
            y = 0
            if D3:
                y = calcul_height(i, j)

            # main square draw
            glBegin(GL_POLYGON)
            color = calcul_color(i, j)
            glNormal3f(0.0, 1.0, 0.0)
            glColor3f(color, color, color)
            glVertex3f(2*x, y, 2*z)
            glVertex3f(2*x+1, y, 2*z)
            glVertex3f(2*x+1, y, 2*z+1)
            glVertex3f(2*x, y, 2*z+1)
            glEnd()

            # draw of horizontal rectangles
            if j+1 < len(GRID[0]):
                i_plus1_y = 0
                j_plus1_y = 0
                if D3:
                    j_plus1_y = calcul_height(i, j+1)

                glBegin(GL_POLYGON)
                color = calcul_color(i, j)
                glColor3f(color, color, color)
                glVertex3f(2*x+1, y, 2*z)
                glVertex3f(2*x+1, y, 2*z+1)
                color = calcul_color(i, j+1)
                glColor3f(color, color, color)
                glVertex3f(2*x+2, j_plus1_y, 2*z+1)
                glVertex3f(2*x+2, j_plus1_y, 2*z)
                glEnd()

            #draw of vertical rectangles
            if i+1 < len(GRID):
                if D3:
                    i_plus1_y = calcul_height(i+1, j)
                glBegin(GL_POLYGON)
                color = calcul_color(i, j)
                glColor3f(color, color, color)
                glVertex3f(2*x, y, 2*z+1)
                glVertex3f(2*x+1, y, 2*z+1)
                color = calcul_color(i+1, j)
                glColor3f(color, color, color)
                glVertex3f(2*x+1, i_plus1_y, 2*z+2)
                glVertex3f(2*x, i_plus1_y, 2*z+2)
                glEnd()

            #draw of inner triangles
            if D3:
                if i+1 < len(GRID) and j+1<len(GRID[0]):
                    ij_plus1_y = calcul_height(i+1, j+1)
                    i_plus1_y = calcul_height(i+1, j)
                    j_plus1_y = calcul_height(i, j+1)

                    glBegin(GL_POLYGON)

                    color = calcul_color(i, j)
                    glColor3f(color, color, color)
                    glVertex3f(2*x+1, y, 2*z+1)

                    color = calcul_color(i+1, j)
                    glColor3f(color, color, color)
                    glVertex3f(2*x+1, i_plus1_y, 2*z+2)

                    color = calcul_color(i+1, j+1)
                    glColor3f(color, color, color)
                    glVertex3f(2*x+2, ij_plus1_y, 2*z+2)

                    glEnd()

                    glBegin(GL_POLYGON)
                    color = calcul_color(i, j)
                    glColor3f(color, color, color)
                    glVertex3f(2*x+1, y, 2*z+1)

                    color = calcul_color(i, j+1)
                    glColor3f(color, color, color)
                    glVertex3f(2*x+2, j_plus1_y, 2*z+1)

                    color = calcul_color(i+1, j+1)
                    glColor3f(color, color, color)
                    glVertex3f(2*x+2, ij_plus1_y, 2*z+2)
                    glEnd()
    if PATH:
        glBegin(GL_LINES)
        for i in range(1, len(PATH)) :
            sz, sx = PATH[i-1]
            dz, dx = PATH[i]
            sense = calculate_sense(PATH[i-1], PATH[i])
            y_s, y_d = 0.5, 0.5
            if D3:
                y_s = (GRID[sz][sx])/255 *10 + .5
                y_d = (GRID[dz][dx])/255 * 10 + .5
            glColor3f (1.0, 0.0, 0.0);
            glVertex3f(2*sx+0.5, y_s, 2*sz+0.5);
            if sense == "horizontal":
                glVertex3f(2*sx+1, y_s, 2*sz+0.5);
                glVertex3f(2*sx+1, y_s, 2*sz+0.5);
                glVertex3f(2*dx, y_d, 2*dz+0.5);
                glVertex3f(2*dx, y_d, 2*dz+0.5);
            elif sense =="vertical":
                glVertex3f(2*sx+0.5, y_s, 2*sz+1);
                glVertex3f(2*sx+0.5, y_s, 2*sz+1);
                glVertex3f(2*dx+0.5, y_d, 2*dz);
                glVertex3f(2*dx+0.5, y_d, 2*dz);
            else:
                assert(sense =="diagonal")
                glVertex3f(2*sx+1, y_s, 2*sz+1);
                glVertex3f(2*sx+1, y_s, 2*sz+1);
                glVertex3f(2*dx, y_d, 2*dz);
                glVertex3f(2*dx, y_d, 2*dz);

            glVertex3f(2*dx+0.5, y_d, 2*dz+0.5);
        glEnd()

    glPopMatrix()
    glutSwapBuffers()
    return

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(110, width/height, 3, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    return


def keyboard(key, x, y):
    global x_pos, y_pos, z_pos, DISPLAY_GRID, PATH, D3
    if key == b'g':
        DISPLAY_GRID = not DISPLAY_GRID
    elif key == b'3':
        D3 = not D3
    elif key == b'p':
        for line in GRID:
            print(line)
        PATH = dijkstra_sd(GRID, START, TARGET)
    elif key == b'w':
        y_pos -= 1
    elif key == b's':
        y_pos += 1
    elif key == b'j':
        z_pos += 1
    elif key == b'k':
        z_pos -= 1
    elif key == b'h':
        x_pos -= 1
    elif key == b'l':
        x_pos += 1
    elif key == b'\033':
        glutDestroyWindow(WIN)
        sys.exit(0)
    glutPostRedisplay()  # indispensable en Python
    return

###############################################################
# MAIN

def smooth(grid):
    grid_copy = deepcopy(grid)
    dv = [-1, 0, 1]
    dh = [-1, 0, 1]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            neighbours = 0
            sum_neigh = 0
            for v in dv:
                for h in dh:
                    if v != 0 and h != 0 and 0 <= i+v < len(grid) \
                       and 0 <= j+h < len(grid[0]):
                        sum_neigh += grid[i+v][j+h]
                        neighbours += 1
            grid_copy[i][j] = sum_neigh/neighbours

    return grid_copy

def median_smooth(grid):
    grid_copy = deepcopy(grid)
    dv = [-1, 0, 1]
    dh = [-1, 0, 1]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            neigh = []
            for v in dv:
                for h in dh:
                    if 0 <= i+v < len(grid) and 0 <= j+h < len(grid[0]):
                        neigh.append(grid[i+v][j+h])
            neigh.sort()
            n = len(neigh)
            mid = n//2
            if n % 2 == 0:
                # pair
                grid_copy[i][j] = (neigh[mid] + neigh[mid+1]) / 2
            else:
                grid_copy[i][j] = neigh[mid]
    return grid_copy

def init_random_grid(n):
    global GRID
    grid = [[random.randint(0, 255) for x in range(n)] for x in range(n)]
    grid = median_smooth(grid)
    # grid = smooth(grid)
    rd_line, rd_col = random.randint(0, n), random.randint(0, n)
    for j in range(n):
        print(rd_line, j)
        grid[rd_line][j] = float('inf')
    grid[rd_line][rd_col] = random.randint(0, 255)
    GRID = grid
    return


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA |GLUT_DEPTH )
    WIN = glutCreateWindow('projet')
    glutReshapeWindow(512, 512)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    init()
    print(glGetString(GL_VERSION))
    glutMainLoop()
