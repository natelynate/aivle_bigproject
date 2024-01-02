x = [1410, 1478, 1398, 1329, 1405, 1337, 1404, 1339, 1324, 1337, 1185, 965, 961, 961, 957, 960, 952, 953, 960, 964, 962, 876, 958, 956, 965, 1031]
y = [226, 230, 226, 222, 229, 227, 212, 232, 217, 220, 172, 227, 237, 175, 178, 233, 167, 171, 225, 115, 170, 177, 176, 174, 175, 174]

def findScaleFactor(x, y):
    min_x, min_y, max_x, max_y = 1e99, 1e99, -1e99, -1e99
    for pixel_x, pixel_y in zip(x, y):
        min_x, min_y = min(pixel_x, min_x), min(pixel_y, min_y)
        max_x, max_y = max(pixel_x, max_x), max(pixel_y, max_y)
    return min_x, min_y, max_x, max_y

def translatePoint(x, y):
    min_x, min_y, max_x, max_y = findScaleFactor(x, y)

    for pixel_x, pixel_y in zip(x, y):
        pixel_x = (pixel_x-min_x)/(max_x-min_x) * 1920
        pixel_y = (pixel_y-min_y)/(max_y-min_y) * 1080
        print(round(pixel_x), round(pixel_y))

translatePoint(x, y)