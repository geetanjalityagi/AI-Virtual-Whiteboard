import cv2
import numpy as np


def shape_recognition(canvas):
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

    if perimeter == 0 or area < 100:
        return None

    # ------------------------------------------------------------------
    # Line detection: use the minimum-area bounding rectangle.
    # A line has one dimension vastly larger than the other.
    # approxPolyDP almost never returns exactly 2 corners for a
    # hand-drawn stroke, so we rely on elongation ratio instead.
    # ------------------------------------------------------------------
    rect = cv2.minAreaRect(contour)          # ((cx,cy), (w,h), angle)
    rw, rh = rect[1]
    if rw == 0 or rh == 0:
        return None

    long_side  = max(rw, rh)
    short_side = min(rw, rh)
    elongation = long_side / short_side

    # Elongation > 5 means the stroke is at least 5× longer than it is wide
    if elongation > 5.0:
        # Compute the two endpoints of the line from the rotated bounding box
        box = cv2.boxPoints(rect)             # 4 corners of the rotated rect
        box = np.int32(box)
        # The "start" and "end" are the midpoints of the two short edges
        # Sort corners by x so we get consistent left/right ordering
        box_sorted = box[np.argsort(box[:, 0])]
        # Left midpoint (average of the 2 leftmost corners)
        pt1 = tuple(np.mean(box_sorted[:2], axis=0).astype(int))
        # Right midpoint (average of the 2 rightmost corners)
        pt2 = tuple(np.mean(box_sorted[2:], axis=0).astype(int))
        # Store endpoints as a 2-point contour so draw_perfect_shape can use it
        line_contour = np.array([[pt1], [pt2]], dtype=np.int32)
        return "Line", line_contour

    # ------------------------------------------------------------------
    # Polygon / circle detection via approxPolyDP
    # ------------------------------------------------------------------
    approx = cv2.approxPolyDP(contour,
                              0.03 * perimeter,
                              True)

    corners = len(approx)

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
        circularity = (4 * np.pi * area) / (perimeter * perimeter)
        shape_name = "Circle" if circularity > 0.60 else "Unknown"

    if shape_name == "Unknown":
        return None

    return shape_name, approx
