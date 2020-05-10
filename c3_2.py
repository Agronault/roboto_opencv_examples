import cv2 as c
import numpy as n

cam_w = 640
cam_h = 480

img_w = 640
img_h = 480

cam = c.VideoCapture(1)
cam.set(3, img_w)
cam.set(4, img_h)


def pre_processing(img):
    img_gray = c.cvtColor(img, c.COLOR_BGR2GRAY)
    img_blur = c.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = c.Canny(img_blur, 200, 200)
    kernel = n.ones((5, 5))
    img_dilate = c.dilate(img_canny, kernel, iterations=2)
    img_thres = c.erode(img_dilate, kernel, iterations=1)
    return img_thres


def get_contours(cnt_img):
    contours, hierarchy = c.findContours(cnt_img, c.RETR_EXTERNAL, c.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    biggest = n.array([])
    maxArea = 0
    for cnt in contours:
        area = c.contourArea(cnt)
        if area > 4000:
            #c.drawContours(imgCont, cnt, -1, (241, 58, 255), 5)
            peri = c.arcLength(cnt, True)
            approx = c.approxPolyDP(cnt, 0.02*peri, True)
            print(len(approx))
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    c.drawContours(imgCont, biggest, -1, (241, 58, 255), 20)
    return biggest


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


def reorder_point(points):
    points = points.reshape((4, 2))
    points_new = n.zeros((4, 1, 2), n.int32)

    add = points.sum(1)
    points_new[0] = points[n.argmin(add)]
    points_new[3] = points[n.argmax(add)]

    diff = n.diff(points, axis=1)
    points_new[1] = points[n.argmin(diff)]
    points_new[2] = points[n.argmax(diff)]

    return points_new

def get_warp(img, biggest):
    try:
        biggest = reorder_point(biggest)
        pt1 = n.float32(biggest)
        pt2 = n.float32([[0, 0], [img_w, 0], [0, img_h], [img_w, img_h]])
        matrix = c.getPerspectiveTransform(pt1, pt2)
        img_out = c.warpPerspective(img, matrix, (img_w, img_h))
        img_out_crop = img_out[20:img_out.shape[0]-20, 20:img_out.shape[1]-20]
        img_out_crop = c.resize(img_out_crop, (img_w, img_h))
        return img_out_crop
    except:
        return img

while True:
    status, img = cam.read()
    img = c.resize(img, (img_w, img_h))
    imgCont = img.copy()
    imgThres = pre_processing(img)

    biggest = get_contours(imgThres)
    get_warp(img, biggest)
    imgWarp = get_warp(img, biggest)

    stack = stack_images(0.8, ([img, imgThres, imgCont], [imgWarp, img, img]))
    c.imshow("cam", stack)
    if c.waitKey(1) & 0xFF == ord('q'):
        break
