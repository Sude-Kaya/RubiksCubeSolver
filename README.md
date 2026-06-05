# Rubik's Cube Solver

A computer vision-based Rubik's Cube Solver that scans a physical 3×3 Rubik's Cube using a webcam, reconstructs the cube state, computes a solution using the Kociemba algorithm, and provides a visual step-by-step solution.

<img width="907" height="499" alt="SS1" src="https://github.com/user-attachments/assets/9130d5f3-a937-435e-b170-6969052f3df9" />

---

## Features

### Computer Vision Cube Detection

* Detects Rubik's Cube faces using OpenCV contour detection
* Supports automatic face tracking
* Detects 3×3 cube grids in real time


### Color Recognition

* HSV color-space based color classification
* Supports:

  * White
  * Yellow
  * Red
  * Orange
  * Blue
  * Green

### Dual Scanning Modes

* **Track Mode**

  * Automatically detects cube stickers using contour analysis
* **Grid Mode**

  * Uses a fixed scanning grid for environments where automatic detection is difficult

<img width="908" height="499" alt="SS3" src="https://github.com/user-attachments/assets/9129deea-ecbb-4b77-bb55-bb6bad0cf724" />


### Interactive Cube Editor

* Displays a full 2D cube net during scanning
* Users can manually correct incorrectly detected colors
* Undo functionality for rescanning faces

### Cube Solving

* Uses the Kociemba two-phase solving algorithm
* Produces near-optimal solutions
* Handles invalid and incomplete cube states

### Visual Solution Guidance

* Step-by-step solving instructions
* Dynamic arrow overlays indicating required rotations
* Support for:

  * Clockwise turns
  * Counter-clockwise turns
  * Double turns
  
<img width="905" height="499" alt="SS2" src="https://github.com/user-attachments/assets/8e234bd9-0c99-4636-8dc3-e4884f63b54a" />

### User-Friendly Interface

* Live webcam feed
* Interactive buttons
* Real-time feedback during scanning and solving
* Completion screen with animation


---

## Technologies Used

* Python 3.7+
* OpenCV
* NumPy
* Matplotlib
* Kociemba

---

## System Architecture

```
Webcam Input
      ↓
Cube Detection
      ↓
Color Recognition
      ↓
Cube State Construction
      ↓
Manual Verification / Editing
      ↓
Kociemba Solver
      ↓
Solution Visualization
      ↓
User Solves Cube
```

---

## Project Structure

```
.
├── Main.py
├── DetectFace.py
├── Solver.py
├── SolutionVisualizer.py
├── CubeVisualizer.py
├── MainHelper.py
└── README.md
```

### Main.py

Controls application flow, GUI logic, webcam interaction, and state transitions.

### DetectFace.py

Handles:

* Cube face detection
* Contour processing
* Sticker extraction
* HSV color classification

### Solver.py

Converts detected colors into Kociemba notation and generates the solution sequence.

### SolutionVisualizer.py

Draws directional overlays that show users how to perform each move.

### CubeVisualizer.py

Displays the interactive cube net used during scanning and editing.

### MainHelper.py

Contains UI utilities, animations, and helper functions.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/rubiks-cube-solver.git
cd rubiks-cube-solver
```

Install dependencies:

```bash
pip install opencv-python numpy matplotlib kociemba
```

---

## Usage

Run:

```bash
python Main.py
```

### Scanning Procedure

1. Launch the application.
2. Present the requested cube face to the webcam.
3. Click **SCAN FACE**.
4. Repeat until all six faces are scanned.
5. Review the generated cube net.
6. Correct any incorrectly detected stickers by clicking on them.
7. Click **EDIT DONE**.

### Solving Procedure

1. Wait for solution generation.
2. Follow the visual move instructions.
3. Use:
   * **NEXT MOVE**
   * **PREV MOVE**
4. Continue until the cube is solved.

---

## Requirements

### Hardware

* Webcam
* 3×3 Rubik's Cube

### Recommended Environment

* Good lighting
* Plain background
* Stable camera positioning

---

## Limitations

* Poor lighting may reduce color recognition accuracy and cube tracking.
* Webcam quality directly affects detection performance.
* Reflective stickers may cause occasional misclassification.

---

## Authors

Developed as part of an Advanced Programming course project.

💫 Team Pulsar
