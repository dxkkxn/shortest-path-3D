#!/usr/bin/env python3
from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from water_rendering import init_water, water_render
from linear_algebra import Vector, Point, LineSegment
import random

inf = float("inf")
class Render3D(object):
    def __init__(self, *args, **kwargs):
        glutInit(*args, **kwargs)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
        glutCreateWindow('projet')
        glutReshapeWindow(1024, 1024)
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        # glutMouseFunc(mouse)
        self.initgl()
        print(glGetString(GL_VERSION))
        self.x_cam, self.y_cam, self.z_cam = 0, 10, 10
        self.sph1 = gluNewQuadric()
        self.display_grid_toggle = False
        self.grid = None
        self.y_water = -1 # height of water
        self.three_d = False
        self.display_normals = False
        self.path = None
        self.display_path = False


    def set_water_heigth(self, x):
        self.y_water = x

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
        init_water()
        glDisable(GL_TEXTURE_2D)
        return

    def display_ground(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                x, z = (j, i)
                y = 0
                if self.three_d:
                    y = self.grid.calculate_height(i, j)

                # main square draw
                glBegin(GL_POLYGON)
                color = self.grid.calculate_color(i, j)

                glNormal3f(0.0, 1.0, 0.0)
                glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                             [color, color, color, 1])
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
                        j_plus1_y = self.grid.calculate_height(i, j + 1)

                    glBegin(GL_POLYGON)
                    color = self.grid.calculate_color(i, j)
                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                                [color, color, color, 1])

                    p0 = Point(2 * x + 1, y, 2 * z)
                    v1 = Vector(p0, Point(2 * x + 2, j_plus1_y, 2 * z))
                    v2 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                    normal = v2 ^ v1

                    glNormal3f(*normal.to_tuple())
                    glVertex3f(2 * x + 1, y, 2 * z)
                    glVertex3f(2 * x + 1, y, 2 * z + 1)
                    color = self.grid.calculate_color(i, j + 1)

                    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                                [color, color, color, 1])
                    glVertex3f(2 * x + 2, j_plus1_y, 2 * z + 1)
                    glVertex3f(2 * x + 2, j_plus1_y, 2 * z)
                    glEnd()

                # draw of vertical rectangles
                if i + 1 < len(self.grid):
                    i_plus1_y = 0
                    if self.three_d:
                        i_plus1_y = self.grid.calculate_height(i + 1, j)
                    glBegin(GL_POLYGON)
                    p0 = Point(2 * x, y, 2 * z + 1)
                    v1 = Vector(p0, Point(2 * x + 1, y, 2 * z + 1))
                    v2 = Vector(p0, Point(2 * x, i_plus1_y, 2 * z + 2))
                    normal = v2 ^ v1
                    glNormal3f(*normal.to_tuple())
                    color = self.grid.calculate_color(i, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                [color, color, color, 1])
                    glVertex3f(2 * x, y, 2 * z + 1)
                    glVertex3f(2 * x + 1, y, 2 * z + 1)
                    color = self.grid.calculate_color(i + 1, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                [color, color, color, 1])
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
                        ij_plus1_y = self.grid.calculate_height(i + 1, j + 1)
                        i_plus1_y = self.grid.calculate_height(i + 1, j)
                        j_plus1_y = self.grid.calculate_height(i, j + 1)

                    glBegin(GL_POLYGON)
                    v0 = Vector(Point(2 * x + 1, y, 2 * z + 1))
                    v1 = Vector(Point(2 * x + 2, ij_plus1_y, 2 * z + 2))
                    v2 = Vector(Point(2 * x + 1, i_plus1_y, 2 * z + 2))
                    v1 = v1 - v0
                    v2 = v2 - v0
                    normal = v2 ^ v1
                    glNormal3f(*normal.to_tuple())
                    color = self.grid.calculate_color(i, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                [color, color, color, 1])
                    glVertex3f(2 * x + 1, y, 2 * z + 1)

                    color = self.grid.calculate_color(i + 1, j)

                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                [color, color, color, 1])
                    glVertex3f(2 * x + 1, i_plus1_y, 2 * z + 2)

                    color = self.grid.calculate_color(i + 1, j + 1)

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
                    color = self.grid.calculate_color(i, j)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                                 [color, color, color, 1])
                    glVertex3f(2 * x + 1, y, 2 * z + 1)

                    color = self.grid.calculate_color(i, j + 1)
                    glMaterialfv(
                        GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [
                            color, color, color, 1])
                    glVertex3f(2 * x + 2, j_plus1_y, 2 * z + 1)

                    color = self.grid.calculate_color(i + 1, j + 1)
                    glMaterialfv(
                        GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [
                            color, color, color, 1])
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
        # draw of bottom box for more beautiful display
        self.draw_box()

    def draw_triangles(self, vertices):
        glBegin(GL_TRIANGLES)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1])
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
                y = self.grid.calculate_height(i, 0)
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
                y = self.grid.calculate_height(z, x)
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
                y = self.grid.calculate_height(z, x)
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
                y = self.grid.calculate_height(z, x)
            pts.append((2 * x, y, 2 * z))
            pts.append((2 * x + 1, y, 2 * z))
        pts.append((2 * (n - 1) + 1, -2, 0))
        self.draw_triangles(self.triangulate(pts))


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        gluLookAt(self.x_cam, self.y_cam, self.z_cam,  # pos camera
                  self.x_cam, -10 + self.y_cam, -10 + self.z_cam,  # look at
                  0, 1, 0)  # up vector

        if self.display_grid_toggle:
            self.display_grid()
        glClearColor(0.0, 0.0, 0.0, 0.0)

        if self.grid:
            self.display_ground()
            if self.display_normals:
                draw_normals()
            if self.path:
                pts = []
                sz, sx = PATH[0]
                y_s, y_d = 0.5, 0.5
                if self.three_d:
                    y_s = (self.grid[sz][sx]) / 255 * 10 + .5
                pts.append(Point(2 * sx + 0.5, y_s, 2 * sz + 0.5))
                point_prec = Point(2 * sx + 0.5, y_s, 2 * sz + 0.5)
                for i in range(1, len(PATH)):
                    sz, sx = PATH[i - 1]
                    dz, dx = PATH[i]
                    sense = self.grid.calculate_sense(PATH[i - 1], PATH[i])
                    print(sense)
                    y_s, y_d = 0.5, 0.5
                    if self.three_d:
                        y_s = (self.grid[sz][sx]) / 255 * 10 + .5
                        y_d = (self.grid[dz][dx]) / 255 * 10 + .5
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
                        if self.three_d:
                            left_h = self.grid.calculate_height(i, j - 1) + .5
                            print(i+1, j)
                            down_h = self.grid.calculate_height(i + 1, j) + .5

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

                        if self.three_d:
                            left_h = self.grid.calculate_height(i, j - 1) + .5
                            down_h = self.grid.calculate_height(i + 1, j) + .5

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
                if self.three_d:
                    y_s = (self.grid[sz][sx]) / 255 * 10 + .5
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))
                pts.append(random_point(Point(2 * sx, y_s, 2 * sz)))

                pts.append(Point(2 * sx + 0.5, y_s, 2 * sz + 0.5))
                CONTROL_PTS = pts
                PATH = False

            if self.display_path:
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
            water_render(2*len(self.grid), self.y_water)
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


    def set_grid(self, grid):
        """Sets the grid"""
        self.grid = grid
    def set_path(self, path):
        """Sets the grid"""
        self.grid = path

    def keyboard(self, key, x, y):
        """Control keyboards inputs."""
        if key == b'g':
            self.display_grid_toggle = not self.display_grid_toggle
        elif key == b'3':
            self.three_d = not self.three_d
        elif key == b'w':
            self.y_cam -= 1
        elif key == b's':
            self.y_cam += 1
        elif key == b'j':
            self.z_cam += 1
        elif key == b'k':
            self.z_cam -= 1
        elif key == b'h':
            self.x_cam -= 1
        elif key == b'l':
            self.x_cam += 1
        elif key == b'm':
            MOVE_WORM += 1
        elif key == b'n':
            self.display_normals = not self.display_normals
        elif key == b'd':
            self.display_path = not self.display_path
        elif key == b'\033':
            glutDestroyWindow(WIN)
            sys.exit(0)
        glutPostRedisplay()  # indispensable en Python
        return

    def rescale_normal(nv: Vector, norm: int):
        """Renvoie le vector nv a echelle i.e pour que il aie une norme norm."""
        scale = sqrt(norm / (nv.x**2 + nv.y**2 + nv.z**2))
        return Vector(Point(scale * nv.x, scale * nv.y, scale * nv.z))

    def draw_normals(self):
        """Affichage des normals."""
        sph1 = gluNewQuadric()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x, z = (j, i)
                y = 0
                if self.three_d:
                    y = self.grid.calculate_height(i, j)
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
                    if self.three_d:
                        j_plus1_y = self.grid.calculate_height(i, j + 1)

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
                    if self.three_d:
                        i_plus1_y = self.grid.calculate_height(i + 1, j)
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
                    if self.three_d:
                        ij_plus1_y = self.grid.calculate_height(i + 1, j + 1)
                        i_plus1_y = self.grid.calculate_height(i + 1, j)
                        j_plus1_y = self.grid.calculate_height(i, j + 1)

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


class Grid(object):
    def __init__(self, size: int, seed: int):
        random.seed(seed)
        self.grid = [[random.randint(0, 255) for x in range(size)]
                     for x in range(size)]
        # self.grid = tuckey_smooth(grid, 1)
        # self.old_grid = copy.deepcopy(grid)

    def __getitem__(self, key: tuple):
        assert(isinstance(key, tuple) and  len(key) == 2)
        i, j = key
        return self.grid[i][j]


    def __len__(self):
        """Return the lenght of grid."""
        return len(self.grid)

    def calculate_color(self, i, j):
        """Calcul du color selon la coordonnee (i,j)."""
        color = self.old_grid[i][j] / 255
        if color == inf:
            color = .0
        return color

    def calculate_height(self, i, j):
        """Calcul du hauteur selon la coordonnee (i,j)."""
        y = self.old_grid[i][j] / 255 * 10
        if y == inf:
            y = 0
        return y


    def calculate_sense(self, p1, p2):
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

    def tuckey_smooth(self, radius: int):
        grid_copy = copy.deepcopy(self.grid)
        dep = [x for x in range(-radius, radius + 1)]
        length = len(self.grid)
        for i in range(length):
            for j in range(length):
                neigh = []
                for v in dep:
                    for h in dep:
                        if 0 <= i + v < length and 0 <= j + h < length:
                            neigh.append(self[i + v, j + h])
                neigh.sort()
                n = len(neigh)
                mid = n // 2
                if n % 2 == 0:
                    # pair
                    grid_copy[i] [j] = (neigh[mid] + neigh[mid + 1]) / 2
                else:
                    grid_copy[i][j] = neigh[mid]
        self.grid = grid_copy
        self.old_grid = copy.deepcopy(self.grid)

    def smooth(grid):
        grid_copy = copy.deepcopy(grid)
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


if __name__ == "__main__":
    import copy


    app3D = Render3D(sys.argv)
    grid_ = Grid(12, 1)
    grid_.tuckey_smooth(1)
    app3D.set_grid(grid_)
    app3D.mainloop()
