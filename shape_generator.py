import cv2

def draw_perfect_shape(img, shape, contour, color, thickness):

    if shape == "Rectangle":

        x, y, w, h = cv2.boundingRect(contour)

        cv2.rectangle(img, (x,y), (x+w, y+h), color, thickness)

    elif shape == "Triangle":

        cv2.polylines(img, [contour], True, color, thickness)

    elif shape == "Circle":

        (x, y), radius = cv2.minEnclosingCircle(contour)

        cv2.circle(img, (int(x), int(y)), int(radius), color, thickness)