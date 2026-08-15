import cv2

def shape_recognition(canvas, img):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(
        gray,
        50,
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

    cv2.drawContours(
    img,
    [approx],
    -1,
    (255, 0, 0),
    3
)

    corners = len(approx)
