import random
import sys
# from Image import open
# from PIL import Image
from math import sqrt
from copy import deepcopy
from dijkstra import dijkstra_matrix_sorted_dict
from linear_algebra import LineSegment, Vector, Point
from water_rendering import init_water, water_render
import time
import tkinter as tk
from tkinter import ttk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from OpenGL import *

inf = float('inf')


def barycenter_calculation(a: Point, b: Point, c: Point):
    """Calcul le barycentre d'un triangle."""
    v_a = Vector(Point(*a.to_tuple()))
    v_b = Vector(Point(*b.to_tuple()))
    v_c = Vector(Point(*c.to_tuple()))
    sum_ = v_a + v_b + v_c
    return Point(sum_.x / 3, sum_.y / 3, sum_.z / 3)


def rescale_normal(nv: Vector, norm: int):
    """Renvoie le vector nv a echelle i.e pour que il aie une norme norm."""
    scale = sqrt(norm / (nv.x**2 + nv.y**2 + nv.z**2))
    return Vector(Point(scale * nv.x, scale * nv.y, scale * nv.z))

def draw_normals():
    """Affichage des normals."""
    sph1 = gluNewQuadric()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x, z = (j, i)
            y = 0
            if D3:
                y = calculate_height(i, j)
            glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
            # draw of main squares
            # centre of de square
            cx, cy, cz = (2 * x + .5, y, 2 * z + .5)
            glTranslatef(cx, cy, cz)
            gluSphere(sph1, 0.1, 5, 5)
            glTranslatef(-cx, -cy, -cz)

            glBegin(GL_LINES)
            glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
            normal = Vector(Point(0, 1, 0))
            glVertex(cx, cy, cz)
            res_normal = rescale_normal(normal, 0.5)
            glVertex3fv(res_normal.translate(Point(cx, cy, cz)).to_tuple())
            glEnd()
            # horizontal rectangles
            j_plus1_y = 0
            if j + 1 < len(grid[0]):
                if D3:
                    j_plus1_y = calculate_height(i, j + 1)

                p0 = Point(2 * x + 1, y, 2 * z)
                v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z))
                v2 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                normal = v2 ^ v1

                a = Point(2 * x + 1, y, 2 * z)
                b = Point(2 * x + 2, j_plus1_y, 2 * z + 1)
                seg = LineSegment(a, b)
                # center of the rectangle
                cx, cy, cz = seg.mid_point().to_tuple()
                glTranslatef(cx, cy, cz)
                gluSphere(sph1, 0.1, 5, 5)
                glTranslatef(-cx, -cy, -cz)

                glBegin(GL_LINES)
                glNormal3f(0, 1, 0)
                glVertex3f(cx, cy, cz)
                res_normal = rescale_normal(normal, 0.5)
                glVertex3fv(res_normal.translate(Point(cx, cy, cz)).to_tuple())
                glEnd()

            if i + 1 < len(grid):
                i_plus1_y = 0
                if D3:
                    i_plus1_y = calculate_height(i + 1, j)
                # vertical rectangles
                p0 = Point(2 * x, y, 2 * z + 1)
                v1 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                v2 = Vector(p0, Point(2 * x, i_plus1_y, 2 * z + 2))
                normal = v2 ^ v1
                a = Point(2 * x, y, 2 * z + 1)
                b = Point(2 * x + 1, i_plus1_y, 2 * z + 2)
                seg = LineSegment(a, b)
                # centre du rectangle
                cx, cy, cz = seg.mid_point().to_tuple()
                glTranslatef(cx, cy, cz)
                gluSphere(sph1, 0.1, 5, 5)
                glTranslatef(-cx, -cy, -cz)

                glBegin(GL_LINES)
                glVertex3f(cx, cy, cz)
                res_normal = rescale_normal(normal, 0.5)
                glVertex3fv(res_normal.translate(Point(cx, cy, cz)).to_tuple())
                glEnd()

            # inner triagle
            if i + 1 < len(grid) and j + 1 < len(grid[0]):
                ij_plus1_y = 0
                i_plus1_y = 0
                j_plus1_y = 0
                if D3:
                    ij_plus1_y = calculate_height(i + 1, j + 1)
                    i_plus1_y = calculate_height(i + 1, j)
                    j_plus1_y = calculate_height(i, j + 1)

                p0 = (Point(2 * x + 1, y, 2 * z + 1))
                v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z + 1))
                v2 = Vector(p0, Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                normal = v2 ^ v1

                barycenter = barycenter_calculation(Point(2 * x + 1, y, 2 * z + 1),
                                                    Point(2 * x + 2, j_plus1_y, 2 * z + 1),
                                                    Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                bx, by, bz = (barycenter.to_tuple())
                glTranslatef(bx, by, bz)
                gluSphere(sph1, 0.1, 5, 5)
                glTranslatef(-bx, -by, -bz)

                glBegin(GL_LINES)
                res_normal = rescale_normal(normal, 0.5)
                glVertex3f(bx, by, bz)
                glVertex3fv(res_normal.translate(barycenter).to_tuple())
                glEnd()

                barycenter = barycenter_calculation(Point(2 * x + 1, y, 2 * z + 1),
                                                    Point(2 * x + 2, ij_plus1_y, 2 * z + 2),
                                                    Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                p0 = Point(2 * x + 1, y, 2 * z + 1)
                v1 = Vector(p0, Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                v2 = Vector(p0, Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                normal = v2 ^ v1
                bx, by, bz = (barycenter.to_tuple())
                glTranslatef(bx, by, bz)
                gluSphere(sph1, 0.1, 5, 5)
                glTranslatef(-bx, -by, -bz)

                glBegin(GL_LINES)
                glMaterialfv(
                    GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [
                        1, 0, 0, 1])
                res_normal = rescale_normal(normal, 0.5)
                glVertex3f(bx, by, bz)
                glVertex3fv(res_normal.translate(Point(bx, by, bz)).to_tuple())
                glEnd()

def display_grid():
    """
    Affichage de la grille.

    Affiche un grille pour un meilleur comprehension
    du mouvement de la camera.
    """
    glBegin(GL_LINES)

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
DISPLAY_grid = False
grid = None
PATH = None
D3 = False
# N = 20
start = (None, None)
target = (None, None)
MOVE_WORM = 0
NORMALS = False
DRAW_PATH = False
y_water = -1

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
    # init_random_grid(12)
    init_water()
    glDisable(GL_TEXTURE_2D)
    return


def calculate_color(i, j):
    """Calcul du color selon la coordonnee (i,j)."""
    color = old_grid[i][j] / 255
    if color == inf:
        color = .0
    return color


def calculate_height(i, j):
    """Calcul du hauteur selon la coordonnee (i,j)."""
    y = old_grid[i][j] / 255 * 10
    if y == inf:
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
    elif y == -1 and x == 0:
        return "vertical up"
    elif y == 1 and x == 0:
        return "vertical down"
    raise TypeError
    return None

def random_point(point: Point):
    x, y, z = point.to_tuple()
    points = [point, Point(x + .5, y, z), Point(x + 1, y, z),
                  Point(x, y, z + .5), Point(x + .5, y, z + .5),
                  Point(x, y, z + 1), Point(x + .5, y, z + 1),
                  Point(x + 1, y, z+ 1)]
    return random.choice(points)

CONTROL_PTS = []
def display():
    global PATH, CONTROL_PTS
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    gluLookAt(x_pos, y_pos, z_pos,  # pos camera
              x_pos, -10 + y_pos, -10 + z_pos,  # look at
              0, 1, 0)  # up vector
    sph1 = gluNewQuadric()

    if DISPLAY_grid:
        display_grid()
    glClearColor(0.0, 0.0, 0.0, 0.0)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x, z = (j, i)
            y = 0
            if D3:
                y = calculate_height(i, j)

            # main square draw
            glBegin(GL_POLYGON)
            color = calculate_color(i, j)

            glNormal3f(0.0, 1.0, 0.0)
            # glColor3f(color, color, color)
            glMaterialfv(
                GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [
                    color, color, color, 1])
            glVertex3f(2 * x, y, 2 * z)
            glVertex3f(2 * x + 1, y, 2 * z)
            glVertex3f(2 * x + 1, y, 2 * z + 1)
            glVertex3f(2 * x, y, 2 * z + 1)
            glEnd()

            # draw of horizontal rectangles
            if j + 1 < len(grid[0]):
                i_plus1_y = 0
                j_plus1_y = 0
                if D3:
                    j_plus1_y = calculate_height(i, j + 1)

                glBegin(GL_POLYGON)
                color = calculate_color(i, j)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])

                p0 = Point(2 * x + 1, y, 2 * z)
                v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z))
                v2 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
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

            # draw of vertical rectangles
            if i + 1 < len(grid):
                i_plus1_y = 0
                if D3:
                    i_plus1_y = calculate_height(i + 1, j)
                glBegin(GL_POLYGON)
                p0 = Point(2 * x, y, 2 * z + 1)
                v1 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                v2 = Vector(p0, Point(2 * x, i_plus1_y, 2 * z + 2))
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
            # draw of inner triangles
            if i + 1 < len(grid) and j + 1 < len(grid[0]):
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

                glBegin(GL_POLYGON)
                v0 = Vector(Point(2 * x + 1, y, 2 * z + 1))
                v1 = Vector(Point(2 * x + 2, j_plus1_y, 2 * z + 1))
                v2 = Vector(Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                v1 = v1 - v0
                v2 = v2 - v0
                normal = v2 ^ v1
                glNormal3f(*normal.to_tuple())
                color = calculate_color(i, j)
                glMaterialfv(
                    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [
                        color, color, color, 1])
                glVertex3f(2 * x + 1, y, 2 * z + 1)

                color = calculate_color(i, j + 1)
                glMaterialfv(
                    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [
                        color, color, color, 1])
                glVertex3f(2 * x + 2, j_plus1_y, 2 * z + 1)

                color = calculate_color(i + 1, j + 1)
                glMaterialfv(
                    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [
                        color, color, color, 1])
                glVertex3f(2 * x + 2, ij_plus1_y, 2 * z + 2)
                glEnd()
    if NORMALS:
        draw_normals()
    if PATH:
        pts = []
        sz, sx = PATH[0]
        y_s, y_d = 0.5, 0.5
        if D3:
            y_s = (grid[sz][sx]) / 255 * 10 + .5
        pts.append(Point(2 * sx + 0.5, y_s, 2 * sz + 0.5))
        point_prec = Point(2 * sx + 0.5, y_s, 2 * sz + 0.5)
        for i in range(1, len(PATH)):
            sz, sx = PATH[i - 1]
            dz, dx = PATH[i]
            sense = calculate_sense(PATH[i - 1], PATH[i])
            print(sense)
            y_s, y_d = 0.5, 0.5
            if D3:
                y_s = (grid[sz][sx]) / 255 * 10 + .5
                y_d = (grid[dz][dx]) / 255 * 10 + .5
            if sense == "horizontal left":
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))

                pts.append(Point(2 * sx, y_s, 2 * sz + 0.5))

                segment_sup = LineSegment(Point(2 * sx, y_s, 2 * sz),
                                          Point(2 * dx + 1, y_d, 2 * dz))

                segment_inf = LineSegment(Point(2 * sx + 1, y_s, 2 * sz + 1),
                                          Point(2 * dx, y_d, 2 * dz + 1))

                mid_p = segment_sup.mid_point()
                pts.append(mid_p)
                mid_p = segment_inf.mid_point()
                pts.append(mid_p)

                pts.append(Point(2 * dx + 1, y_d, 2 * dz + 0.5))
                point_prec = Point(2 * dx + 1, y_d, 2 * dz + 0.5)
            elif sense == "horizontal right":
                pts.append(Point(2 * sx + 1, y_s, 2 * sz + 0.5))
                pts.append(Point(2 * dx, y_d, 2 * dz + 0.5))
            elif sense == "vertical down":
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))

                pts.append(Point(2 * sx + 0.5, y_s, 2 * sz + 1))

                segment_sup = LineSegment(Point(2 * sx, y_s, 2 * sz + 1),
                                          Point(2 * dx, y_d, 2 * dz))

                segment_inf = LineSegment(Point(2 * sx + 1, y_s, 2 * sz + 1),
                                          Point(2 * dx + 1, y_d, 2 * dz))

                mid_p = segment_sup.mid_point()
                pts.append(mid_p)
                mid_p = segment_inf.mid_point()
                pts.append(mid_p)

                pts.append(Point(2 * dx + 0.5, y_d, 2 * dz))
            elif sense == "vertical up":
                pts.append(Point(2 * sx + 0.5, y_s, 2 * sz))
                pts.append(Point(2 * dx + 0.5, y_d, 2 * dz + 1))
            elif sense == "ldiagonal down":
                i, j = PATH[i - 1]
                left_h = 0.5
                down_h = 0.5

                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))

                pts.append(Point(2 * sx, y_s, 2 * sz + 1))
                if D3:
                    left_h = calculate_height(i, j - 1) + .5
                    print(i+1, j)
                    down_h = calculate_height(i + 1, j) + .5

                s_down = Point(2 * sx, down_h, 2 * sz + 2)
                s_left = Point(2 * sx - 1, left_h, 2 * sz + 1)
                vertex = (Point(2 * sx, y_s, 2 * sz + 1))
                seg_down = LineSegment(vertex, s_down)
                seg_left = LineSegment(vertex, s_left)

                pts.append(seg_down.mid_point())
                pts.append(seg_left.mid_point())

                mid_p_h = ((2 * sx - 1 + 2 * sx) / 2,
                           (left_h + down_h) / 2,
                           (2 * sz + 2 + 2 * sz + 1) / 2)
                pts.append(Point(*mid_p_h))

                if D3:
                    left_h = calculate_height(i, j - 1) + .5
                    down_h = calculate_height(i + 1, j) + .5

                s_down = Point(2 * sx, down_h, 2 * sz + 2)
                s_left = Point(2 * sx - 1, left_h, 2 * sz + 1)
                vertex = Point(2 * dx + 1, y_d, 2 * dz)

                seg_down = LineSegment(vertex, s_down)
                seg_left = LineSegment(vertex, s_left)
                pts.append(seg_down.mid_point())
                pts.append(seg_left.mid_point())

                pts.append(Point(2 * dx + 1, y_d, 2 * dz))
            elif sense == "ldiagonal up":
                pts.append(Point(2 * sx + 1, y_s, 2 * sz))
                pts.append(Point(2 * dx, y_d, 2 * dz + 1))
            elif sense == "rdiagonal down":
                pts.append(Point(2 * sx + 1, y_s, 2 * sz + 1))
                pts.append(Point(2 * dx, y_d, 2 * dz))
            elif sense == "rdiagonal up":
                pts.append(Point(2 * sx, y_d, 2 * sz))
                pts.append(Point(2 * dx + 1, y_d, 2 * dz + 1))
        sz, sx = PATH[-1]
        y_s, y_d = 0.5, 0.5
        if D3:
            y_s = (grid[sz][sx]) / 255 * 10 + .5
        pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))
        pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))

        pts.append(Point(2 * sx + 0.5, y_s, 2 * sz + 0.5))
        CONTROL_PTS = pts
        PATH = False


    if DRAW_PATH:
        pts = CONTROL_PTS
        test = []
        for i in range(0, len(pts)-1, 3):
            test.extend(cubic_bezier(pts[i:i+4]))

        draw_lines(test)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1])
        glTranslatef(*test[MOVE_WORM % len(test)].to_tuple())
        gluQuadricDrawStyle(sph1, GLU_FILL)
        gluQuadricNormals(sph1, GLU_SMOOTH)
        gluQuadricTexture(sph1, GL_TRUE)
        gluSphere(sph1, 0.4, 100, 80)
        x, y, z = test[MOVE_WORM % len(test)].to_tuple()
        glTranslatef(-x, -y, -z)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1])
    glEnable(GL_BLEND)
    glBlendFunc( GL_ONE, GL_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    water_render(y_water)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

    # glDisable(GL_TEXTURE_2D)
    # init_water()

    glPopMatrix()
    glutSwapBuffers()
    glFlush()
    glutSwapBuffers()
    glutPostRedisplay()
    return


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(110, width / height, 3, 100)
    # glOrtho(-100, 10, -100, 10, -100, 10)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    return

def draw_lines(points_list: list[Point]):
    for i in range(1, len(points_list)):
        glBegin(GL_LINES)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
        glVertex3fv(points_list[i-1].to_tuple())
        glVertex3fv(points_list[i].to_tuple())
        glEnd()

def cubic_bezier(points_list: list[Point]):
    polys = ((1, -3, 3, -1), (0, 3, -6, 3), (0, 0, 3, -3), (0, 0, 0, 1))
    assert(len(points_list) == len(polys))
    u = 0
    bezier_curve = []
    while u <= 1:
        res = Point(0, 0, 0)
        for poly, point in zip(polys, points_list):
            res_p = horner(poly, u)
            x = res_p * point.x
            y = res_p * point.y
            z = res_p * point.z
            vec = Vector(Point(x, y, z))
            res = vec.translate(res)
        bezier_curve.append(res)
        u += 0.1
    return bezier_curve


def horner(poly, x):
    n = len(poly)
    res = poly[n - 1]
    i = 0
    for i in range(2, n+1):
        res = res * x + poly[n-i]
    return res

def keyboard(key, x, y):
    global x_pos, y_pos, z_pos, DISPLAY_grid, PATH, D3, MOVE_WORM, NORMALS, DRAW_PATH
    if key == b'g':
        DISPLAY_grid = not DISPLAY_grid
    elif key == b'3':
        D3 = not D3
    elif key == b'p':
        for line in grid:
            print(line)
        print(start, target)
        PATH = dijkstra_matrix_sorted_dict(grid, start, target)
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
    elif key == b'd':
        DRAW_PATH = not DRAW_PATH
    elif key == b'\033':
        # glutDestroyWindow(WIN)
        sys.exit(0)
    # glutPostRedisplay()  # indispensable en Python
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
                    if v != 0 and h != 0 and 0 <= i + v < len(grid) \
                       and 0 <= j + h < len(grid[0]):
                        sum_neigh += grid[i + v][j + h]
                        neighbours += 1
            grid_copy[i][j] = sum_neigh / neighbours

    return grid_copy


def tuckey_smooth(grid: list[list], radius: int):
    grid_copy = deepcopy(grid)
    dep = [x for x in range(-radius, radius + 1)]
    dep = [x for x in range(-radius, radius + 1)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            neigh = []
            for v in dep:
                for h in dep:
                    if 0 <= i + v < len(grid) and 0 <= j + h < len(grid[0]):
                        neigh.append(grid[i + v][j + h])
            neigh.sort()
            n = len(neigh)
            mid = n // 2
            if n % 2 == 0:
                # pair
                grid_copy[i][j] = (neigh[mid] + neigh[mid + 1]) / 2
            else:
                grid_copy[i][j] = neigh[mid]
    return grid_copy


old_grid = None
import copy
def init_random_grid(n):
    global grid, old_grid
    random.seed(1)
    grid = [[random.randint(0, 255) for x in range(n)] for x in range(n)]
    grid = tuckey_smooth(grid, 1)
    old_grid = copy.deepcopy(grid)
    # grid = smooth(grid)
    # rd_line, rd_col = random.randint(0, n - 1), random.randint(0, n - 1)
    # while rd_line != target[0] and rd_line == start[0]:
    #     rd_line, rd_col = random.randint(0, n - 1), random.randint(0, n - 1)
    # for j in range(n):
    #     grid[rd_line][j] = inf
    # grid[rd_line][rd_col] = random.randint(0, 255)
    return

def to_hex_rgb(r, g, b):
        """
        Returns de color in 8bits hexadecimal form in str format
        """
        color = [r,g,b]
        hex_rgb_list = []
        for x in color:
            hex_x = hex(x)[2:]
            if len(hex_x) == 1:
                hex_x = "0" + hex_x
            hex_rgb_list.append(hex_x)
        return "#" + "".join(hex_rgb_list)

dico = {}

def create_grid(canvas, n: int):
    global dico
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x_step = width/n
    y_step = height/n
    for i in range(n):
        for j in range(n):
            #draw of main square
            x_0 = i * x_step
            y_0 = j * y_step
            col = grid[j][i]
            col = int(col)
            str_col = to_hex_rgb(col, col, col)
            dico[(j, i)] = canvas.create_rectangle(x_0, y_0, x_0 + x_step, y_0 + y_step,
                                    fill=str_col, width=2, tags="main")

    canvas.tag_bind("main", sequence="<ButtonRelease-1>", func=select_square)
    canvas.addtag_all("all")


selected = []
path = None
def draw_path(path):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x_step = width/12
    y_step = height/12
    x_small_sq_len = x_step/3
    y_small_sq_len = y_step/3
    for j, i in path:
        x_0 = i * x_step + x_small_sq_len
        y_0 = j * y_step + y_small_sq_len
        canvas.create_rectangle(x_0, y_0, x_0 + x_small_sq_len,
                                               y_0 + y_small_sq_len,
                                        fill="green", width=2, tags="path")

def select_square(event=None):
    global selected, start, target
    n = len(selected)
    if n < 2:
        id_ = canvas.find_withtag("current")[0]
        canvas.itemconfigure(id_, fill="purple")
        canvas.tag_bind(id_, sequence="<ButtonRelease-3>", func=deselect_square)
        for coord, iden in dico.items():
            if iden == id_:
                selected.append(coord)
                break
        if len(selected) == 2:
            start = selected[0]
            target = selected[1]
            path = dijkstra_matrix_sorted_dict(grid, start, target)
            draw_path(path)
            water_lvl.configure(state=tk.DISABLED)

def deselect_square(event=None):
    print("ok")
    id_ = canvas.find_withtag("current")[0]
    canvas.tag_unbind(id_, sequence="<ButtonRelease-3>")
    i = 0 if dico[selected[0]] == id_ else 1
    print(i)
    j, k = selected[i]
    col = int(old_grid[j][k])
    str_col = to_hex_rgb(col, col, col)
    canvas.itemconfigure(id_, fill=str_col)
    selected.pop(i)
    water_lvl.configure(state="readonly")
    canvas.delete("path")
width = 0
height = 0
# def resize(event):
#     global width, height
#     print(event)
#     if width != curr_width or height != curr_height:
#         width = canvas.winfo_width()
#         height = canvas.winfo_height()
#         # rescale all the objects tagged with the "all" tag
#         canvas.delete("all")
#         create_grid(canvas, 12)

def update_grid(*args):
    global selected, y_water
    if len(selected) > 0:
        assert(len(selected)==1)
        id_ = dico[selected[0]]
        canvas.tag_unbind(id_, sequence="<ButtonRelease-3>")
    selected = []
    lvl = int(water_lvl.get())
    y_water = lvl
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            y = calculate_height(j, i)
            print(y, lvl)
            if y <= lvl:
                if len(selected) > 0:
                    if (j,i) != selected[0]:
                        canvas.itemconfig(dico[j,i], fill="cyan")
                        grid[j][i] = inf
                else:
                    canvas.itemconfig(dico[j,i], fill="cyan")
                    grid[j][i] = inf

            else:
                print(grid[i][j])
                print(old_grid[i][j])
                grid[j][i] = old_grid[j][i]
                col = int(grid[j][i])
                str_col = to_hex_rgb(col, col, col)
                canvas.itemconfig(dico[j,i], fill=str_col)
canvas = None
water_lvl = None
def home_window(*args):
    print(*args)
    global canvas, water_lvl
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1024, height=1024)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
    settings = tk.Frame(root, bg="red")
    settings.pack(side=tk.TOP, fill=tk.BOTH)

    phone = tk.StringVar()
    img = tk.PhotoImage(file="red.gif")
    print(img)
    subframe = tk.Frame(settings)
    dijkstra = tk.Radiobutton(subframe, selectimage=img, text="Dijkstra",
                               variable=phone, value="Dijkstra", anchor=tk.W)
    a_star = tk.Radiobutton(subframe, text="A-star", variable=phone,
                            value="A-star", anchor=tk.W)

    subframe2 = tk.Frame(settings)
    phone = tk.StringVar()
    two_d = tk.Radiobutton(subframe2, selectimage=img, text="2D",
                           variable=phone, value="2D", anchor=tk.W)

    three_d = tk.Radiobutton(subframe2, text="3D", variable=phone,
                            value="3D", anchor=tk.W)
    two_d.pack(side=tk.TOP, fill=tk.X, padx=10)
    three_d.pack(side=tk.TOP, fill=tk.X,  padx=10)

    label = tk.Label(settings, text="Water level :")
    label.pack(side=tk.LEFT, fill=tk.BOTH)
    water_lvl = tk.Spinbox(settings, from_=0, to=10, increment=1, width=2,
                           command=update_grid, state="readonly")
    water_lvl.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

    sep = ttk.Separator(settings, orient=tk.VERTICAL)
    sep.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

    dijkstra.pack(side=tk.TOP, fill=tk.X, padx=10)
    a_star.pack(side=tk.TOP, fill=tk.X,  padx=10)
    subframe.pack(side=tk.LEFT, padx=10)
    subframe2.pack(side=tk.LEFT, padx=10)

    sep = ttk.Separator(settings, orient=tk.VERTICAL)
    sep.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

    animate = tk.Button(settings, text="Animate")
    animate.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

    root.update_idletasks()
    # root.bind("<Configure>", resize)
    init_random_grid(12)
    create_grid(canvas, 12)
    return root.mainloop()

if __name__ == "__main__":
    import threading
    # home_window()
    x = threading.Thread(target=home_window)
    x.start()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
    WIN = glutCreateWindow('projet')
    glutReshapeWindow(512, 512)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    # glutMouseFunc(mouse)
    init()
    print(glGetString(GL_VERSION))
    glutMainLoop()
    print("xddddd")
