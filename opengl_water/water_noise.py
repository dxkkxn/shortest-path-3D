"""
Improved Perlin noise.
Copyright (C) 2005  Julien Guertault
Original Perlin noise implementation can be found at :
http://mrl.nyu.edu/~perlin/doc/oscar.html#noise

Python conversion
"""


from random import randint

MOD = 0xff

permut = []
gradient = [
    [ 1,  1,  1,  0], [ 1,  1,  0,  1], [ 1,  0,  1,  1], [ 0,  1,  1,  1],
    [ 1,  1, -1,  0], [ 1,  1,  0, -1], [ 1,  0,  1, -1], [ 0,  1,  1, -1],
    [ 1, -1,  1,  0], [ 1, -1,  0,  1], [ 1,  0, -1,  1], [ 0,  1, -1,  1],
    [ 1, -1, -1,  0], [ 1, -1,  0, -1], [ 1,  0, -1, -1], [ 0,  1, -1, -1],
    [-1,  1,  1,  0], [-1,  1,  0,  1], [-1,  0,  1,  1], [ 0, -1,  1,  1],
    [-1,  1, -1,  0], [-1,  1,  0, -1], [-1,  0,  1, -1], [ 0, -1,  1, -1],
    [-1, -1,  1,  0], [-1, -1,  0,  1], [-1,  0, -1,  1], [ 0, -1, -1,  1],
    [-1, -1, -1,  0], [-1, -1,  0, -1], [-1,  0, -1, -1], [ 0, -1, -1, -1],
]


def InitNoise():
    global permut
    
    permut = [randint(0, 32767) & MOD for i in range(256)]


def Indice(i, j, k, l):
    """ finding out the gradient corresponding to the coordinates """
    return permut[(l + permut[(k + permut[(j + permut[i & MOD]) & MOD]) & MOD]) & MOD] & 0x1f


def Prod (a, b):
    if (b > 0):
        return a
    if (b < 0):
        return -a
    return 0

def Dot_prod (x1, x2, y1, y2, z1, z2, t1, t2):
    """ computing the dot product of the vector and the gradient """
    return Prod (x1, x2) + Prod (y1, y2) + Prod (z1, z2) + Prod (t1, t2)


def Spline5 (state):
    """
    computing interpolations
    Enhanced spline :
    (3x^2 + 2x^3) is not as good as (6x^5 - 15x^4 + 10x^3)
    """
    sqr = state * state;
    return state * sqr * (6 * sqr - 15 * state + 10)


def Linear(start, end, state):
    """
    computing interpolations
    """
    return start + (end - start) * state


def Noise (x, y, z, t):
    """
    Noise function, returning the Perlin Noise at a given point
    """
    # The unit hypercube containing the point
    x1 = int(x if x > 0 else x - 1)
    y1 = int(y if y > 0 else y - 1)
    z1 = int(z if z > 0 else z - 1)
    t1 = int(t if t > 0 else t - 1)
    x2 = x1 + 1
    y2 = y1 + 1
    z2 = z1 + 1
    t2 = t1 + 1
    
    # The 16 corresponding gradients
    g0000 = gradient[Indice (x1, y1, z1, t1)]
    g0001 = gradient[Indice (x1, y1, z1, t2)]
    g0010 = gradient[Indice (x1, y1, z2, t1)]
    g0011 = gradient[Indice (x1, y1, z2, t2)]
    g0100 = gradient[Indice (x1, y2, z1, t1)]
    g0101 = gradient[Indice (x1, y2, z1, t2)]
    g0110 = gradient[Indice (x1, y2, z2, t1)]
    g0111 = gradient[Indice (x1, y2, z2, t2)]
    g1000 = gradient[Indice (x2, y1, z1, t1)]
    g1001 = gradient[Indice (x2, y1, z1, t2)]
    g1010 = gradient[Indice (x2, y1, z2, t1)]
    g1011 = gradient[Indice (x2, y1, z2, t2)]
    g1100 = gradient[Indice (x2, y2, z1, t1)]
    g1101 = gradient[Indice (x2, y2, z1, t2)]
    g1110 = gradient[Indice (x2, y2, z2, t1)]
    g1111 = gradient[Indice (x2, y2, z2, t2)]
    
    # The 16 vectors
    dx1 = x - x1
    dx2 = x - x2
    dy1 = y - y1
    dy2 = y - y2
    dz1 = z - z1
    dz2 = z - z2
    dt1 = t - t1
    dt2 = t - t2
    
    # The 16 dot products
    b0000 = Dot_prod(dx1, g0000[0], dy1, g0000[1],
		     dz1, g0000[2], dt1, g0000[3])
    b0001 = Dot_prod(dx1, g0001[0], dy1, g0001[1],
		     dz1, g0001[2], dt2, g0001[3])
    b0010 = Dot_prod(dx1, g0010[0], dy1, g0010[1],
		     dz2, g0010[2], dt1, g0010[3])
    b0011 = Dot_prod(dx1, g0011[0], dy1, g0011[1],
		     dz2, g0011[2], dt2, g0011[3])
    b0100 = Dot_prod(dx1, g0100[0], dy2, g0100[1],
		     dz1, g0100[2], dt1, g0100[3])
    b0101 = Dot_prod(dx1, g0101[0], dy2, g0101[1],
		     dz1, g0101[2], dt2, g0101[3])
    b0110 = Dot_prod(dx1, g0110[0], dy2, g0110[1],
		     dz2, g0110[2], dt1, g0110[3])
    b0111 = Dot_prod(dx1, g0111[0], dy2, g0111[1],
		     dz2, g0111[2], dt2, g0111[3])
    b1000 = Dot_prod(dx2, g1000[0], dy1, g1000[1],
		     dz1, g1000[2], dt1, g1000[3])
    b1001 = Dot_prod(dx2, g1001[0], dy1, g1001[1],
		     dz1, g1001[2], dt2, g1001[3])
    b1010 = Dot_prod(dx2, g1010[0], dy1, g1010[1],
		     dz2, g1010[2], dt1, g1010[3])
    b1011 = Dot_prod(dx2, g1011[0], dy1, g1011[1],
		     dz2, g1011[2], dt2, g1011[3])
    b1100 = Dot_prod(dx2, g1100[0], dy2, g1100[1],
		     dz1, g1100[2], dt1, g1100[3])
    b1101 = Dot_prod(dx2, g1101[0], dy2, g1101[1],
		     dz1, g1101[2], dt2, g1101[3])
    b1110 = Dot_prod(dx2, g1110[0], dy2, g1110[1],
		     dz2, g1110[2], dt1, g1110[3])
    b1111 = Dot_prod(dx2, g1111[0], dy2, g1111[1],
		     dz2, g1111[2], dt2, g1111[3])
    
    # Then the interpolations, down to the result
    idx1 = Spline5 (dx1)
    idy1 = Spline5 (dy1)
    idz1 = Spline5 (dz1)
    idt1 = Spline5 (dt1)
    
    b111 = Linear (b1110, b1111, idt1)
    b110 = Linear (b1100, b1101, idt1)
    b101 = Linear (b1010, b1011, idt1)
    b100 = Linear (b1000, b1001, idt1)
    b011 = Linear (b0110, b0111, idt1)
    b010 = Linear (b0100, b0101, idt1)
    b001 = Linear (b0010, b0011, idt1)
    b000 = Linear (b0000, b0001, idt1)
    
    b11 = Linear (b110, b111, idz1)
    b10 = Linear (b100, b101, idz1)
    b01 = Linear (b010, b011, idz1)
    b00 = Linear (b000, b001, idz1)
    
    b1 = Linear (b10, b11, idy1)
    b0 = Linear (b00, b01, idy1)
    
    return Linear (b0, b1, idx1)
