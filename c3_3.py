import cv2 as c


nPlate = c.CascadeClassifier('ext/haarscascade_russian_plate.xml')
cam = c.VideoCapture('videos/russiaStreet360p.mp4')
cam.set(3, 640)
cam.set(4, 480)
minArea = 500
maxArea = 5000
count = 0


def empty(arg):
    pass


c.namedWindow('Controles Roboto')
c.resizeWindow('Controles Roboto', 640, 240)
c.createTrackbar('minArea', 'Controles Roboto', minArea, 5000, empty)
c.createTrackbar('maxArea', 'Controles Roboto', maxArea, 20000, empty)


while True:
    status, img = cam.read()
    imgGray = c.cvtColor(img, c.COLOR_BGR2GRAY)

    nPlateList = nPlate.detectMultiScale(imgGray, 1.1, 4)
    minArea = c.getTrackbarPos('minArea', 'Controles Roboto')
    maxArea = c.getTrackbarPos('maxArea', 'Controles Roboto')

    for (x, y, w, h) in nPlateList:
        area = w*h
        if minArea < area < maxArea:
            c.rectangle(img, (x, y), (x+w, y+h), (241, 58, 255), 2)
            c.putText(img, 'Placa Detectada', (x, y-5), c.FONT_ITALIC,
                      1, (241, 58, 255), 2)
            imgRoI = img[y:y+h, x:x+w]

    c.imshow('img', c.resize(img, (640, 480)))

    try:
        c.imshow('imgRoI', imgRoI)
    except:
        c.imshow('imgRoI', c.resize(imgGray, (640, 480)))

    if c.waitKey(1) & 0xFF == ord('s'):
        c.imwrite('scans/plate/nPlate_'+str(count)+".jpg", imgRoI)
        c.rectangle(img, (0, 200), (640, 300), (241, 58, 255), c.FILLED)
        c.putText(img, 'ESCANEADO', (150, 265), c.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
        c.imshow('Result', img)
        c.waitKey(5)
        count += 1
