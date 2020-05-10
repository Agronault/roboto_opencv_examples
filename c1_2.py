import cv2 as c
import numpy as n

kernel = n.ones((5, 5), n.uint8)

img = c.imread("photos/park.jpg")
c.imshow("img", img)
print(img.shape)

imgResize = c.resize(img, (300, 200))
#c.imshow("imgRes", imgResize)

imgCropped = img[0:200, 200:500]
c.imshow("imgCrop", imgCropped)

imgGray = c.cvtColor(img, c.COLOR_BGR2GRAY)
imgBlur = c.GaussianBlur(img, (7, 7), 0)
imgCanny = c.Canny(img, 150, 200)
imgDilation = c.dilate(imgCanny, kernel, iterations=5)
imgEroded = c.erode(imgDilation, kernel, iterations=1)

c.imshow("imgF", imgDilation)
c.waitKey(0)