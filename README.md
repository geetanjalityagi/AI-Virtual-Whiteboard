# AI Virtual Whiteboard

An interactive, touchless virtual whiteboard application built using Python, OpenCV, and Mediapipe. Draw, erase, select colors, and change brush sizes directly in the air using hand gestures tracked in real-time by your webcam.

---

## Features

- **Real-Time Hand Tracking**: Fast, low-latency hand landmark detection using Google's Mediapipe.
- **Dual Modes**:
  - **Selection Mode** (Index + Middle finger raised): Hover to pick colors, select eraser sizes, or adjust brush thickness.
  - **Drawing Mode** (Only Index finger raised): Draw freehand lines on the screen using the selected color and thickness.
- **Diverse Paint Palette**: Pick Red, Purple, Green, Blue, Orange, and Pink directly from the top toolbar.
- **Interactive Hand-Controlled Slider**: Adjust the brush thickness dynamically using a virtual horizontal slider on the screen (no mouse required).
- **Eraser with Adjustable Thickness**: Quick size presets (Small, Medium, Large) for precision erasing.
- **FPS Counter**: On-screen real-time performance display.

---

## Project Structure

- **[VisionBoard.py](file:///c:/Projects/AI_Virtual_WhiteBoard/VisionBoard.py)**: The main entry point script. Manages camera ingestion, mode switching, UI rendering, canvas overlaying, and the main event loop.
- **[toolbar.py](file:///c:/Projects/AI_Virtual_WhiteBoard/toolbar.py)**: UI definition module containing bounds checking and drawer methods for toolbar tools, the eraser size selection panel, and the horizontal brush thickness slider.
- **[HandTrackingModule.py](file:///c:/Projects/AI_Virtual_WhiteBoard/HandTrackingModule.py)**: MediaPipe abstraction wrapper. Detects hands and processes tracking points into pixel coordinate arrays.
- **[assets/](file:///c:/Projects/AI_Virtual_WhiteBoard/assets)**: Images used for the top toolbar states (e.g., individual highlighted color assets).

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

### 1. Mode Selection
- **Selection Mode**: Raise both your **Index Finger** and **Middle Finger**. In this mode, no lines are drawn, and you can point to select tools or adjust sliders.
- **Drawing Mode**: Raise **only your Index Finger** (curl the middle finger down). This draws lines with the selected color and thickness.

| Gestures | Mode | Description |
| :---: | :---: | :---: |
| ✌️ (Two fingers up) | **Selection Mode** | Select colors, change brush/eraser sizes. |
| ☝️ (One finger up) | **Drawing Mode** | Write/draw on the digital canvas. |

### 2. Toolbar Operations (Selection Mode)
- **Select Color**: Hover your fingers over the color slots at the top toolbar to switch drawing colors.
- **Eraser**: Hover over the Eraser tool at the top-right slot. Once selected:
  - An **Eraser size menu** appears on the right side. Hover over "Small", "Medium", or "Large" to change eraser thickness.
- **Adjust Brush Size**: When a drawing color is active:
  - A **Brush Size slider panel** appears horizontally below the toolbar. 
  - Drag your index finger horizontally along the track line (from left to right) to adjust the brush size (from `5` to `50` px). A dynamic preview circle displays the active size.
