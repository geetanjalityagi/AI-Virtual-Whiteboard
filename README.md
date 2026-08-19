# AI Virtual Whiteboard

An interactive, touchless virtual whiteboard built with **Python**, **OpenCV**, and **Mediapipe**. Draw freehand strokes in the air with your index finger, and the app automatically snaps them into perfect geometric shapes — all in real-time using your webcam and hand gesture recognition.

---

## Features

- **Real-Time Hand Tracking** — Low-latency 21-landmark detection via Google Mediapipe Hands.
- **Dual Interaction Modes**
  - **Selection Mode** (Index + Middle finger raised) — Hover to pick colors, adjust brush/eraser size.
  - **Drawing Mode** (Index finger only) — Draw freehand strokes on the canvas.
- **Automatic Shape Recognition & Snap-to-Perfect**  
  When you lift your finger after drawing, the stroke is analyzed and replaced with a clean geometric primitive:
  - **Line** — detected via bounding-box elongation ratio (`long ÷ short > 5`)
  - **Triangle** — 3-corner polygon (approxPolyDP)
  - **Square** — 4-corner polygon with aspect ratio ≈ 1.0
  - **Rectangle** — 4-corner polygon with non-square aspect ratio
  - **Circle** — high circularity score > 0.60
- **6-Color Palette** — Red, Purple, Green, Blue, Orange, Pink, selectable from the top toolbar.
- **Brush Size Slider** — Adjustable from 5 px to 50 px via a virtual horizontal slider (no mouse needed).
- **Eraser with 3 Size Presets** — Small (25 px), Medium (50 px), Large (80 px).
- **Fist-Hold Clear Canvas** — Hold a fist for **2.5 seconds** to wipe the canvas with a live countdown timer.
- **Green Shape Highlight** — After snap-to-shape, the perfect outline is shown in green with a label for 3 seconds.
- **FPS Counter** — On-screen real-time performance display.

---

## Project Structure

```
AI_Virtual_WhiteBoard/
├── VisionBoard.py          # Main entry point: camera loop, gesture dispatch, canvas overlay
├── HandTrackingModule.py   # Mediapipe wrapper: hand detection & 21-landmark extraction
├── shape_recognition.py    # Contour analysis: classifies Line, Triangle, Square, Rectangle, Circle
├── shape_generator.py      # Geometric renderer: draws perfect primitives from contour data
├── toolbar.py              # UI module: color toolbar, brush slider, eraser size panel
├── assets/                 # Per-color highlighted toolbar JPGs (e.g. Red_Color.jpg)
└── requirements.txt        # Pinned Python package dependencies
```

### Module Responsibilities

| File | Key Function / Class | Role |
|---|---|---|
| [`VisionBoard.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/VisionBoard.py) | Main loop | Reads webcam, dispatches gestures, triggers shape recognition, composites canvas onto camera feed |
| [`HandTrackingModule.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/HandTrackingModule.py) | `handDetector` | Wraps Mediapipe Hands; `findpoints()` returns list of `[id, x_px, y_px]` for all 21 landmarks |
| [`shape_recognition.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/shape_recognition.py) | `shape_recognition(canvas)` | Finds largest contour, runs elongation test for lines, then approxPolyDP + circularity for polygons/circles |
| [`shape_generator.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/shape_generator.py) | `draw_perfect_shape(img, shape, contour, color, thickness)` | Draws a clean cv2 primitive (line, rectangle, polyline, circle) onto the target frame |
| [`toolbar.py`](file:///c:/Projects/AI_Virtual_WhiteBoard/toolbar.py) | `select_toolbar_tool`, `show_brush_size_slider`, etc. | Color/tool selection, eraser size panel, brush size slider, canvas clear utility |

---

## Shape Recognition Pipeline

When the user lifts their index finger (stroke ends), the following pipeline runs automatically:

```
Canvas frame
  └─► Grayscale → Binary Threshold (threshold = 1)
        └─► findContours (RETR_EXTERNAL)
              └─► Largest contour by area
                    ├─► minAreaRect → elongation = long_side / short_side
                    │     └─► elongation > 5.0  ──────────────────► LINE
                    │           (endpoints extracted from rotated bbox)
                    └─► approxPolyDP (epsilon = 0.03 × perimeter)
                          ├─► corners == 3  ────────────────────────► TRIANGLE
                          ├─► corners == 4
                          │     ├─► aspect ratio 0.9–1.1  ──────────► SQUARE
                          │     └─► aspect ratio outside   ──────────► RECTANGLE
                          └─► else: circularity = 4π·area / perimeter²
                                └─► circularity > 0.60  ─────────────► CIRCLE
  └─► draw_perfect_shape() replaces freehand stroke on canvas
  └─► Green outline + shape label displayed for 3 seconds
```

### Detection Formulas

| Shape | Method | Threshold |
|---|---|---|
| Line | `minAreaRect` elongation = `long_side / short_side` | `> 5.0` |
| Triangle | `approxPolyDP` corner count | `== 3` |
| Square | `approxPolyDP` corner count + bounding rect aspect ratio `w/h` | `== 4` and `0.9 ≤ ratio ≤ 1.1` |
| Rectangle | `approxPolyDP` corner count + aspect ratio outside square range | `== 4` and ratio outside `0.9–1.1` |
| Circle | Circularity = `(4 × π × area) / perimeter²` | `> 0.60` |

---

## Installation & Setup

### Prerequisites
- Python **3.8** or above
- A functional webcam

### 1. Clone / Open the Workspace
```powershell
cd c:\Projects\AI_Virtual_WhiteBoard
```

### 2. Set Up a Virtual Environment (Recommended)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

Or install the core packages directly:
```powershell
pip install opencv-python mediapipe numpy
```

---

## How to Run

```powershell
python VisionBoard.py
```

Press **`q`** while the whiteboard window is focused to exit.

> **Webcam note**: The app opens camera index `1` by default (`cv2.VideoCapture(1)`).  
> If your webcam is not detected, change `1` to `0` on line 9 of `VisionBoard.py`.

---

## Controls & Gestures

| Gesture | Mode | Action |
|:---:|:---:|---|
| ✌️ Two fingers up (index + middle) | **Selection Mode** | Hover over toolbar to select color or tool |
| ☝️ One finger up (index only) | **Drawing Mode** | Draw freehand strokes on the canvas |
| ✊ Fist — hold 2.5 s | **Clear Canvas** | Wipes the canvas after a countdown; green "Cleared!" badge confirms |

### Toolbar Layout (top 150 px of the window)

| Slot | X Range | Tool |
|---|---|---|
| Red | 240 – 360 px | Red color brush |
| Purple | 360 – 480 px | Purple color brush |
| Green | 480 – 600 px | Green color brush |
| Blue | 600 – 720 px | Blue color brush |
| Orange | 720 – 840 px | Orange color brush |
| Pink | 840 – 960 px | Pink color brush |
| Eraser | 1000 – 1280 px | Eraser (black, variable thickness) |

### Brush Size Slider (Selection Mode, color active)

A horizontal panel appears below the toolbar. Hover your index finger in the region **x: 620–750, y: 160–210** to set brush thickness:
- Left end (x ≈ 620) → **5 px** minimum
- Right end (x ≈ 750) → **50 px** maximum
- A live preview circle shows the current size at the right of the slider.

### Eraser Size Panel (Selection Mode, eraser active)

A floating panel appears in the top-right corner. Hover your finger in:

| Zone | Y Range | Eraser Thickness |
|---|---|---|
| Small | 240 – 265 px | 25 px |
| Medium | 265 – 290 px | 50 px |
| Large | 290 – 310 px | 80 px |

### Shape Auto-Correction (Automatic)

After finishing a freehand stroke (lifting your index finger), the app:

1. Runs `shape_recognition()` on the canvas.
2. If a known shape is detected:
   - **Clears** the rough freehand stroke from the canvas.
   - **Redraws** a perfect geometric shape (`draw_perfect_shape()`) in your current color and brush thickness.
3. Displays a **green highlight outline** and shape label (e.g., `Shape: Line`) for **3 seconds**.

Supported auto-corrected shapes: **Line**, **Triangle**, **Square**, **Rectangle**, **Circle**.

---

## Key Dependencies

| Package | Version | Purpose |
|---|---|---|
| `opencv-python` | 5.0.0.93 | Camera capture, contour analysis, all drawing primitives |
| `mediapipe` | 0.10.14 | Real-time hand landmark detection (21 points) |
| `numpy` | 2.5.1 | Array math for contour geometry and canvas operations |

---

## Architecture Overview

```
Webcam Frame
    │
    ▼
handDetector.findhands()       ← Mediapipe: draws skeleton on frame
handDetector.findpoints()      ← Returns lmlist[0..20] = [id, x_px, y_px]
    │
    ├─ Selection Mode (lm8 & lm12 up)
    │       select_toolbar_tool()   ← updates colorBar, toolbar image
    │       select_brush_size()     ← updates brushThickness
    │       select_eraser_size()    ← updates eraserThickness
    │
    ├─ Drawing Mode (lm8 up only)
    │       cv2.line(canvas, prev, curr)   ← freehand stroke accumulates
    │
    ├─ Fist Gesture (all fingers down)
    │       countdown timer → clear_canvas()
    │
    └─ Stroke-end transition (was_drawing → not drawing)
            shape_recognition(canvas)
                ├─ Line       → draw_perfect_shape("Line",   line_contour)
                ├─ Triangle   → draw_perfect_shape("Triangle", approx)
                ├─ Square     → draw_perfect_shape("Square",   approx)
                ├─ Rectangle  → draw_perfect_shape("Rectangle", approx)
                └─ Circle     → draw_perfect_shape("Circle",   approx)
    │
    ▼
Canvas composited onto webcam feed → cv2.imshow("Virtual Whiteboard")
```
