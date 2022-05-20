import numpy as np
import matplotlib.pyplot as plt
from time import time
from PIL import Image, ImageEnhance


maxiter = 10000
border = 4

x, y = -0.793197078177363, 0.16093721735804

pmin = x - 0.01
pmax = x + 0.01
qmin = y - 0.01
qmax = y + 0.01

# pmin = -2
# pmax = 2
# qmin = -2
# qmax = 2

ppoints = 2000
qpoints = 2000


def Mandelbrot(maxiter, border, pmin, pmax, qmin, qmax, ppoints, qpoints):
    image = np.zeros((ppoints, qpoints))
    p, q = np.mgrid[pmin:pmax:(ppoints * 1j), qmin:qmax:(qpoints * 1j)]
    c = p + 1j * q
    z = np.zeros(c.shape, dtype=np.complex128)
    for i in range(maxiter):
        z = z ** 2 + c
        mask = ((np.abs(z) > border) & (image == 0))
        image[mask] = i
        z[mask] = np.nan
    return image.T


start = time()
image = Mandelbrot(maxiter, border, pmin, pmax, qmin, qmax, ppoints, qpoints)
image = (image * 255. / np.max(image)).astype('uint8')
image = np.dstack((image, image, image))

img = Image.fromarray(image, mode='RGB')

r, g, b = img.split()

rr = np.random.uniform(0.5, 3.5)
rg = np.random.uniform(0.5, 3.5)
rb = np.random.uniform(0.5, 3.5)

print(rr, rg, rb)

r = r.point(lambda i: i * rr)
g = g.point(lambda i: i * rg)
b = b.point(lambda i: i * rb)

result = Image.merge('RGB', (r, g, b))

filter = ImageEnhance.Brightness(result)

result = filter.enhance(maxiter / 1200.)

print(time() - start)

result.save('result.png')
result.show()