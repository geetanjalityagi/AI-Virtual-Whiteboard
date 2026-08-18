import cv2
import numpy as np

def shape_recognition(canvas, img):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(
        gray,
        1,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(thresh,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None


    contour = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(contour,
                              0.02*perimeter,
                              True)

    corners = len(approx)

    shape_name = "Unknown"
    if corners == 3:
        shape_name = "Triangle"
    elif corners == 4:
        x, y, w, h = cv2.boundingRect(approx)
        ratio = w / float(h) if h != 0 else 0
        if 0.9 <= ratio <= 1.1:
            shape_name = "Square"
        else:
            shape_name = "Rectangle"
    else:
        if perimeter > 0:
            circularity = (4 * np.pi * area) / (perimeter * perimeter)
        else:
            circularity = 0
        if circularity > 0.60:
            shape_name = "Circle"

    if shape_name == "Unknown":
        return None

    return shape_name, approx

