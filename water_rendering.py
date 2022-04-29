"""
Demonstration of water rendering.

Copyright (C) 2005  Julien Guertault

Python conversion
Site de l'auteur original : http://www.lousodrome.net/opengl/
"""

from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from math import sqrt, sin

from water_noise import init_noise, noise

# RESOLUTION = 64
RESOLUTION = 34

texture = 0

left_click = GLUT_UP
right_click = GLUT_UP
wire_frame = False
normals = 0
xold = 0
yold = 0
rotate_x = 30
rotate_y = 15
translate_z = 4

surface = [0 for i in range(6 * RESOLUTION * (RESOLUTION + 1))]
normal = [0 for i in range(6 * RESOLUTION * (RESOLUTION + 1))]
display_grid_toggle = False


def z(x, y, t):
    """Calculate z cooord? ."""
    x2 = x - 3
    y2 = y + 1
    xx = x2 * x2
    yy = y2 * y2
    return (2 * sin(20 * sqrt(xx + yy) - 4 * t)
            + noise(10 * x, 10 * y, t, 0)) / 200


def load_texture(filename):
    """Load a jpeg file."""
    image = Image.open(filename)  # retourne une PIL.image
    return image.tobytes()  # TODO: distinguer les cas (RGB, L, ...)


x_pos, y_pos, z_pos = 0, 10, 10

def water_render(n):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.
    delta = 39 / RESOLUTION
    length = 2 * (RESOLUTION + 1)
    xn = (RESOLUTION + 1) * delta + 1
    for j in range(RESOLUTION):
        y = (j + 1) * delta - 1
        for i in range(RESOLUTION + 1):
            indice = 6 * (i + j * (RESOLUTION + 1))
            x = i * delta - 1
            surface[indice + 3] = x
            surface[indice + 4] = z(x, y, t)
            surface[indice + 5] = y
            if j != 0:
                # Values were computed during the previous loop
                preindice = 6 * (i + (j - 1) * (RESOLUTION + 1))
                surface[indice] = surface[preindice + 3]
                surface[indice + 1] = surface[preindice + 4]
                surface[indice + 2] = surface[preindice + 5]
            else:
                surface[indice] = x
                surface[indice + 1] = z(x, -1, t)
                surface[indice + 2] = -1

    # Normals
    for j in range(RESOLUTION):
        for i in range(RESOLUTION + 1):
            indice = 6 * (i + j * (RESOLUTION + 1))

            v1x = surface[indice + 3]
            v1y = surface[indice + 4]
            v1z = surface[indice + 5]

            v2x = v1x
            v2y = surface[indice + 1]
            v2z = surface[indice + 2]

            if i < RESOLUTION:
                v3x = surface[indice + 9]
                v3y = surface[indice + 10]
                v3z = v1z
            else:
                v3x = xn
                v3y = z(xn, v1z, t)
                v3z = v1z

            vax = v2x - v1x
            vay = v2y - v1y
            vaz = v2z - v1z

            vbx = v3x - v1x
            vby = v3y - v1y
            vbz = v3z - v1z

            nx = (vby * vaz) - (vbz * vay)
            ny = (vbz * vax) - (vbx * vaz)
            nz = (vbx * vay) - (vby * vax)

            l = sqrt(nx * nx + ny * ny + nz * nz)
            if l != 0:
                l = 1 / l
                normal[indice + 3] = nx * l
                normal[indice + 4] = ny * l
                normal[indice + 5] = nz * l
            else:
                normal[indice + 3] = 0
                normal[indice + 4] = 1
                normal[indice + 5] = 0

            if j != 0:
                # Values were computed during the previous loop
                preindice = 6 * (i + (j - 1) * (RESOLUTION + 1))
                normal[indice] = normal[preindice + 3]
                normal[indice + 1] = normal[preindice + 4]
                normal[indice + 2] = normal[preindice + 5]
            else:
                # v1x = v1x
                v1y = z(v1x, (j - 1) * delta - 1, t)
                v1z = (j - 1) * delta - 1

                # v3x = v3x
                v3y = z(v3x, v2z, t)
                v3z = v2z

                vax = v1x - v2x
                vay = v1y - v2y
                vaz = v1z - v2z

                vbx = v3x - v2x
                vby = v3y - v2y
                vbz = v3z - v2z

                nx = (vby * vaz) - (vbz * vay)
                ny = (vbz * vax) - (vbx * vaz)
                nz = (vbx * vay) - (vby * vax)

                l = sqrt(nx * nx + ny * ny + nz * nz)
                if l != 0:
                    l = 1 / l
                    normal[indice] = nx * l
                    normal[indice + 1] = ny * l
                    normal[indice + 2] = nz * l
                else:
                    normal[indice] = 0
                    normal[indice + 1] = 1
                    normal[indice + 2] = 0


    glTranslatef(1, n, 1)

    # Render wireframe?
    if wire_frame:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # The water
    glEnable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    glNormalPointer(GL_FLOAT, 0, normal)
    glVertexPointer(3, GL_FLOAT, 0, surface)
    for i in range(RESOLUTION):
        glDrawArrays(GL_TRIANGLE_STRIP, i * length, length)

    # Draw normals?
    if normals != 0:
        glDisable(GL_TEXTURE_2D)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        for j in range(RESOLUTION):
            for i in range(RESOLUTION + 1):
                indice = 6 * (i + j * (RESOLUTION + 1))
                # glVertex3fv (*surface[indice])
                glVertex3f(surface[indice], surface[indice + 1],
                           surface[indice + 2])
                glVertex3f(surface[indice] + normal[indice] / 3,
                           surface[indice + 1] + normal[indice + 1] / 3,
                           surface[indice + 2] + normal[indice + 2] / 3)
        glEnd()
    glTranslatef(-1, -n, -1)
    return


def less_bloated_display_func():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(x_pos, y_pos, z_pos,  # pos camera
              x_pos, -10 + y_pos, -10 + z_pos,  # look at
              0, 1, 0)  # up vector
    if display_grid_toggle:
        display_grid()

    water_render()
    # End
    glFlush()
    glutSwapBuffers()
    glutPostRedisplay()

def display_func():
    """Get called to update rendering."""
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.
    delta = 2. / RESOLUTION
    length = 2 * (RESOLUTION + 1)
    xn = (RESOLUTION + 1) * delta + 1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0, 0, -translate_z)
    glRotatef(rotate_y, 1, 0, 0)
    glRotatef(rotate_x, 0, 1, 0)

    # Vertices
    for j in range(RESOLUTION):
        y = (j + 1) * delta - 1
        for i in range(RESOLUTION + 1):
            indice = 6 * (i + j * (RESOLUTION + 1))
            x = i * delta - 1
            surface[indice + 3] = x
            surface[indice + 4] = z(x, y, t)
            surface[indice + 5] = y
            if j != 0:
                # Values were computed during the previous loop
                preindice = 6 * (i + (j - 1) * (RESOLUTION + 1))
                surface[indice] = surface[preindice + 3]
                surface[indice + 1] = surface[preindice + 4]
                surface[indice + 2] = surface[preindice + 5]
            else:
                surface[indice] = x
                surface[indice + 1] = z(x, -1, t)
                surface[indice + 2] = -1

    # Normals
    for j in range(RESOLUTION):
        for i in range(RESOLUTION + 1):
            indice = 6 * (i + j * (RESOLUTION + 1))

            v1x = surface[indice + 3]
            v1y = surface[indice + 4]
            v1z = surface[indice + 5]

            v2x = v1x
            v2y = surface[indice + 1]
            v2z = surface[indice + 2]

            if i < RESOLUTION:
                v3x = surface[indice + 9]
                v3y = surface[indice + 10]
                v3z = v1z
            else:
                v3x = xn
                v3y = z(xn, v1z, t)
                v3z = v1z

            vax = v2x - v1x
            vay = v2y - v1y
            vaz = v2z - v1z

            vbx = v3x - v1x
            vby = v3y - v1y
            vbz = v3z - v1z

            nx = (vby * vaz) - (vbz * vay)
            ny = (vbz * vax) - (vbx * vaz)
            nz = (vbx * vay) - (vby * vax)

            l = sqrt(nx * nx + ny * ny + nz * nz)
            if l != 0:
                l = 1 / l
                normal[indice + 3] = nx * l
                normal[indice + 4] = ny * l
                normal[indice + 5] = nz * l
            else:
                normal[indice + 3] = 0
                normal[indice + 4] = 1
                normal[indice + 5] = 0

            if j != 0:
                # Values were computed during the previous loop
                preindice = 6 * (i + (j - 1) * (RESOLUTION + 1))
                normal[indice] = normal[preindice + 3]
                normal[indice + 1] = normal[preindice + 4]
                normal[indice + 2] = normal[preindice + 5]
            else:
                # v1x = v1x
                v1y = z(v1x, (j - 1) * delta - 1, t)
                v1z = (j - 1) * delta - 1

                # v3x = v3x
                v3y = z(v3x, v2z, t)
                v3z = v2z

                vax = v1x - v2x
                vay = v1y - v2y
                vaz = v1z - v2z

                vbx = v3x - v2x
                vby = v3y - v2y
                vbz = v3z - v2z

                nx = (vby * vaz) - (vbz * vay)
                ny = (vbz * vax) - (vbx * vaz)
                nz = (vbx * vay) - (vby * vax)

                l = sqrt(nx * nx + ny * ny + nz * nz)
                if l != 0:
                    l = 1 / l
                    normal[indice] = nx * l
                    normal[indice + 1] = ny * l
                    normal[indice + 2] = nz * l
                else:
                    normal[indice] = 0
                    normal[indice + 1] = 1
                    normal[indice + 2] = 0

    # The ground
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glColor3f(1, 0.9, 0.7)
    # glBegin(GL_TRIANGLE_FAN)
    # glVertex3f(-1, 0, -1)
    # glVertex3f(-1, 0, 1)
    # glVertex3f(1, 0, 1)
    # glVertex3f(1, 0, -1)
    # glEnd()

    glTranslatef(0, 0.2, 0)

    # Render wireframe?
    if wire_frame:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # The water
    glEnable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    glNormalPointer(GL_FLOAT, 0, normal)
    glVertexPointer(3, GL_FLOAT, 0, surface)
    for i in range(RESOLUTION):
        glDrawArrays(GL_TRIANGLE_STRIP, i * length, length)

    # Draw normals?
    if normals != 0:
        glDisable(GL_TEXTURE_2D)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        for j in range(RESOLUTION):
            for i in range(RESOLUTION + 1):
                indice = 6 * (i + j * (RESOLUTION + 1))
                # glVertex3fv (*surface[indice])
                glVertex3f(surface[indice], surface[indice + 1],
                           surface[indice + 2])
                glVertex3f(surface[indice] + normal[indice] / 50,
                           surface[indice + 1] + normal[indice + 1] / 50,
                           surface[indice + 2] + normal[indice + 2] / 50)
        glEnd()

    # End
    glFlush()
    glutSwapBuffers()
    glutPostRedisplay()


def reshape_func(width, height):
    """Get called when the window is created or resized."""
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(110, width / float(height), 3, 150)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()

def display_grid():
    """
    Affichage de la grille.

    Affiche un grille pour un meilleur comprehension
    du mouvement de la camera.
    """
    glDisable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    n = 90
    for i in range(-n, n):
        # x, y
        glVertex3f(i, -n, 0.0)
        glVertex3f(i, n, 0.0)

        glVertex3f(-n, i, 0.0)
        glVertex3f(n, i, 0.0)

        # x, z
        glVertex3f(i, 0.0, -n)
        glVertex3f(i, 0.0, n)

        glVertex3f(-n, 0.0, i)
        glVertex3f(n, 0.0, i)

        # y, z
        glVertex3f(0.0, i, -n)
        glVertex3f(0.0, i, n)

        glVertex3f(0.0, -n, i)
        glVertex3f(0.0, n, i)

    glEnd()
    return

def keyboard_func(key, x, y):
    """Get called when a key is hit."""
    global wire_frame, normals, x_pos, y_pos, z_pos, display_grid_toggle

    key = key.decode('utf8')

    if key in ('q', 'Q', '\033'):
        glutLeaveMainLoop()
    elif key in ('f', 'F', 'p', 'P'):
        wire_frame = not wire_frame
    elif key in ('n', 'N'):
        normals = 1 - normals
    elif key == 'w':
        y_pos -= 1
    elif key == 's':
        y_pos += 1
    elif key == 'j':
        z_pos += 1
    elif key == 'k':
        z_pos -= 1
    elif key == 'h':
        x_pos -= 1
    elif key == 'l':
        x_pos += 1
    elif key == 'd':
        display_grid_toggle = not display_grid_toggle


def mouse_func(button, state, x, y):
    """Get called when a mouse button is hit."""
    global left_click, right_click, xold, yold
    print(x,y)

    if (GLUT_LEFT_BUTTON == button):
        left_click = state
    if (GLUT_RIGHT_BUTTON == button):
        right_click = state
    xold = x
    yold = y


def motion_func(x, y):
    """Get called when the mouse is moved."""
    global rotate_x, rotate_y, translate_z, xold, yold

    if (GLUT_DOWN == left_click):
        rotate_y = rotate_y + (y - yold) / 5.0
        rotate_x = rotate_x + (x - xold) / 5.0
        if (rotate_y > 90):
            rotate_y = 90
        if (rotate_y < -90):
            rotate_y = -90
        glutPostRedisplay()
    if (GLUT_DOWN == right_click):
        rotate_x = rotate_x + (x - xold) / 5.
        translate_z = translate_z + (yold - y) / 50.
        if (translate_z < 0.5):
            translate_z = 0.5
        if (translate_z > 10):
            translate_z = 10
        glutPostRedisplay()
    xold = x
    yold = y


def init_water():
    """Initialise les parametres globaux."""
    total_texture = [0 for i in range(4 * 256 * 256)]
    alpha_texture = []  # [256 * 256]
    caustic_texture = []  # [3 * 256 * 256]
    i = 0

    init_noise()

    # OpenGL settings
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    # Texture loading
    texture = glGenTextures(1)
    # alpha.jpg : alpha_texture, GL_ALPHA, 256
    alpha_texture = load_texture("alpha.jpg")  # bytes array
    # reflection.jpg : caustic_texture, GL_RGB, 256
    caustic_texture = load_texture("reflection.jpg")  # bytes array
    # int array
    for i in range(256 * 256):
        total_texture[4 * i] = caustic_texture[3 * i]
        total_texture[4 * i + 1] = caustic_texture[3 * i + 1]
        total_texture[4 * i + 2] = caustic_texture[3 * i + 2]
        total_texture[4 * i + 3] = alpha_texture[i]

    glBindTexture(GL_TEXTURE_2D, texture)
    # conversion en bytes indispensable
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, 256, 256, GL_RGBA,
                      GL_UNSIGNED_BYTE, bytes(total_texture))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

if __name__ == '__main__':
    from sys import argv

    # Creation of the window
    glutInit(argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Water")

    init_water()
    # Declaration of the callbacks
    glutDisplayFunc(less_bloated_display_func)
    glutReshapeFunc(reshape_func)
    glutKeyboardFunc(keyboard_func)
    glutMouseFunc(mouse_func)
    glutMotionFunc(motion_func)

    # Loop
    glutMainLoop()

    # Never reached
    exit(0)
