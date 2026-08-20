import cv2 
import time
import numpy as np
from HandTrackingModule import handDetector
from toolbar import select_toolbar_tool, show_eraser_size_toolbar, select_eraser_size, show_brush_size_slider, select_brush_size,  clear_canvas
from shape_recognition import shape_recognition
from shape_generator import draw_perfect_shape

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

cv2.namedWindow("Virtual Whiteboard")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Creating a window with black image
canvas = np.zeros((720, 1280, 3), np.uint8)

toolbar = cv2.imread("assets/Colors.jpg")
if toolbar is not None:
    toolbar = cv2.resize(toolbar, (1280, 150))

detector = handDetector(num_hands = 1)

# ------------------------------------------------------------------
colorBar = (255, 0, 0)
brushThickness = 5
eraserThickness = 80
# ------------------------------------------------------------------

points = []
xp, yp = 0, 0

# Fist gesture hold timer tracking
fist_start_time = None
fist_cleared = False
hold_duration_threshold = 2.5  # seconds to hold fist to clear canvas

# Shape recognition state tracking variables
was_drawing = False
detected_shape = None
detected_contour = None
shape_display_expiry = 0

ptime = 0
while(True):
    is_currently_drawing = False
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
            fist_start_time = None
            fist_cleared = False

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), colorBar, cv2.FILLED)
            
            # Select color/tool
            new_color, new_toolbar, name = select_toolbar_tool(x1, y1)
            if new_color is not None:
                colorBar = new_color
                if new_toolbar is not None:
                    toolbar = new_toolbar

            # If eraser is selected, allow updating eraser thickness in selection mode
            if colorBar == (0,0,0):
                new_size = select_eraser_size(x1, y1)
                if new_size is not None:
                    eraserThickness = new_size
            else:
                new_size = select_brush_size(x1, y1)
                if new_size is not None:
                    brushThickness = new_size

        # 2. Drawing Mode: Only index finger is up
        elif (lmlist[8][2] < lmlist[6][2]):
            if colorBar != (0, 0, 0):
                is_currently_drawing = True
            fist_start_time = None
            fist_cleared = False
            cv2.circle(img, (x1, y1), 20, colorBar, cv2.FILLED)
            if(xp == 0 and yp == 0):
                xp, yp = x1, y1

            if colorBar == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), colorBar, eraserThickness)
                cv2.line(canvas, (xp, yp), (x1, y1), colorBar, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), colorBar, brushThickness)
                cv2.line(canvas, (xp, yp), (x1, y1), colorBar, brushThickness)

            xp, yp = x1, y1

        # 3. Fist Gesture: All fingers down
        elif (lmlist[8][2] > lmlist[6][2]) and (lmlist[12][2] > lmlist[10][2]) and (lmlist[16][2] > lmlist[14][2]) and (lmlist[20][2] > lmlist[18][2]):
            if not fist_cleared:
                if fist_start_time is None:
                    fist_start_time = time.time()
                
                elapsed = time.time() - fist_start_time
                remaining = max(0.0, hold_duration_threshold - elapsed)
                
                # Visual countdown indicator near the wrist landmark (lmlist[0])
                wrist_x, wrist_y = lmlist[0][1], lmlist[0][2]
                cv2.rectangle(img, (wrist_x - 110, wrist_y + 15), (wrist_x + 130, wrist_y + 55), (0, 0, 0), cv2.FILLED)
                cv2.rectangle(img, (wrist_x - 110, wrist_y + 15), (wrist_x + 130, wrist_y + 55), (0, 0, 255), 2)
                cv2.putText(img, f"Clear: {remaining:.1f}s", (wrist_x - 100, wrist_y + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                if elapsed >= hold_duration_threshold:
                    clear_canvas(canvas)
                    fist_cleared = True
                    fist_start_time = None
            else:
                # Keep displaying "Cleared!" while they continue to hold the fist
                wrist_x, wrist_y = lmlist[0][1], lmlist[0][2]
                cv2.rectangle(img, (wrist_x - 110, wrist_y + 15), (wrist_x + 130, wrist_y + 55), (0, 100, 0), cv2.FILLED)
                cv2.rectangle(img, (wrist_x - 110, wrist_y + 15), (wrist_x + 130, wrist_y + 55), (0, 255, 0), 2)
                cv2.putText(img, "Cleared!", (wrist_x - 70, wrist_y + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # 4. Other/Neutral Gesture
        else:
            fist_start_time = None
            fist_cleared = False
    else:
        # No hand detected
        fist_start_time = None
        fist_cleared = False

    # Check for transition: user stopped drawing
    if was_drawing and not is_currently_drawing:
        result = shape_recognition(canvas)
        if result is not None:
            detected_shape, detected_contour = result
            shape_display_expiry = time.time() + 3.0  # Display for 3 seconds
            # Clear the freehand stroke and replace it with a perfect shape on canvas
            clear_canvas(canvas)
            draw_perfect_shape(canvas, detected_shape, detected_contour, colorBar, brushThickness)
        else:
            detected_shape = None
            detected_contour = None
            shape_display_expiry = 0
        # Always reset points after a stroke ends so the next stroke starts fresh
        points.clear()
        xp, yp = 0, 0

    # If user starts drawing again, clear previous shape display immediately
    if is_currently_drawing:
        detected_shape = None
        detected_contour = None
        shape_display_expiry = 0

    was_drawing = is_currently_drawing



    # Overlay the toolbar at the top
    if toolbar is not None:
        img[0:150, 0:1280] = toolbar

    # Overlay the eraser size toolbar if eraser is selected
    if colorBar == (0,0,0):
        show_eraser_size_toolbar(img)
    else:
        show_brush_size_slider(img, brushThickness)

    ctime = time.time()
    fps = 1/(ctime - ptime) if (ctime - ptime) > 0 else 0
    ptime = ctime

    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 1, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)

    # Render recognized shape and name if within the display duration
    if time.time() < shape_display_expiry and detected_shape is not None:
        if detected_contour is not None:
            # Draw the perfect shape outline on the display frame as a visual highlight
            draw_perfect_shape(img, detected_shape, detected_contour, (0, 255, 0), 3)
        cv2.putText(img, f"Shape: {detected_shape}", (40, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.putText(img, f"FPS : {fps : .2f}", (40, 180), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("Virtual Whiteboard", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        filename = f"drawing_{int(time.time())}.png"
        cv2.imwrite(filename, canvas)
        print(f"Canvas saved to {filename}")

cap.release()
cv2.destroyAllWindows()
