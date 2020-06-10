import time

import numpy as np
from numba import jit

from matplotlib import colors
from matplotlib import pyplot as plt


@jit
def mandelbrot(creal, cimag, maxiter, horizon, log_horizon):
    real = creal
    imag = cimag
    for n in range(maxiter):
        real2 = real*real
        imag2 = imag*imag
        if real2 + imag2 > horizon:
            return n - np.log(np.log(real2+imag2))/np.log(2) + log_horizon
        imag = 2 * real*imag + cimag
        real = real2 - imag2 + creal
    return 0


@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    horizon = 2.0 ** 40
    log_horizon = np.log(np.log(horizon))/np.log(2)
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i], r2[j], maxiter, horizon, log_horizon)
    return (r1, r2, n3)


def mandelbrot_image(xmin, xmax, ymin, ymax, width=10, height=10,
                     maxiter=256, cmap="jet", gamma=0.3):
    dpi = 72
    img_width = dpi * width
    img_height = dpi * height
    x, y, z = mandelbrot_set(xmin, xmax, ymin, ymax,
                             img_width, img_height, maxiter)

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)

    plt.axis("off")
    norm = colors.PowerNorm(gamma)
    plt.imshow(z.T, cmap=cmap, origin='lower', norm=norm)

    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    filename = "images\\mandelbrot_%s_iter%s_%s.png" % (
        cmap, maxiter, time.strftime("%H-%M-%S"))
    fig.savefig(filename, bbox_inches=extent, pad_inches=0,)
    plt.close()


def make_fractal(x, y, range, width=10, height=10, maxiter=512, cmap="jet"):
    xmin = x-range
    xmax = x+range
    ymin = y-range
    ymax = y+range
    mandelbrot_image(xmin, xmax, ymin, ymax, maxiter=maxiter,
                     width=width, height=height, cmap=cmap)


def animation():
    for n in range(500, 2048, 10):
        make_fractal(-0.748, 0.1, 0.0014, maxiter=n, cmap='inferno')
        print("Frame %i complete" % n)

# cmaps = ['viridis', 'plasma', 'inferno', 'magma',
#         ('Sequential (2)', [
#            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
#            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
#            'hot', 'afmhot', 'gist_heat', 'copper']),
#         ('Diverging', [
#            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
#            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
#            'ocean', 'gist_earth', 'terrain',
#            'gnuplot', 'gnuplot2', 'CMRmap', 'brg', 'hsv',
#          'gist_rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


start = time.time()
make_fractal( 0.3750001200618655, -0.2166393884377127,
             0.000000000002, maxiter=1000000000, cmap='jet')
end = time.time()
print("Total time: %i seconds" % (end-start))
