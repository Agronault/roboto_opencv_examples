import cv2

#meme = cv2.imread('photos/meme.jpg')
#cv2.imshow('meme', meme)
#cv2.waitKey(0)

#########################################################

#wv = cv2.VideoCapture('videos/winvista.mp4')

#while True:
#    status, img = wv.read()
#    cv2.imshow("windows vista", img)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

#########################################################

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
cam.set(10, 50)

while True:
    status, img = cam.read()
    cv2.imshow("cam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break