# AI Virtual Whiteboard

An interactive, touchless virtual whiteboard application built using Python, OpenCV, and Mediapipe. Draw, erase, select colors, adjust brush sizes, and automatically snap freehand shapes into perfect geometry — all in real-time using hand gestures tracked by your webcam.

---

## Features

- **Real-Time Hand Tracking**: Fast, low-latency hand landmark detection using Google's Mediapipe.
- **Dual Interaction Modes**:
  - **Selection Mode** (Index + Middle finger raised): Hover to pick colors, adjust brush/eraser size.
  - **Drawing Mode** (Only Index finger raised): Draw freehand strokes on the canvas.
- **Automatic Shape Recognition & Correction**: When you stop drawing, the app analyzes your stroke and automatically replaces it with a perfect geometric shape:
  - **Triangle** (3 corners detected)
  - **Square** (4 corners, aspect ratio ~1:1)
  - **Rectangle** (4 corners, non-square)
  - **Circle** (high circularity score > 0.60)
- **Diverse Color Palette**: Red, Purple, Green, Blue, Orange, and Pink — selectable from the top toolbar.
- **Interactive Brush Size Slider**: Adjust brush thickness (5–50 px) via a virtual horizontal slider (no mouse needed).
- **Eraser with Adjustable Thickness**: Three quick size presets — Small, Medium, Large.
- **Clear Canvas (Fist Gesture with Hold Timer)**: Hold a fist for 2.5 seconds to wipe the canvas. A visual countdown prevents accidental clears.
- **FPS Counter**: On-screen real-time performance display.

---

## Project Structure

```
AI_Virtual_WhiteBoard/
├── VisionBoard.py          # Main entry point: camera loop, gesture handling, canvas overlay
├── HandTrackingModule.py   # Mediapipe wrapper: hand detection & landmark extraction
├── shape_recognition.py    # Contour analysis: identifies Triangle, Square, Rectangle, Circle
├── shape_generator.py      # Geometric drawing: renders perfect shapes onto a frame
├── toolbar.py              # UI module: color toolbar, brush slider, eraser size panel
├── assets/                 # Toolbar state images (per-color highlighted JPGs)
└── requirements.txt        # Python package dependencies
```

### Module Responsibilities

| File | Role |
|---|---|
| [`VisionBoard.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/VisionBoard.py) | Main loop — reads webcam, detects gestures, triggers shape recognition, composites canvas onto camera feed |
| [`HandTrackingModule.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/HandTrackingModule.py) | `handDetector` class — wraps Mediapipe Hands, returns 21 landmark `(id, x, y)` pixel coordinates |
| [`shape_recognition.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/shape_recognition.py) | `shape_recognition(canvas, img)` — finds the largest contour, uses `approxPolyDP` + circularity to classify shape |
| [`shape_generator.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/shape_generator.py) | `draw_perfect_shape(img, shape, contour, color, thickness)` — draws a clean geometric primitive from contour data |
| [`toolbar.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/toolbar.py) | Color tool selection, eraser size panel, brush size slider, canvas clear utility |

---

## Shape Recognition Pipeline

When the user stops drawing (index finger lifted), the following pipeline runs automatically:

```
Canvas → Grayscale → Binary Threshold → findContours
    → Largest Contour → approxPolyDP
        → corners == 3              →  Triangle
        → corners == 4
            → aspect ratio ≈1.0     →  Square
            → aspect ratio ≠1.0     →  Rectangle
        → circularity > 0.60        →  Circle
    → draw_perfect_shape() replaces freehand stroke on canvas
    → Green outline + shape label displayed for 3 seconds
```

**Circularity formula** used for circle detection:

```
circularity = (4 × π × area) / (perimeter²)
```

A value > 0.60 is classified as a Circle.

---

## Installation & Setup

### Prerequisites
- Python 3.8 or above
- A functional webcam

### 1. Clone/Open the Workspace
Open your terminal in the root project directory `c:/Projects/AI_Virtual_WhiteBoard`.

### 2. Set Up a Virtual Environment (Optional but Recommended)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install the required packages using `pip`:
```powershell
pip install opencv-python mediapipe numpy
```

---

## How to Run

Launch the application using Python:
```powershell
python VisionBoard.py
```

Press **`q`** on your keyboard while focusing the whiteboard window to exit the application.

---

## Controls & Gestures

| Gesture | Mode | Action |
|:---:|:---:|---|
| ✌️ Two fingers up | **Selection Mode** | Hover to select colors, adjust brush/eraser size |
| ☝️ One finger up | **Drawing Mode** | Draw freehand strokes on the canvas |
| ✊ Fist (hold 2.5s) | **Clear Canvas** | Wipes the entire canvas after countdown |

### Toolbar Operations (Selection Mode Only)

- **Select Color**: Hover over any color slot in the top toolbar (Red, Purple, Green, Blue, Orange, Pink).
- **Eraser**: Hover over the Eraser slot (far right). An **Eraser Size** panel appears — hover over Small / Medium / Large.
- **Brush Size Slider**: When a color is active, a horizontal slider panel appears below the toolbar. Move your index finger left/right along the track (x: 620–750) to set brush thickness from `5` to `50` px. A live preview circle shows the current size.
- **Clear Canvas**: Make a fist and hold for **2.5 seconds**. A countdown (e.g. `Clear: 2.1s`) appears near your wrist. On completion, a green `Cleared!` badge confirms the action.

### Shape Auto-Correction (Automatic)

After finishing a freehand stroke (lifting your index finger), the app:
1. Runs `shape_recognition()` on the canvas.
2. If a known shape is detected, **clears the rough stroke** and redraws a **perfect geometric shape** in your current color and brush thickness using `draw_perfect_shape()`.
3. Displays a **green highlight outline** and shape label (e.g., `Shape: Circle`) for 3 seconds.

Supported auto-corrected shapes: **Triangle**, **Square**, **Rectangle**, **Circle**.

---

## Key Dependencies

| Package | Version | Purpose |
|---|---|---|
| `opencv-python` | 5.0.0+ | Camera capture, drawing, image processing |
| `mediapipe` | 0.10.14 | Real-time hand landmark detection |
| `numpy` | 2.5+ | Contour math, canvas array operations |
