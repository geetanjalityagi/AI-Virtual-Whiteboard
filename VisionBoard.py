import cv2 
import time
from HandTrackingModule import handDetector
from toolbar import select_toolbar_tool


# Try opening camera 0 first, fall back to 1 if it fails
cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

toolbar = cv2.imread("assets/Colors.jpg")
if toolbar is not None:
    toolbar = cv2.resize(toolbar, (1280, 150))

detector = handDetector(num_hands=1)

colorBar = (255, 0, 0)
brushThickness = 15
eraserThickness = 80

ptime = 0
while(True):
    ok, img = cap.read()

    if not ok:
        break

    img = cv2.flip(img, 1)

    img = detector.findhands(img)
    lmlist = detector.findpoints(img)

    if len(lmlist) != 0:
        # Tip of index finger
        x1, y1 = lmlist[8][1], lmlist[8][2]
        # Tip of middle finger
        x2, y2 = lmlist[12][1], lmlist[12][2]

        # 1. Selection Mode: Both index and middle fingers are up
        if (lmlist[8][2] < lmlist[6][2]) and (lmlist[12][2] < lmlist[10][2]):
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), colorBar, cv2.FILLED)
            
            # Select color/tool
            new_color, new_toolbar = select_toolbar_tool(x1, y1)
            if new_color is not None:
                colorBar = new_color
                if new_toolbar is not None:
                    toolbar = new_toolbar

        # 2. Drawing Mode: Only index finger is up
        elif (lmlist[8][2] < lmlist[6][2]):
            cv2.circle(img, (x1, y1), 20, colorBar, cv2.FILLED)


    # Overlay the toolbar at the top
    if toolbar is not None:
        img[0:150, 0:1280] = toolbar

    ctime = time.time()
    fps = 1/(ctime - ptime) if (ctime - ptime) > 0 else 0
    ptime = ctime

    cv2.putText(img, f"FPS : {fps : .2f}", (40, 180), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
