import cv2 as c
import numpy as n

img = n.zeros((512, 512, 3), n.uint8)
# img[200:300] = 255, 0, 0

c.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
c.rectangle(img, (0, 0), (250, 350), (0, 0, 255), c.FILLED)
c.circle(img, (400, 50), 30, (255, 255, 0), 5)

c.putText(img, "PEPE THE FROG", (100, 200), c.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

c.imshow("Image", img)

c.waitKey(0)
