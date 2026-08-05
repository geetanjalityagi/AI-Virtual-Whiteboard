import cv2 
import time
from HandTrackingModule import handDetector

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

ptime = 0
while(True):
    ok, img = cap.read()

    if not ok:
        break

    img = cv2.flip(img, 1)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, f"FPS : {fps : .2f}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
