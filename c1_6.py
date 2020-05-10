import cv2 as c
import numpy as n


def show_canvas(canvas_name, canvas_img, cnv_factor=3):
    canvas_w = canvas_img.shape[0]
    canvas_h = canvas_img.shape[1]
    c.imshow(canvas_name, c.resize(canvas_img, (int(canvas_h/cnv_factor), int(canvas_w/cnv_factor))))


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


def empty(arg):
    pass


c.namedWindow('TrackBars')
c.resizeWindow('TrackBars', 640, 240)
c.createTrackbar('Hue Min', 'TrackBars', 145, 179, empty)
c.createTrackbar('Hue Max', 'TrackBars', 173, 179, empty)
c.createTrackbar('Sat Min', 'TrackBars', 121, 255, empty)
c.createTrackbar('Sat Max', 'TrackBars', 255, 255, empty)
c.createTrackbar('Val Min', 'TrackBars', 122, 255, empty)
c.createTrackbar('Val Max', 'TrackBars', 255, 255, empty)

cam = c.VideoCapture(0)

while True:
    #img = c.imread('photos/yugioh.jpg')
    status, img = cam.read()

    imgHSV = c.cvtColor(img, c.COLOR_BGR2HSV)

    h_min = c.getTrackbarPos('Hue Min', 'TrackBars')
    h_max = c.getTrackbarPos('Hue Max', 'TrackBars')
    s_min = c.getTrackbarPos('Sat Min', 'TrackBars')
    s_max = c.getTrackbarPos('Sat Max', 'TrackBars')
    v_min = c.getTrackbarPos('Val Min', 'TrackBars')
    v_max = c.getTrackbarPos('Val Max', 'TrackBars')

    lower = n.array([h_min, s_min, v_min])
    upper = n.array([h_max, s_max, v_max])
    mask = c.inRange(imgHSV, lower, upper)
    maskedImg = c.bitwise_and(img, img, mask=mask)

    # c.imshow("img", img)
    show_canvas("mask", mask, 2)
    imgStack = stack_images(0.2, ([img, imgHSV], [mask, maskedImg]))
    c.imshow("Stack View", imgStack)

    if c.waitKey(1) & 0xFF == ord('q'):
        break
