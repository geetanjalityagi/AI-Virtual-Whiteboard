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
    cv2.putText(img, f"Select size", (1075, 215), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 1)
    cv2.putText(img, f"○ Small", (1075, 240), cv2.FONT_HERSHEY_PLAIN, 1.35, (255, 255, 255), 2)
    cv2.putText(img, f" Medium", (1075, 265), cv2.FONT_HERSHEY_PLAIN, 1.35, (255, 255, 255), 2)
    cv2.putText(img, f" Large", (1075, 290), cv2.FONT_HERSHEY_PLAIN, 1.35, (255, 255, 255), 2)


def select_eraser_size(x, y):
    if x > 1075:

        if 240 <= y < 265:
            return 25
        if 265 <= y < 290:
            return 50
        if 290 <= y < 310:
            return 80
