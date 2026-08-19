import cv2
import numpy as np


def draw_perfect_shape(img, shape, contour, color, thickness, points=None):
    """Draw a geometrically perfect version of the recognised shape onto img."""

    if shape == "Line":
        # contour is a 2-point array [[pt1], [pt2]] produced by shape_recognition
        pt1 = tuple(contour[0][0])
        pt2 = tuple(contour[1][0])
        cv2.line(img, pt1, pt2, color, thickness)

    elif shape == "Rectangle" or shape == "Square":
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

    elif shape == "Triangle":
        cv2.polylines(img, [contour], True, color, thickness)

    elif shape == "Circle":
        (x, y), radius = cv2.minEnclosingCircle(contour)
        cv2.circle(img, (int(x), int(y)), int(radius), color, thickness)