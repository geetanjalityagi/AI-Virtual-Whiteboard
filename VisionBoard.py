import cv2 
import time
from HandTrackingModule import handDetector


cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

toolbar = cv2.imread("assests/Colors.jpg")
toolbar = cv2.resize(toolbar, (1280, 150))

detector = handDetector(num_hands=1)

colorBar = (255, 0, 0)

ptime = 0
while(True):
    ok, img = cap.read()

    if not ok:
        break

    img = cv2.flip(img, 1)

    img[0:150, 0:1280] = toolbar

    img = detector.findhands(img)
    lmlist = detector.findpoints(img)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1], lmlist[8][2]
        x2, y2 = lmlist[12][1], lmlist[12][2]

        if (lmlist[8][1] < lmlist[6][1]) and (lmlist[12][1] < lmlist[10][1]):
            cv2.rectangle(img, (x1, y1), (x2,y2), colorBar, -1)


    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, f"FPS : {fps : .2f}", (40, 180), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
