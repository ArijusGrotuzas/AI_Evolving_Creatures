import math
import numpy
import cv2


def cosine_interpolation(a, b, t):
    ft = t * math.pi
    f = (1 - math.cos(ft)) * 0.5
    return a * (1 - f) + b * f


def random_gradient(x, y):
    random = 2920.0 * math.sin(x * 21942.0 + y * 171324.0 + 8912.0) * math.cos(x * 23157.0 * y * 217832.0 + 9758.0)
    return math.cos(random), math.sin(random)


def dot_grid_gradient(ix, iy, x, y):
    # Get gradient from integer coordinates
    (gradientX, gradientY) = random_gradient(ix, iy)

    # Compute the distance vector
    dx = x - float(ix)
    dy = y - float(iy)

    # Compute the dot-product
    return dx * gradientX + dy * gradientY


def perlin(x, y):
    # Determine grid cell coordinates
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1

    # Determine interpolation weights
    # Could also use higher order polynomial/s-curve here
    sx = x - float(x0)
    sy = y - float(y0)

    # Interpolate between grid point gradients
    n0 = dot_grid_gradient(x0, y0, x, y)
    n1 = dot_grid_gradient(x1, y0, x, y)
    ix0 = cosine_interpolation(n0, n1, sx)

    n0 = dot_grid_gradient(x0, y1, x, y)
    n1 = dot_grid_gradient(x1, y1, x, y)
    ix1 = cosine_interpolation(n0, n1, sx)

    return cosine_interpolation(ix0, ix1, sy)


def create_landscape(size, threshold, amplitude):
    landscape = [[0 for _ in range(size)] for __ in range(size)]

    for i in range(size):
        for j in range(size):
            n = perlin(i * amplitude, j * amplitude)

            n += 1.0
            n /= 2.0

            if n > threshold:
                landscape[i][j] = 1.0
            else:
                landscape[i][j] = 0.0

    return landscape
    # perlin_noise = numpy.array(landscape)
    # print(landscape)
    # cv2.imshow('perlin', cv2.resize(perlin_noise, (800, 800), interpolation=cv2.INTER_AREA))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def main():
    land = create_landscape(50, 0.45, 0.1)
    print(land)


if __name__ == '__main__':
    main()
