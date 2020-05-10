import cv2 as c
import numpy as n


def findColor(img, color, bgr_color, name='none'):
    imgHSV = c.cvtColor(img, c.COLOR_BGR2HSV)
    lower = n.array([color[0], color[2], color[4]])
    upper = n.array([color[1], color[3], color[5]])
    mask = c.inRange(imgHSV, lower, upper)
    x, y = get_contours(mask)
    if x + y != 0:
        c.circle(imgFinal, (x, y), 20, bgr_color, c.FILLED)
        myPoints.append([name, (x, y)])
    canvas_draw(myPoints, bgr_color, name)
    c.imshow(name, mask)


def get_contours(cnt_img):
    contours, hierarchy = c.findContours(cnt_img, c.RETR_EXTERNAL, c.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = c.contourArea(cnt)
        if area > 500:
            #c.drawContours(imgFinal, cnt, -1, (241, 58, 255), 5)
            peri = c.arcLength(cnt, True)
            approx = c.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = c.boundingRect(approx)
    return x+w//2, y


def canvas_draw(points, bgr_color, color_name):
    for point in myPoints:
        if point[0] == color_name:
            c.circle(imgFinal, point[1], 10, bgr_color, c.FILLED)


frame_w = 640
frame_h = 480

red = [130, 179, 127, 255, 139, 255]
blue = [101, 166, 127, 255, 139, 255]
green = [62, 83, 127, 255, 60, 255]
yellow = [25, 45, 123, 255, 136, 255]

bgrRed = (0, 0, 255)
bgrBlue = (255, 0, 0)
bgrGreen = (0, 255, 0)
bgrYellow = (0, 255, 255)

myColors = [red, blue, green, yellow]

myPoints = []  # ["nome", (x, y)]

cam = c.VideoCapture(0)
cam.set(3, frame_w)
cam.set(4, frame_h)

while True:
    status, img = cam.read()
    imgFinal = img.copy()
    findColor(img, red, bgrRed, "red")
    findColor(img, blue, bgrBlue, "blue")
    findColor(img, green, bgrGreen, "green")
    findColor(img, yellow, bgrYellow, "yellow")
    c.imshow("cam", imgFinal)
    if c.waitKey(1) & 0xFF == ord('q'):
        break
