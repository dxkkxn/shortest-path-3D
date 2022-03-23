#!/usr/bin/env python3

###############################################################
# portage de planet.c

from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
# from Image import open
from PIL import Image
from math import cos, sin
from copy import deepcopy


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
    init_random_grid(9)
    glEnable(GL_COLOR_MATERIAL)
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
            glBegin(GL_POLYGON)
            color = (255-GRID[i][j])/255
            # print(color)

            glNormal3f(0.0, 1.0, 0.0)
            glColor3f(color, color, color)

            x, z = (j, i)
            y = 0
            if D3:
                y = color * 10
            glVertex3f(x, y, z)
            glVertex3f(x+1, y, z)
            glVertex3f(x+1, y, z+1)
            glVertex3f(x, y, z+1)

            glEnd()
    if PATH:
        glBegin(GL_LINES)
        for i in range(1, len(PATH)) :
            sy, sx = PATH[i-1]
            dy, dx = PATH[i]
            y_s, y_d = 0.5, 0.5
            if D3:
                y_s = (GRID[sy][sx])/255 *10
                y_d = (GRID[dy][dx])/255 * 10
            glColor3f (1.0, 0.0, 0.0);
            glVertex3f(sx+0.5, y_s, sy+0.5);
            glVertex3f(dx+0.5, y_d, dy+0.5);
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
        PATH = (dijkstra(GRID))
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
            sum_neigh = []
            for v in dv:
                for h in dh:
                    if v != 0 and h != 0 and 0 <= i+v < len(grid) \
                       and 0 <= j+h < len(grid[0]):
                        sum_neigh.append(grid[i+v][j+h])
            grid_copy[i][j] = sum_neigh[len(sum_neigh)//2]

    return grid_copy
def found_min(w, m):
    min_key = None
    min_val = float('inf')
    for key, val in w.items():
        if val < min_val and key not in m:
            min_key = key
            min_val = val

    if min_key == None:
        print(min_key, len(m), len(w))
        print(m)
        print(w)
    return min_key

def dijkstra(grid):
    from time import sleep
    weight = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            weight[(i, j)] = float('inf')

    mark = {}
    weight[(0, 0)] = 0
    prev = {}
    dest = (len(grid)-1, len(grid[0])-1)
    while dest not in mark :
        # found the vertex with smallest weight
        curr_i, curr_j = found_min(weight, mark)
        # for each neighbour modify weight dico
        dv = [-1, 0, 1]
        dh = [-1, 0, 1]
        for v in dv:
            for h in dh:
                if not(v == 0 and h == 0) and 0 <= curr_i+v < len(grid) \
                    and 0 <= curr_j+h < len(grid[0]):
                    curr_weight = weight[(curr_i, curr_j)] + grid[curr_i+v][curr_j+h]
                    if curr_weight < weight[curr_i+v, curr_j+h]:
                        weight[curr_i+v, curr_j+h] = curr_weight
                        prev[(curr_i+v, curr_j+h)] = (curr_i, curr_j)
        mark[(curr_i, curr_j)] = True
    curr_node= (dest)
    path = [dest]
    while curr_node != (0, 0):
        path.append(prev[curr_node])
        curr_node = prev[curr_node]
    path.reverse()
    print(path)

    return path



def init_random_grid(n):
    global GRID
    grid = [[random.randint(0, 255) for x in range(n)] for x in range(n)]
    grid = median_smooth(grid)

    GRID = grid


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
