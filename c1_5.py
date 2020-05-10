import cv2 as c
import numpy as n


def stack_images(scale, img_array):
    rows = len(img_array)
    cols = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = c.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = c.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]),
                                               None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y] = c.cvtColor(img_array[x][y], c.COLOR_GRAY2BGR)
        image_blank = n.zeros((height, width, 3), n.uint8)
        hor = [image_blank] * rows
        hor_con = [image_blank] * rows
        for x in range(0, rows):
            hor[x] = n.hstack(img_array[x])
        ver = n.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = c.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = c.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None, scale,
                                        scale)
            if len(img_array[x].shape) == 2: img_array[x] = c.cvtColor(img_array[x], c.COLOR_GRAY2BGR)
        hor = n.hstack(img_array)
        ver = hor
    return ver


kernel = n.ones((5, 5), n.uint8)
cam = c.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
while True:
    status, img = cam.read()
    imgGray = c.cvtColor(img, c.COLOR_BGR2GRAY)
    imgBlur = c.GaussianBlur(img, (7, 7), 0)
    imgCanny = c.Canny(img, 150, 200)
    imgDilation = c.dilate(imgCanny, kernel, iterations=2)
    imgEroded = c.erode(imgDilation, kernel, iterations=1)

    imgArray = stack_images(0.5, ([img, imgGray, imgBlur], [imgCanny, imgDilation, imgEroded]))

    c.imshow("cam", imgArray)
    if c.waitKey(1) & 0xFF == ord('q'):
        break
