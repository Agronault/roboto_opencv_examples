import cv2 as c
import numpy as n


def on_mouse(event, x, y, flags, param):
    if event == c.EVENT_LBUTTONDOWN:
        print(x)
        print(y)


img = c.imread("photos/yugioh.jpg")
w, h = 250, 350

pts1 = n.float32([[550, 279], [758, 257], [623, 576], [839, 548]])
pts2 = n.float32([[0, 0], [w, 0], [0, h], [w, h]])
matrix = c.getPerspectiveTransform(pts1, pts2)
imgTrat = c.warpPerspective(img, matrix, (w, h))

c.imshow("img", img)
c.imshow("imgTrat", imgTrat)
c.setMouseCallback("img", on_mouse)

c.waitKey(0)
