#!/usr/bin/env python3
#
from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from water_rendering import Water
from linear_algebra import Vector, Point, mid_point, barycenter
from dijkstra import dijkstra_matrix_sorted_dict
from bezier import cubic_bezier
from math import cos, sin
from grid import Grid
from snake import Snake
import random


class Render3D(object):
    """OpenGL application."""

    def __init__(self, grid, water_res=34, *args, **kwargs):
        """Initialise a glut window."""
        glutInit(*args, **kwargs)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
        glutCreateWindow('projet')
        glutReshapeWindow(1024, 1024)
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)

        self.initgl()
        self.x_cam, self.y_cam, self.z_cam = 0, 10, 10
        self.sph1 = gluNewQuadric()
        self.display_grid_toggle = False
        self.grid = None
        self.three_d = True
        self.display_normals = False
        self.path = None
        self.path3D = None
        self.display_path = False
        self.animation = False
        self.x_look_at, self.y_look_at, self.z_look_at = 0, 0, 0

        self.grid = grid
        x = len(grid)
        self.water = Water(resolution=water_res, size=len(grid) * 2)
        self.x_look_at = x
        self.z_look_at = x
        self.stop = False

    def set_grid(self, grid):
        """Update the grid."""
        self.grid = grid
        x = len(grid)
        self.water.set_size(len(grid)*2)
        self.x_look_at = x
        self.z_look_at = x

    def set_water_height(self, x):
        self.water.y = x

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(110, width / height, 3, 100)
        # glOrtho(-100, 10, -100, 10, -100, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        return

    def mainloop(self):
        glutMainLoop()

    def initgl(self):
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
        glDisable(GL_TEXTURE_2D)
        return

    def display_ground(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                x, z = (j, i)
                y = 0
                if self.three_d:
                    y = self.grid.height(i, j)

                # main square draw
                glBegin(GL_POLYGON)
                color = self.grid.color_std(i, j)

                glNormal3f(0.0, 1.0, 0.0)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)
                glVertex3f(2 * x, y, 2 * z)
                glVertex3f(2 * x + 1, y, 2 * z)
                glVertex3f(2 * x + 1, y, 2 * z + 1)
                glVertex3f(2 * x, y, 2 * z + 1)
                glEnd()

                # draw of horizontal rectangles
                if j + 1 < len(self.grid):
                    i_plus1_y = 0
                    j_plus1_y = 0
                    if self.three_d:
                        j_plus1_y = self.grid.height(i, j + 1)

                    glBegin(GL_POLYGON)
                    color = self.grid.color_std(i, j)
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

                    p0 = Point(2 * x + 1, y, 2 * z)
                    v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z))
                    v2 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                    normal = v2 ^ v1
                    normal.rescale(1)

                    glNormal3f(*normal.to_tuple())
                    glVertex3f(2 * x + 1, y, 2 * z)
                    glVertex3f(2 * x + 1, y, 2 * z + 1)
                    color = self.grid.color_std(i, j + 1)

                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)
                                # [color, color, color, 0])
                    glVertex3f(2 * x + 2, j_plus1_y, 2 * z + 1)
                    glVertex3f(2 * x + 2, j_plus1_y, 2 * z)
                    glEnd()

                # draw of vertical rectangles
                if i + 1 < len(self.grid):
                    i_plus1_y = 0
                    if self.three_d:
                        i_plus1_y = self.grid.height(i + 1, j)
                    glBegin(GL_POLYGON)
                    p0 = Point(2 * x, y, 2 * z + 1)
                    v1 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                    v2 = Vector(p0, Point(2 * x, i_plus1_y, 2 * z + 2))
                    normal = v2 ^ v1
                    normal.rescale(1)
                    glNormal3f(*normal.to_tuple())
                    color = self.grid.color_std(i, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                                # [color, color, color, 0])
                    glVertex3f(2 * x, y, 2 * z + 1)
                    glVertex3f(2 * x + 1, y, 2 * z + 1)
                    color = self.grid.color_std(i + 1, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                                #[color, color, color, 0])
                    glVertex3f(2 * x + 1, i_plus1_y, 2 * z + 2)
                    glVertex3f(2 * x, i_plus1_y, 2 * z + 2)
                    glNormal3f(0, 1, 0)
                    glEnd()
                # draw of inner triangles
                if i + 1 < len(self.grid) and j + 1 < len(self.grid):
                    ij_plus1_y = 0
                    i_plus1_y = 0
                    j_plus1_y = 0
                    if self.three_d:
                        ij_plus1_y = self.grid.height(i + 1, j + 1)
                        i_plus1_y = self.grid.height(i + 1, j)
                        j_plus1_y = self.grid.height(i, j + 1)

                    glBegin(GL_POLYGON)
                    v0 = Vector(Point(2 * x + 1, y, 2 * z + 1))
                    v1 = Vector(Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                    v2 = Vector(Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                    v1 = v1 - v0
                    v2 = v2 - v0
                    normal = v2 ^ v1
                    normal.rescale(1)
                    glNormal3f(*normal.to_tuple())
                    color = self.grid.color_std(i, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                                #[color, color, color, 0])
                    glVertex3f(2 * x + 1, y, 2 * z + 1)

                    color = self.grid.color_std(i + 1, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                                # [color, color, color, 0])
                    glVertex3f(2 * x + 1, i_plus1_y, 2 * z + 2)

                    color = self.grid.color_std(i + 1, j + 1)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                                # [color, color, color, 0])
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
                    normal.rescale(1)
                    glNormal3f(*normal.to_tuple())
                    color = self.grid.color_std(i, j)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                                 # [color, color, color, 0])
                    glVertex3f(2 * x + 1, y, 2 * z + 1)

                    color = self.grid.color_std(i, j + 1)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                        #[color, color, color, 0])
                    glVertex3f(2 * x + 2, j_plus1_y, 2 * z + 1)

                    color = self.grid.color_std(i + 1, j + 1)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 color)
                    # [
                    #         color, color, color, 0])
                    glVertex3f(2 * x + 2, ij_plus1_y, 2 * z + 2)
                    glEnd()

            self.draw_box()

    @staticmethod
    def triangulate(polygon):
        """
        Return a list of triangles.

        Uses the GLU Tesselator functions!
        code from
        https://stackoverflow.com/questions/38640395/pyopengl-tessellating-polygons
        Adapted by us for 3D points and polygones without holes.
        """
        vertices = []
        def edgeFlagCallback(param1, param2): pass
        def beginCallback(param=None):
            vertices = []
        def vertexCallback(vertex, otherData=None):
            vertices.append(vertex)
        def combineCallback(vertex, neighbors, neighborWeights, out=None):
            out = vertex
            return out
        def endCallback(data=None): pass

        tess = gluNewTess()
        gluTessProperty(tess, GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD)
        gluTessCallback(tess, GLU_TESS_EDGE_FLAG_DATA, edgeFlagCallback)#forces triangulation of polygons (i.e. GL_TRIANGLES) rather than returning triangle fans or strips
        gluTessCallback(tess, GLU_TESS_BEGIN, beginCallback)
        gluTessCallback(tess, GLU_TESS_VERTEX, vertexCallback)
        gluTessCallback(tess, GLU_TESS_COMBINE, combineCallback)
        gluTessCallback(tess, GLU_TESS_END, endCallback)
        gluTessBeginPolygon(tess, 0)

        #first handle the main polygon
        gluTessBeginContour(tess)
        for point in polygon:
            gluTessVertex(tess, point, point)
        gluTessEndContour(tess)
        gluTessEndPolygon(tess)
        gluDeleteTess(tess)
        return vertices

    def draw_triangles(self, vertices):
        """Draw triangles."""
        glBegin(GL_TRIANGLES)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0, 0, 0))
        glColor(1, 0, 0)
        for vertex in vertices:
            glVertex(*vertex)
        glEnd()

    def draw_box(self):
        """
        Draws a box.

        Draws around the edges for a prettier visualization.
        """
        # left barrier
        n = len(self.grid)
        pts = []
        pts.append((0, -2, 0))
        for i in range(n):
            z = i
            y = 0
            if self.three_d:
                y = self.grid.height(i, 0)
            pts.append((0, y, 2 * z))
            pts.append((0, y, 2 * z + 1))
        pts.append((0, -2, 2 * (n - 1) + 1))
        self.draw_triangles(self.triangulate(pts))

        # right barrier
        pts = []
        pts.append((2 * (n - 1) + 1, -2, 0))
        for i in range(n):
            x = n - 1
            z = i
            y = 0
            if self.three_d:
                y = self.grid.height(z, x)
            pts.append((2 * x + 1, y, 2 * z))
            pts.append((2 * x + 1, y, 2 * z + 1))
        pts.append((2 * (n - 1) + 1, -2, 2 * (n - 1) + 1))
        self.draw_triangles(self.triangulate(pts))

        # front barrier
        pts = []
        pts.append((0, -2, 2 * (n - 1) + 1))
        for i in range(n):
            x = i
            z = n - 1
            y = 0
            if self.three_d:
                y = self.grid.height(z, x)
            p1 = (2 * x, y, 2 * z + 1)
            p2 = (2 * x + 1, y, 2 * z + 1)
            pts.append(p1)
            pts.append(p2)
        pts.append((2 * (n - 1) + 1, -2, 2 * (n - 1) + 1))
        self.draw_triangles(self.triangulate(pts))

        # back barrier
        pts = []
        pts.append((0, -2, 0))
        for i in range(len(self.grid)):
            x = i
            z = 0
            y = 0
            if self.three_d:
                y = self.grid.height(z, x)
            pts.append((2 * x, y, 2 * z))
            pts.append((2 * x + 1, y, 2 * z))
        pts.append((2 * (n - 1) + 1, -2, 0))
        self.draw_triangles(self.triangulate(pts))


    def redisplay(self):
        glutPostRedisplay()

    def compute_path_3D(self):
        """Compute the 3D path using bezier."""
        self.path3D = []
        sz, sx = self.path[0]
        y_s, y_d = 0.5, 0.5
        if self.three_d:
            y_s = (self.grid[sz, sx]) / 255 * 10 + .5
        self.path3D.append(Point(2 * sx + 0.5, y_s, 2 * sz + 0.5))
        for i in range(1, len(self.path)):
            sz, sx = self.path[i - 1]
            dz, dx = self.path[i]
            sense = self.grid.calculate_sense(self.path[i - 1], self.path[i])

            y_s, y_d = 0.5, 0.5
            if self.three_d:
                y_s = (self.grid[sz, sx]) / 255 * 10 + .5
                y_d = (self.grid[dz, dx]) / 255 * 10 + .5

            # deux point aleatoires sur le carre courant pricipal
            self.path3D.append(self.random_point(Point(2 * sx, y_s,
                                                        2 * sz)))
            self.path3D.append(self.random_point(Point(2 * sx, y_s,
                                                        2 * sz)))
            if sense == "horizontal left":
                self.path3D.append(Point(2 * sx, y_s, 2 * sz + 0.5))

                mid_sup = mid_point(Point(2 * sx, y_s, 2 * sz),
                                    Point(2 * dx + 1, y_d, 2 * dz))
                mid_inf = mid_point(Point(2 * sx + 1, y_s, 2 * sz + 1),
                                    Point(2 * dx, y_d, 2 * dz + 1))
                self.path3D.append(mid_sup)
                self.path3D.append(mid_inf)

                self.path3D.append(Point(2 * dx + 1, y_d, 2 * dz + 0.5))

            elif sense == "horizontal right":

                # s -> d
                # s_up   d_up
                # s_mid  d_mid
                # s_down d_down

                s_up = Point(2 * sx + 1, y_s, 2 * sz)
                s_mid = Point(2 * sx + 1, y_s, 2 * sz + 0.5)
                s_down = Point(2 * sx + 1, y_s, 2 * sz + 1)
                d_up = Point(2 * dx, y_d, 2 * dz)
                d_mid = Point(2 * dx, y_d, 2 * dz + 0.5)
                d_down = Point(2 * dx, y_d, 2 * dz + 1)
                self.path3D.append(s_mid)

                self.path3D.append(mid_point(s_up, d_up))
                self.path3D.append(mid_point(s_down, d_down))

                self.path3D.append(d_mid)

            elif sense == "vertical down":
                self.path3D.append(Point(2 * sx + 0.5, y_s, 2 * sz + 1))

                mid_sup = mid_point(Point(2 * sx, y_s, 2 * sz + 1),
                                    Point(2 * dx, y_d, 2 * dz))

                mid_inf = mid_point(Point(2 * sx + 1, y_s, 2 * sz + 1),
                                    Point(2 * dx + 1, y_d, 2 * dz))

                self.path3D.append(mid_sup)
                self.path3D.append(mid_inf)

                self.path3D.append(Point(2 * dx + 0.5, y_d, 2 * dz))
            elif sense == "vertical up":
                # s -> d
                # d_left d_mid d_right
                # s_left s_mid s_right
                s_left = Point(2 * sx, y_s, 2 * sz)
                s_mid = Point(2 * sx + .5, y_s, 2 * sz)
                s_right = Point(2 * sx + 1, y_s, 2 * sz)

                d_left = Point(2 * dx, y_d, 2 * dz + 1)
                d_mid = Point(2 * dx + .5, y_d, 2 * dz + 1)
                d_right = Point(2 * dx + 1, y_d, 2 * dz + 1)

                self.path3D.append(s_mid)
                self.path3D.append(mid_point(s_left, d_left))
                self.path3D.append(mid_point(s_right, d_right))
                self.path3D.append(d_mid)
            elif sense == "ldiagonal down":
                i, j = self.path[i - 1]
                left_h = 0.5
                down_h = 0.5
                self.path3D.append(Point(2 * sx, y_s, 2 * sz + 1))
                if self.three_d:
                    left_h = self.grid.height(i, j - 1) + .5
                    down_h = self.grid.height(i + 1, j) + .5

                s_down = Point(2 * sx, down_h, 2 * sz + 2)
                s_left = Point(2 * sx - 1, left_h, 2 * sz + 1)
                vertex = Point(2 * sx, y_s, 2 * sz + 1)

                self.path3D.append(mid_point(vertex, s_down))
                self.path3D.append(mid_point(vertex, s_left))

                mid_p_h = ((2 * sx - 1 + 2 * sx) / 2,
                            (left_h + down_h) / 2,
                            (2 * sz + 2 + 2 * sz + 1) / 2)
                self.path3D.append(Point(*mid_p_h))

                if self.three_d:
                    left_h = self.grid.height(i, j - 1) + .5
                    down_h = self.grid.height(i + 1, j) + .5

                s_down = Point(2 * sx, down_h, 2 * sz + 2)
                s_left = Point(2 * sx - 1, left_h, 2 * sz + 1)
                vertex = Point(2 * dx + 1, y_d, 2 * dz)

                self.path3D.append(mid_point(vertex, s_down))
                self.path3D.append(mid_point(vertex, s_left))

                self.path3D.append(Point(2 * dx + 1, y_d, 2 * dz))
            elif sense == "ldiagonal up":
                # s -> diag_mid -> d
                # s_up        d
                # s    s_right

                s = Point(2 * sx + 1, y_s, 2 * sz)
                d = Point(2 * dx, y_d, 2 * dz + 1)

                s_up_y = .5
                s_right_y = .5
                if self.three_d:
                    i, j = self.path[i-1]
                    s_up_y = self.grid.height(i - 1, j) + .5
                    s_right_y = self.grid.height(i, j + 1) + .5

                s_up = Point(2 * sx + 1, s_up_y, 2 * sz - 1)
                s_right = Point(2 * sx + 2, s_right_y, 2 * sz)

                self.path3D.append(s)
                self.path3D.append(mid_point(s, s_up))
                self.path3D.append(mid_point(s, s_right))

                diag_mid = ((2 * sx + 1 + 2 * sx + 2) / 2,
                            (s_up_y + s_right_y) / 2,
                            (2 * sz - 1 + 2 * sz ) / 2)
                self.path3D.append(Point(*diag_mid))

                self.path3D.append(mid_point(d, s_up))
                self.path3D.append(mid_point(d, s_right))
                self.path3D.append(d)

            elif sense == "rdiagonal down":
                s = Point(2 * sx + 1, y_s, 2 * sz + 1)
                d = Point(2 * dx, y_d, 2 * dz)
                mid_p = mid_point(s, d)

                self.path3D.append(s)
                self.path3D.append(mid_p)
                self.path3D.append(mid_p)
                self.path3D.append(d)
            elif sense == "rdiagonal up":
                self.path3D.append(Point(2 * sx, y_s, 2 * sz))
                mid_p = mid_point(Point(2 * sx + 1, y_s, 2 * sz + 1),
                                  Point(2 * dx, y_d, 2 * dz))

                self.path3D.append(mid_p)
                self.path3D.append(mid_p)
                self.path3D.append(Point(2 * dx + 1, y_d, 2 * dz + 1))
        sz, sx = self.path[-1]
        y_s, y_d = 0.5, 0.5
        if self.three_d:
            y_s = (self.grid[sz, sx]) / 255 * 10 + .5

        self.path3D.append(self.random_point(Point(2 * sx, y_s,
                                                    2 * sz)))
        self.path3D.append(self.random_point(Point(2 * sx, y_s,
                                                    2 * sz)))

        self.path3D.append(Point(2 * sx + 0.5, y_s, 2 * sz + 0.5))
        tmp = []
        for i in range(0, len(self.path3D)-1, 3):
            tmp.extend(cubic_bezier(self.path3D[i:i+4]))
        self.path3D = tmp

    @staticmethod
    def draw_lines(points_list: list[Point]):
        """Draw lines between points in points_list."""
        for i in range(1, len(points_list)):
            glBegin(GL_LINES)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
            glVertex3fv(points_list[i-1].to_tuple())
            glVertex3fv(points_list[i].to_tuple())
            glEnd()

    @staticmethod
    def random_point(point: Point):
        """
        Return a random  point in a selection.

        Returns a point in the square made by point with 1 length.
        Returned point is not totally random is one of :
        .__.__.
        |     |
        .     .
        |     |
        .__.__.
        """
        x, y, z = point.to_tuple()
        points = [point, Point(x + .5, y, z), Point(x + 1, y, z),
                  Point(x, y, z + .5), Point(x + .5, y, z + .5),
                  Point(x, y, z + 1), Point(x + .5, y, z + 1),
                  Point(x + 1, y, z + 1)]
        return random.choice(points)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        gluLookAt(self.x_cam, self.y_cam, self.z_cam,  # pos camera
                  self.x_look_at, self.y_look_at, self.z_look_at,  # look at
                  0, 1, 0)  # up vector

        if self.display_grid_toggle:
            self.display_grid()
        glClearColor(0.0, 0.0, 0.0, 0.0)

        if self.grid:
            self.display_ground()

            if self.display_normals:
                self.draw_normals()

            if self.display_path:
                if self.path3D:
                    self.draw_lines(self.path3D)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                [0, 1, 0, 1])
                else:
                    print("Please set the path before")
            if self.animation:
                gluQuadricDrawStyle(self.sph1, GLU_FILL)
                gluQuadricNormals(self.sph1, GLU_SMOOTH)
                gluQuadricTexture(self.sph1, GL_TRUE)
                n = len(self.path3D)
                self.snake.move(self.path3D[self.move_worm % n])
                for pos in self.snake.get_positions():
                    x, y, z = pos.to_tuple()
                    glTranslatef(x, y, z)
                    gluSphere(self.sph1, 0.5, 100, 80)
                    glTranslatef(-x, -y, -z)

            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                         [1, 1, 1, 1])
            glEnable(GL_BLEND)
            glBlendFunc(GL_ONE, GL_SRC_ALPHA)
            glEnable(GL_TEXTURE_2D)
            self.water.render()
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

        glPopMatrix()
        glutSwapBuffers()
        glFlush()
        glutSwapBuffers()
        if self.stop is False:
            glutPostRedisplay()
        return

    def keyboard(self, key, x, y):
        """Control keyboards inputs."""
        if key == b'h':
            x, z = self.x_cam - self.x_look_at, self.z_cam - self.z_look_at
            self.x_cam = x * cos(0.1) - z * sin(0.1)
            self.z_cam = z * cos(0.1) + x * sin(0.1)

            self.x_cam += self.x_look_at
            self.z_cam += self.z_look_at
        elif key == b'l':
            x, z = self.x_cam - self.x_look_at, self.z_cam - self.z_look_at
            self.x_cam = x * cos(-0.1) - z * sin(-0.1)
            self.z_cam = z * cos(-0.1) + x * sin(-0.1)

            self.x_cam += self.x_look_at
            self.z_cam += self.z_look_at
        elif key == b'j':
            self.y_cam -= 1
        elif key == b'k':
            self.y_cam += 1
        if key == b'g':
            self.display_grid_toggle = not self.display_grid_toggle
        elif key == b'3':
            self.three_d = not self.three_d
        elif key == b'n':
            self.display_normals = not self.display_normals
            self.water.set_normals(self.display_normals)
        elif key == b'd':
            self.display_path = not self.display_path
        elif key == b'u':
            self.compute_path_3D()
        elif key == b'a':
            # a -animate
            if self.animation:
                print("Animation already in progress")
                return

            if not self.path3D:
                print("No known path")
                return
            self.animation = True
            self.move_worm = 0
            n = len(self.path3D)
            x, y, z = self.path3D[self.move_worm % n].to_tuple()
            self.x_look_at = x
            self.y_look_at = y
            self.z_look_at = z
            self.x_cam, self.y_cam, self.z_cam = x, y + 4, z - 4
            for i in range(len(self.path3D)):
                glutTimerFunc(1000+(i*100), self.animate, None)

        elif key == b'\033':
            glutDestroyWindow(WIN)
            sys.exit(0)
        glutPostRedisplay()  # indispensable en Python
        return

    def start_animation(self):
        if self.animation:
            print("Animation already in progress")
            return
        if not self.path3D:
            print("No known path")
            return
        self.animation = True
        self.move_worm = 0
        n = len(self.path3D)
        x, y, z = self.path3D[self.move_worm % n].to_tuple()
        self.x_look_at = x
        self.y_look_at = y
        self.z_look_at = z
        self.x_cam, self.y_cam, self.z_cam = x, y + 4, z - 4
        for i in range(len(self.path3D)):
            glutTimerFunc(1000+(i*100), self.animate, None)

    def animate(self, event):
        """Start the animation."""
        n = len(self.path3D)
        x, y, z = self.path3D[self.move_worm % n].to_tuple()
        old_x, old_y, old_z = self.x_look_at, self.y_look_at, self.z_look_at
        self.x_look_at, self.y_look_at, self.z_look_at = x, y, z

        move_x, move_y, move_z = x - old_x, y - old_y, z - old_z
        self.x_cam += move_x
        self.y_cam += move_y
        self.z_cam += move_z
        if self.move_worm == n - 1:
            # set look at center point of the model
            self.x_look_at = len(self.grid)
            self.z_look_at = len(self.grid)
            self.animation = False
        self.move_worm += 1

    def draw_normals(self):
        """Affichage des normals."""
        self.sph1 = gluNewQuadric()
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                x, z = (j, i)
                y = 0
                if self.three_d:
                    y = self.grid.height(i, j)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                # draw of main squares
                # centre of de square
                cx, cy, cz = (2 * x + .5, y, 2 * z + .5)
                glTranslatef(cx, cy, cz)
                gluSphere(self.sph1, 0.1, 5, 5)
                glTranslatef(-cx, -cy, -cz)

                glBegin(GL_LINES)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
                normal = Vector(Point(0, 1, 0))
                glVertex(cx, cy, cz)
                normal.rescale(0.1)
                glVertex3fv(normal.translate(Point(cx, cy, cz)).to_tuple())
                glEnd()
                # horizontal rectangles
                j_plus1_y = 0
                if j + 1 < len(self.grid):
                    if self.three_d:
                        j_plus1_y = self.grid.height(i, j + 1)

                    p0 = Point(2 * x + 1, y, 2 * z)
                    v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z))
                    v2 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                    normal = v2 ^ v1

                    a = Point(2 * x + 1, y, 2 * z)
                    b = Point(2 * x + 2, j_plus1_y, 2 * z + 1)
                    # center of the rectangle
                    cx, cy, cz = mid_point(a, b).to_tuple()
                    glTranslatef(cx, cy, cz)
                    gluSphere(self.sph1, 0.1, 5, 5)
                    glTranslatef(-cx, -cy, -cz)

                    glBegin(GL_LINES)
                    glNormal3f(0, 1, 0)
                    glVertex3f(cx, cy, cz)
                    normal.rescale(0.5)
                    glVertex3fv(normal.translate(Point(cx, cy, cz)).to_tuple())
                    glEnd()

                if i + 1 < len(self.grid):
                    i_plus1_y = 0
                    if self.three_d:
                        i_plus1_y = self.grid.height(i + 1, j)
                    # vertical rectangles
                    p0 = Point(2 * x, y, 2 * z + 1)
                    v1 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                    v2 = Vector(p0, Point(2 * x, i_plus1_y, 2 * z + 2))
                    normal = v2 ^ v1
                    a = Point(2 * x, y, 2 * z + 1)
                    b = Point(2 * x + 1, i_plus1_y, 2 * z + 2)
                    # centre du rectangle
                    cx, cy, cz = mid_point(a, b).to_tuple()
                    glTranslatef(cx, cy, cz)
                    gluSphere(self.sph1, 0.1, 5, 5)
                    glTranslatef(-cx, -cy, -cz)

                    glBegin(GL_LINES)
                    glVertex3f(cx, cy, cz)
                    normal.rescale(0.5)
                    glVertex3fv(normal.translate(Point(cx, cy, cz)).to_tuple())
                    glEnd()

                # inner triagle
                if i + 1 < len(self.grid) and j + 1 < len(self.grid):
                    ij_plus1_y = 0
                    i_plus1_y = 0
                    j_plus1_y = 0
                    if self.three_d:
                        ij_plus1_y = self.grid.height(i + 1, j + 1)
                        i_plus1_y = self.grid.height(i + 1, j)
                        j_plus1_y = self.grid.height(i, j + 1)

                    p0 = (Point(2 * x + 1, y, 2 * z + 1))
                    v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z + 1))
                    v2 = Vector(p0, Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                    normal = v2 ^ v1

                    bc = barycenter(Point(2 * x + 1, y, 2 * z + 1),
                                                        Point(2 * x + 2, j_plus1_y, 2 * z + 1),
                                                        Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                    bx, by, bz = (bc.to_tuple())
                    glTranslatef(bx, by, bz)
                    gluSphere(self.sph1, 0.1, 5, 5)
                    glTranslatef(-bx, -by, -bz)

                    glBegin(GL_LINES)
                    normal.rescale(.5)
                    glVertex3f(bx, by, bz)
                    glVertex3fv(normal.translate(bc).to_tuple())
                    glEnd()

                    bc = barycenter(Point(2 * x + 1, y, 2 * z + 1),
                                                        Point(2 * x + 2, ij_plus1_y, 2 * z + 2),
                                                        Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                    p0 = Point(2 * x + 1, y, 2 * z + 1)
                    v1 = Vector(p0, Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                    v2 = Vector(p0, Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                    normal = v2 ^ v1
                    bx, by, bz = (bc.to_tuple())
                    glTranslatef(bx, by, bz)
                    gluSphere(self.sph1, 0.1, 5, 5)
                    glTranslatef(-bx, -by, -bz)

                    glBegin(GL_LINES)
                    glMaterialfv(
                        GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [
                            1, 0, 0, 1])
                    normal.rescale(.5)
                    glVertex3f(bx, by, bz)
                    glVertex3fv(normal.translate(Point(bx, by, bz)).to_tuple())
                    glEnd()

    def display_grid(self):
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

    def set_path(self, path):
        self.path = path
        self.compute_path_3D()
        initial_pos = self.path3D[0]
        self.snake = Snake(5, initial_pos)



if __name__ == "__main__":
    app3D = Render3D(sys.argv)
    grid_ = Grid(12, 1)
    grid_.tuckey_smooth(1)
    app3D.set_grid(grid_)
    path = dijkstra_matrix_sorted_dict(grid_.grid, (0, 11), (11, 0))
    app3D.set_path(path)
    app3D.mainloop()
