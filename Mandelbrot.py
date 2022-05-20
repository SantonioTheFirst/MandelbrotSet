import numpy as np
import matplotlib.pyplot as plt
from time import time
from PIL import Image, ImageEnhance, ImageOps
import imageio

start_iter = 0
maxiter = 200
border = 4

x, y = -0.793197078177363, 0.16093721735804

pmin = x - 0.01
pmax = x + 0.01
qmin = y - 0.01
qmax = y + 0.01

pmin = -2.5
pmax = 1.5
qmin = -2
qmax = 2

ppoints = 300
qpoints = 300


def Mandelbrot_step(step, z, c, border, image):
    z = z ** 2 + c
    mask = ((np.abs(z) > border) & (image == 0))
    image[mask] = step
    z[mask] = np.nan
    return z, image


def Mandelbrot(maxiter, border, pmin, pmax, qmin, qmax, ppoints, qpoints, return_points=False, transpose=False):
    image = np.zeros((ppoints, qpoints))
    p, q = np.mgrid[pmin:pmax:(ppoints * 1j), qmin:qmax:(qpoints * 1j)]
    c = p + 1j * q
    z = np.zeros(c.shape, dtype=np.complex128)
    for i in range(maxiter):
        z, image = Mandelbrot_step(i, z, c, border, image)
    if transpose:
        image = image.T
        if return_points:
            c = c.T
            z = z.T
    if not return_points:
        return image
    else:
        return (image, c, z)


def make_pictures(start_iter, maxiter, border, pmin, pmax, qmin, qmax, ppoints, qpoints):
    image, c, z = Mandelbrot(start_iter, border, pmin, pmax, qmin, qmax, ppoints, qpoints, return_points=True, transpose=True)
    for i in range(start_iter, maxiter):
        z, image = Mandelbrot_step(i, z, c, border, image)
        img = (image * 255. / np.max(image)).astype('uint8')
        img = Image.fromarray(img, 'L')
        img = ImageOps.colorize(img, black='black', white='white', mid='green', blackpoint=5, whitepoint=255)
        img.save(f'result_{i}.png')

    
def make_gif(start_iter, maxiter):
    images = []
    for i in range(start_iter, maxiter - 1):
        im = f'result_{i}.png'
        images.append(imageio.imread(im))
    imageio.mimsave('animation.gif', images)


start = time()
make_pictures(start_iter, maxiter, border, pmin, pmax, qmin, qmax, ppoints, qpoints)
make_gif(start_iter, maxiter)
print(time() - start)