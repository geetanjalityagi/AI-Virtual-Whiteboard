import cv2

TOOLS = [
    {"name": "Red_Color",    "x1":240,  "x2":360,  "color":(0,0,255)},
    {"name": "Purple_Color", "x1":360,  "x2":480,  "color":(255,105,180)},
    {"name": "Green_Color",  "x1":480,  "x2":600,  "color":(0,255,0)},
    {"name": "Blue_Color",   "x1":600,  "x2":720,  "color":(255,0,0)},
    {"name": "Orange_Color", "x1":720,  "x2":840,  "color":(0,165,255)},
    {"name": "Pink_Color",   "x1":840,  "x2":960, "color":(255,0,255)},
    {"name": "Eraser",       "x1":1000, "x2":1280, "color":(0,0,0)}
]

def select_toolbar_tool(x, y):

    if y < 150:

        for tool in TOOLS:
            if tool["x1"] < x < tool["x2"]:
                name = tool["name"]
                toolbar = cv2.imread(f"assets/{name}.jpg")
                if toolbar is not None:
                    toolbar = cv2.resize(toolbar, (1280, 150))
                return tool["color"], toolbar, name

    return None, None, None

def show_eraser_size_toolbar(img):
    cv2.rectangle(img, (1060, 180), (1200, 310), (255, 123, 255), 2)
    cv2.putText(img, f"Eraser size", (1075, 215), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 1)
    cv2.circle(img, (1085, 233), 3, (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Small", (1105, 240), cv2.FONT_HERSHEY_PLAIN, 1.35, (255, 255, 255), 2)
    cv2.circle(img, (1085, 258), 6, (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Medium", (1105, 265), cv2.FONT_HERSHEY_PLAIN, 1.35, (255, 255, 255), 2)
    cv2.circle(img, (1085, 283), 9, (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Large", (1105, 290), cv2.FONT_HERSHEY_PLAIN, 1.35, (255, 255, 255), 2)


def select_eraser_size(x, y):
    if x > 1075:

        if 240 <= y < 265:
            return 25
        if 265 <= y < 290:
            return 50
        if 290 <= y < 310:
            return 80


def show_brush_size_slider(img, brushThickness):
    # Draw slider box background or border (450 to 810 horizontally, 160 to 210 vertically)
    cv2.rectangle(img, (450, 160), (810, 210), (255, 123, 255), 2)
    cv2.putText(img, f"Brush Size: {brushThickness}", (460, 192), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 255), 1)
    
    # Draw slider track line (length 130: from x=620 to x=750)
    cv2.line(img, (620, 185), (750, 185), (255, 255, 255), 3)
    
    # Draw current size cursor
    x_pos = int(620 + (brushThickness - 5) * (130 / 45))
    cv2.circle(img, (x_pos, 185), 8, (0, 0, 255), cv2.FILLED)
    
    # Draw a visual size preview indicator
    cv2.circle(img, (785, 185), max(2, brushThickness // 2), (255, 255, 255), cv2.FILLED)


def select_brush_size(x, y):
    if 620 <= x <= 750 and 160 <= y <= 210:
        thickness = int(5 + (x - 620) * (45 / 130))
        return max(5, min(50, thickness))
    return None


