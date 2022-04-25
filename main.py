from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
# from Image import open
# from PIL import Image
# from math import cos, sin, sqrt
from copy import deepcopy
from dijkstra import dijkstra_matrix_sorted_dict
from linear_algebra import LineSegment, Vector, Point

INF = float('inf')


def barycenter_calculation(a: Point, b: Point, c: Point):
    """Calcul le barycentre d'un triangle."""
    v_a = Vector(Point(*a.to_tuple()))
    v_b = Vector(Point(*b.to_tuple()))
    v_c = Vector(Point(*c.to_tuple()))
    sum_ = v_a + v_b + v_c
    return Point(sum_.x / 3, sum_.y / 3, sum_.z / 3)


def rescale_normal(nv: Vector, norm: int):
    """Renvoie le point pour que le vector aie une norme norm."""
    scale = sqrt(norm / (nv.x**2 + nv.y**2 + nv.z**2))
    return Point(scale * nv.x, scale * nv.y, scale * nv.z)


def display_grid():
    """
    Affichage de la grille.

    Affiche un grille pour un meilleur comprehension
    du mouvement de la camera.
    """
    glBegin(GL_LINES);

    n = 90
    for i in range(-n, n):
        # x, y
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(i, -n, 0.0)
        glVertex3f(i, n, 0.0)

        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(-n, i, 0.0)
        glVertex3f(n, i, 0.0)

        #x, z
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(i, 0.0, -n)
        glVertex3f(i, 0.0, n)

        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(-n, 0.0, i)
        glVertex3f(n, 0.0, i)

        #y, z
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(0.0, i, -n)
        glVertex3f(0.0, i, n)

        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(0.0, -n, i)
        glVertex3f(0.0, n, i)

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
START = (0, N - 1)
TARGET = (N - 1, 0)
MOVE_WORM = 0
NORMALS = False


def init():
    """Initialisation des variables et lumiere openGL."""
    # clear color to black
    glClearColor(0.0, 0.0, 0.0, 0.0)
    # diffuse = [0.7, 0.7, 0.7, 1.0]
    # specular = [0.001, 0.001, 0.001, 1.0]
    pos = [1, 50, 50, 1]
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glDepthFunc(GL_LESS)
    glClearDepth(1)

    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glLightfv(GL_LIGHT0, GL_POSITION, pos)
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    # glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    init_random_grid(N)
    return


def calculate_color(i, j):
    """Calcul du color selon la coordonnee (i,j)."""
    color = GRID[i][j] / 255
    if color == INF:
        color = .0
    return color


def calculate_height(i, j):
    """Calcul du hauteur selon la coordonnee (i,j)."""
    y = GRID[i][j] / 255 * 10
    if y == INF:
        y = 0
    return y


def calculate_sense(p1, p2):
    """Pp1 --> p2."""
    y = p2[0] - p1[0]
    x = p2[1] - p1[1]
    if x == -1 and y == -1:
        return "rdiagonal down"
    if x == 1 and y == 1:
        return "rdiagonal up"
    if x == -1 and y == 1:
        return "ldiagonal down"
    if x == -1 and y == 1:
        return "ldiagonal down"
    if x == 1 and y == -1:
        return "ldiagonal down"
    if y == 0 and x == -1:
        return "horizontal left"
    if y == 0 and x == 1:
        return "horizontal right"
    elif y == -1 and x == 0 :
        return "vertical up"
    elif y == 1 and x == 0:
        return "vertical down"
    raise TypeError
    return None

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    gluLookAt(x_pos, y_pos, z_pos,  # pos camera
              x_pos, -10 + y_pos, -10 + z_pos,  # look at
              0, 1, 0)  # up vector
    sph1 = gluNewQuadric()

    if DISPLAY_GRID :
        display_grid()
    glClearColor(0.0, 0.0, 0.0, 0.0)

    for i in range(len(GRID)):
        for j in range(len(GRID[0])):
            x, z = (j, i)
            y = 0
            if D3:
                y = calculate_height(i, j)

            # main square draw
            glBegin(GL_POLYGON)
            color = calculate_color(i, j)

            glNormal3f(0.0, 1.0, 0.0)
            # glColor3f(color, color, color)
            glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [color, color, color, 1])
            glVertex3f(2 * x, y, 2 * z)
            glVertex3f(2 * x + 1, y, 2 * z)
            glVertex3f(2 * x + 1, y, 2 * z + 1)
            glVertex3f(2 * x, y, 2 * z + 1)
            glEnd()
            if NORMALS:
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                a_, b_, c_ = (2 * x + .5, y, 2 * z + .5)
                glTranslatef(a_, b_, c_)
                gluSphere(sph1, 0.1, 5, 5)
                glTranslatef(-a_, -b_, -c_)

                glBegin(GL_LINES)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                normal = Vector(Point(0, 1, 0))
                glNormal(*normal.to_tuple())
                glVertex(2 * x + .5, y, 2 * z + .5)
                a, b, c = rescale_normal(normal, 0.5).to_tuple()
                glVertex3f(a_ + a, b_ + b, c_ + c)
                glEnd()

            # draw of horizontal rectangles
            if j + 1 < len(GRID[0]):
                i_plus1_y = 0
                j_plus1_y = 0
                if D3:
                    j_plus1_y = calculate_height(i, j+1)

                glBegin(GL_POLYGON)
                color = calculate_color(i, j)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])

                v0 = Vector(Point(2 * x + 1, y, 2 * z))
                v1 = Vector(Point(2 * x + 2, j_plus1_y, 2 * z))
                v2 = Vector(Point(2 * x + 1, y, 2 * z + 1))
                v1 = v1 - v0
                v2 = v2 - v0
                normal = v2 ^ v1
                glNormal3f(*normal.to_tuple())
                glVertex3f(2 * x + 1, y, 2 * z)
                glVertex3f(2 * x + 1, y, 2 * z + 1)
                color = calculate_color(i, j + 1)

                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
                glVertex3f(2 * x + 2, j_plus1_y, 2 * z + 1)
                glVertex3f(2 * x + 2, j_plus1_y, 2 * z)
                glEnd()
                if NORMALS:
                    a = Point(2 * x + 1, y, 2 * z)
                    b = Point(2 * x + 2, j_plus1_y, 2 * z + 1)
                    seg = LineSegment(a, b)
                    a_, b_, c_ = seg.mid_point().to_tuple()
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                    glTranslatef(a_, b_, c_)
                    gluSphere(sph1, 0.1, 5, 5)
                    glTranslatef(-a_, -b_, -c_)

                    glBegin(GL_LINES)
                    glNormal3f(0, 1, 0)
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                    glVertex3f(a_, b_, c_)
                    a, b, c = rescale_normal(normal, 0.5).to_tuple()
                    glVertex3f(a_ + a, b_ + b, c_ + c)
                    glEnd()

            # draw of vertical rectangles
            if i + 1 < len(GRID):
                i_plus1_y = 0
                if D3:
                    i_plus1_y = calculate_height(i + 1, j)
                glBegin(GL_POLYGON)
                v0 = Vector(Point(2 * x, y, 2 * z + 1))
                v1 = Vector(Point(2 * x + 1, y, 2 * z + 1))
                v2 = Vector(Point(2 * x, i_plus1_y, 2 * z + 2))
                v1 = v1 - v0
                v2 = v2 - v0
                normal = v2 ^ v1
                glNormal3f(*normal.to_tuple())
                color = calculate_color(i, j)

                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
                glVertex3f(2 * x, y, 2 * z + 1)
                glVertex3f(2 * x + 1, y, 2 * z + 1)
                color = calculate_color(i + 1, j)

                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
                glVertex3f(2 * x + 1, i_plus1_y, 2 * z + 2)
                glVertex3f(2 * x, i_plus1_y, 2 * z + 2)
                glNormal3f(0, 1, 0)
                glEnd()
                if NORMALS:
                    a = Point(2 * x, y, 2 * z + 1)
                    b = Point(2 * x + 1, i_plus1_y, 2 * z + 2)
                    seg = LineSegment(a, b)
                    a_, b_, c_ = seg.mid_point().to_tuple()
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                    glTranslatef(a_, b_, c_)
                    gluSphere(sph1, 0.1, 5, 5)
                    glTranslatef(-a_, -b_, -c_)

                    glBegin(GL_LINES)
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                    glVertex3f(a_, b_, c_)
                    a, b, c = rescale_normal(normal, 0.5).to_tuple()
                    glVertex3f(a_ + a, b_ + b, c_ + c)
                    glEnd()
            # draw of inner triangles
            if i + 1 < len(GRID) and j + 1 < len(GRID[0]):
                ij_plus1_y = 0
                i_plus1_y = 0
                j_plus1_y = 0
                if D3:
                    ij_plus1_y = calculate_height(i + 1, j + 1)
                    i_plus1_y = calculate_height(i + 1, j)
                    j_plus1_y = calculate_height(i, j + 1)

                glBegin(GL_POLYGON)
                v0 = Vector(Point(2 * x + 1, y, 2 * z + 1))
                v1 = Vector(Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                v2 = Vector(Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                v1 = v1 - v0
                v2 = v2 - v0
                normal = v2 ^ v1
                glNormal3f(*normal.to_tuple())
                color = calculate_color(i, j)

                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
                glVertex3f(2 * x + 1, y, 2 * z + 1)

                color = calculate_color(i + 1, j)

                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
                glVertex3f(2 * x + 1, i_plus1_y, 2 * z + 2)

                color = calculate_color(i + 1, j + 1)

                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
                glVertex3f(2 * x + 2, ij_plus1_y, 2 * z + 2)

                glNormal3f(0, 1, 0)
                glEnd()
                if NORMALS:
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0,0, 1])
                    barycenter = barycenter_calculation(Point(2*x+1, y, 2*z+1),
                                                        Point(2*x+2, ij_plus1_y, 2*z+2),
                                                        Point(2*x+1, i_plus1_y, 2*z+2))
                    bx, by, bz = (barycenter.to_tuple())
                    a_, b_, c_ = (barycenter.to_tuple())
                    glTranslatef(bx, by, bz)
                    gluSphere(sph1, 0.1, 5, 5)
                    glTranslatef(-bx, -by, -bz)

                    glBegin(GL_LINES)
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0,0, 1])
                    new_normal = Vector(rescale_normal(normal, 0.5))
                    glVertex3f(a_, b_, c_)
                    a, b, c = new_normal.translate(barycenter).to_tuple()
                    glVertex3f(a, b, c)
                    glEnd()


                glBegin(GL_POLYGON)
                v0 = Vector(Point(2*x+1, y, 2*z+1))
                v1 = Vector(Point(2*x+2, j_plus1_y, 2*z+1))
                v2 = Vector(Point(2*x+2, ij_plus1_y, 2*z+2))
                v1 = v1-v0
                v2 = v2-v0
                normal = v2 ^ v1
                glNormal3f(*normal.to_tuple())
                color = calculate_color(i, j)
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [color, color, color, 1])
                glVertex3f(2*x+1, y, 2*z+1)

                color = calculate_color(i, j+1)
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [color, color, color, 1])
                glVertex3f(2*x+2, j_plus1_y, 2*z+1)

                color = calculate_color(i+1, j+1)
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [color, color, color, 1])
                glVertex3f(2*x+2, ij_plus1_y, 2*z+2)
                glEnd()
                if NORMALS:
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0,0, 1])
                    barycenter = barycenter_calculation(Point(2*x+1, y, 2*z+1),
                                                        Point(2*x+2, j_plus1_y, 2*z+1),
                                                        Point(2*x+2, ij_plus1_y, 2*z+2))
                    bx, by, bz = (barycenter.to_tuple())
                    a_, b_, c_ = (barycenter.to_tuple())
                    glTranslatef(bx, by, bz)
                    gluSphere(sph1, 0.1, 5, 5)
                    glTranslatef(-bx, -by, -bz)

                    glBegin(GL_LINES)
                    new_normal = Vector(rescale_normal(normal, 0.5))
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0,0, 1])
                    glVertex3f(a_, b_, c_)
                    a, b, c = new_normal.translate(barycenter).to_tuple()
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0,0, 1])
                    glVertex3f(a, b, c)
                    glEnd()
#     if PATH:
#         pts = []
#         glBegin(GL_LINES)
#         for i in range(1, len(PATH)) :
#             sz, sx = PATH[i-1]
#             dz, dx = PATH[i]
#             sense = calculate_sense(PATH[i-1], PATH[i])
#             y_s, y_d = 0.5, 0.5
#             if D3:
#                 y_s = (GRID[sz][sx])/255 *10 + .5
#                 y_d = (GRID[dz][dx])/255 * 10 + .5
#             glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [color, color, color, 1])
#             # glColor3f (1.0, 0.0, 0.0);
#             glVertex3f(2*sx+0.5, y_s, 2*sz+0.5)
#             pts.append((2*sx+0.5, y_s, 2*sz+0.5))
#             print(sense)
#             if sense == "horizontal left":
#                 glVertex3f(2*sx, y_s, 2*sz+0.5)
#                 glVertex3f(2*sx, y_s, 2*sz+0.5)
#                 glVertex3f(2*dx+1, y_d, 2*dz+0.5)
#                 glVertex3f(2*dx+1, y_d, 2*dz+0.5)
#                 pts.append((2*sx, y_s, 2*sz+0.5))
#                 pts.append((2*dx+1, y_d, 2*dz+0.5))
#             if sense == "horizontal right":
#                 glVertex3f(2*sx+1, y_s, 2*sz+0.5)
#                 glVertex3f(2*sx+1, y_s, 2*sz+0.5)
#                 glVertex3f(2*dx, y_d, 2*dz+0.5)
#                 glVertex3f(2*dx, y_d, 2*dz+0.5)
#                 pts.append((2*sx+1, y_s, 2*sz+0.5))
#                 pts.append((2*dx, y_d, 2*dz+0.5))
#             elif sense =="vertical down":
#                 glVertex3f(2*sx+0.5, y_s, 2*sz+1)
#                 glVertex3f(2*sx+0.5, y_s, 2*sz+1)
#                 glVertex3f(2*dx+0.5, y_d, 2*dz)
#                 glVertex3f(2*dx+0.5, y_d, 2*dz)
#                 pts.append((2*sx+0.5, y_s, 2*sz+1))
#                 pts.append((2*dx+0.5, y_d, 2*dz))
#             elif sense =="vertical up":
#                 glVertex3f(2*sx+0.5, y_s, 2*sz)
#                 glVertex3f(2*sx+0.5, y_s, 2*sz)
#                 glVertex3f(2*dx+0.5, y_d, 2*dz+1)
#                 glVertex3f(2*dx+0.5, y_d, 2*dz+1)
#                 pts.append((2*sx+0.5, y_s, 2*sz))
#                 pts.append((2*dx+0.5, y_d, 2*dz+1))
#             elif sense =="ldiagonal down":
#                 glVertex3f(2*sx, y_s, 2*sz+1)
#                 glVertex3f(2*sx, y_s, 2*sz+1)
#                 i, j = PATH[i-1]
#                 left_h = 0.5
#                 down_h = 0.5
#                 if D3:
#                     left_h = calculate_height(i, j-1)+0.5
#                     down_h = calculate_height(i+1, j)+0.5
#                 mid_p_h = ((2*sx-1 + 2*sx)/2,(left_h+down_h)/2, (2*sz+2 + 2*sz+1)/2)
#                 glVertex3f(*mid_p_h)
#                 glVertex3f(*mid_p_h)
#                 glVertex3f(2*dx+1, y_d, 2*dz)
#                 glVertex3f(2*dx+1, y_d, 2*dz)
#                 pts.append((2*sx, y_s, 2*sz+1))
#                 pts.append(mid_p_h)
#                 pts.append((2*dx+1, y_d, 2*dz))
#             elif sense =="ldiagonal up":
#                 glVertex3f(2*sx+1, y_s, 2*sz)
#                 glVertex3f(2*sx+1, y_s, 2*sz)
#                 glVertex3f(2*dx, y_d, 2*dz+1)
#                 glVertex3f(2*dx, y_d, 2*dz+1)
#                 pts.append((2*sx+1, y_s, 2*sz))
#                 pts.append((2*dx, y_d, 2*dz+1))
#             elif sense =="rdiagonal down":
#                 glVertex3f(2*sx+1, y_s, 2*sz+1)
#                 glVertex3f(2*sx+1, y_s, 2*sz+1)
#                 glVertex3f(2*dx, y_d, 2*dz)
#                 glVertex3f(2*dx, y_d, 2*dz)
#                 pts.append((2*sx+1, y_s, 2*sz+1))
#                 pts.append((2*dx, y_d, 2*dz))
#             elif sense =="rdiagonal up":
#                 glVertex3f(2*sx, y_s, 2*sz)
#                 glVertex3f(2*sx, y_s, 2*sz)
#                 glVertex3f(2*dx+1, y_d, 2*dz+1)
#                 glVertex3f(2*dx+1, y_d, 2*dz+1)
#                 pts.append((2*sx, y_d, 2*sz))
#                 pts.append((2*dx+1, y_d, 2*dz+1))
#             else:
#                 print(sense)
#                 # glVertex3f(2*sx, y_s, 2*sz+1)
#                 # glVertex3f(2*sx, y_s, 2*sz+1)
#                 # glVertex3f(2*dx+1, y_d, 2*dz)
#                 # glVertex3f(2*dx+1, y_d, 2*dz)
#                 # pts.append((2*sx, y_s, 2*sz+1))
#                 # pts.append((2*dx+1, y_d, 2*dz+1))
#             glVertex3f(2*dx+0.5, y_d, 2*dz+0.5);
#         glEnd()

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1])
        glTranslatef(*pts[MOVE_WORM % len(pts)])
        gluQuadricDrawStyle(sph1, GLU_FILL)
        gluQuadricNormals(sph1, GLU_SMOOTH)
        gluQuadricTexture(sph1, GL_TRUE)
        gluSphere(sph1, 0.4, 100, 80)
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
    global x_pos, y_pos, z_pos, DISPLAY_GRID, PATH, D3, MOVE_WORM, NORMALS
    if key == b'g':
        DISPLAY_GRID = not DISPLAY_GRID
    elif key == b'3':
        D3 = not D3
    elif key == b'p':
        for line in GRID:
            print(line)
        PATH = dijkstra_matrix_sorted_dict(GRID, START, TARGET)
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
    elif key == b'm':
        MOVE_WORM += 1
    elif key == b'n':
        NORMALS = not NORMALS
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

def tuckey_smooth(grid: list[list], radius: int):
    grid_copy = deepcopy(grid)
    dep = [x for x in range(-radius, radius+1)]
    dep = [x for x in range(-radius, radius+1)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            neigh = []
            for v in dep:
                for h in dep:
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
    random.seed(1)
    grid = [[random.randint(0, 255) for x in range(n)] for x in range(n)]
    grid = tuckey_smooth(grid, 1)
    # grid = smooth(grid)
    rd_line, rd_col = random.randint(0, n-1), random.randint(0, n-1)
    while rd_line !=TARGET[0] and rd_line ==START[0] :
        rd_line, rd_col = random.randint(0, n-1), random.randint(0, n-1)
    for j in range(n):
        grid[rd_line][j] = INF
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
