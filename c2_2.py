import cv2 as c

faceCascade = c.CascadeClassifier('ext/haarscascade_frontalface_default.xml')

cam = c.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

while True:
    status, img = cam.read()
    imgGray = c.cvtColor(img, c.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in faces:
        c.rectangle(img, (x, y), (x + w, y + h), (241, 58, 255), 2)

    c.imshow("port", img)
    if c.waitKey(1) & 0xFF == ord('q'):
        break
