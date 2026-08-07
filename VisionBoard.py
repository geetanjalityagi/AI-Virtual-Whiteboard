import cv2 
import time
import numpy as np
from HandTrackingModule import handDetector
from toolbar import select_toolbar_tool, show_eraser_size_toolbar, select_eraser_size


cap = cv2.VideoCapture(1)
cv2.namedWindow("Virtual Whiteboard")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

imgcanvas = np.zeros((720, 1280, 3), np.uint8)

toolbar = cv2.imread("assets/Colors.jpg")
if toolbar is not None:
    toolbar = cv2.resize(toolbar, (1280, 150))

detector = handDetector(num_hands = 1)

# ------------------------------------------------------------------
colorBar = (255, 0, 0)
brushThickness = 15
eraserThickness = 80
# ------------------------------------------------------------------


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
            xp, yp = 0, 0

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), colorBar, cv2.FILLED)
            
            # Select color/tool
            new_color, new_toolbar, name = select_toolbar_tool(x1, y1)
            if new_color is not None:
                colorBar = new_color
                if new_toolbar is not None:
                    toolbar = new_toolbar

            # If eraser is selected, allow updating eraser thickness in selection mode
            if colorBar == (0, 0, 0):
                new_size = select_eraser_size(x1, y1)
                if new_size is not None:
                    eraserThickness = new_size
                        

        # 2. Drawing Mode: Only index finger is up
        elif (lmlist[8][2] < lmlist[6][2]):
            cv2.circle(img, (x1, y1), 20, colorBar, cv2.FILLED)
            if(xp == 0 and yp == 0):
                xp, yp = x1, y1

            if colorBar == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), colorBar, eraserThickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), colorBar, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), colorBar, brushThickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), colorBar, brushThickness)

            xp, yp = x1, y1


    # Overlay the toolbar at the top
    if toolbar is not None:
        img[0:150, 0:1280] = toolbar

    # Overlay the eraser size toolbar if eraser is selected
    if colorBar == (0, 0, 0):
        show_eraser_size_toolbar(img)

    ctime = time.time()
    fps = 1/(ctime - ptime) if (ctime - ptime) > 0 else 0
    ptime = ctime

    imgGray = cv2.cvtColor(imgcanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgcanvas)


    cv2.putText(img, f"FPS : {fps : .2f}", (40, 180), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
