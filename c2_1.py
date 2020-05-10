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


def get_contours(cnt_img):
    contours, hierarchy = c.findContours(cnt_img, c.RETR_EXTERNAL, c.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = c.contourArea(cnt)
        print(area)
        if area > 500:
            c.drawContours(imgCnt, cnt, -1, (241, 58, 255), 5)
            peri = c.arcLength(cnt, True)
            approx = c.approxPolyDP(cnt, 0.02*peri, True)
            obj_cor = len(approx)
            x, y, w, h = c.boundingRect(approx)

            obj_type = '???'
            if obj_cor == 3:
                obj_type = 'Triangulo'
            elif obj_cor == 4:
                asp_ratio = w/float(h)
                if (float(peri)/4)**2 - 100 < area < (float(peri)/4)**2 + 100:
                    obj_type = 'Quadrado'
                else:
                    obj_type = 'Retangulo'
            elif obj_cor > 4:
                obj_type = 'Circulo?'

            c.rectangle(imgCnt, (x, y), (x+w, y+h), (106, 0, 255), 2)
            c.putText(imgCnt, obj_type,
                      (x+w//2-10, y+h//2-10), c.FONT_ITALIC, 0.5,
                      (0, 0, 0), 2)


path = 'photos/shapes.png'
img = c.imread(path)

imgGray = c.cvtColor(img, c.COLOR_BGR2GRAY)
imgBlur = c.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = c.Canny(imgBlur, 50, 50)
imgCnt = img.copy()
get_contours(imgCanny)

imgStack = stack_images(0.7, ([img, imgGray, imgBlur],
                              [imgCanny, imgCnt, imgBlur]))
c.imshow('stack', imgStack)

c.waitKey(0)
