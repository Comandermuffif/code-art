import math

if __name__ == "__main__":
    center = (0.5, 0.5)
    segments = 20
    radious = 0.45

    x_skew = 1 #math.sin(math.radians(45))
    y_skew = 1

    print([
        [
            str(center[0] + math.cos(math.radians(360 * (float(x)/segments))) * radious * x_skew),
            str(center[1] + math.sin(math.radians(360 * (float(x)/segments))) * radious * y_skew)
        ]
        for x in range(segments)
    ])