# Rubik's Cube Solver

A computer vision-based Rubik's Cube Solver that scans a physical 3×3 Rubik's Cube using a webcam, reconstructs the cube configuration digitally, computes a solution with the Kociemba algorithm, and provides a visual step-by-step solution.

<img width="907" height="499" alt="SS1" src="https://github.com/user-attachments/assets/9130d5f3-a937-435e-b170-6969052f3df9" />

---

## Features

### Cube Detection
* Detects Rubik's Cube faces using OpenCV contour detection
* Classifies sticker colors using the HSV color space

### Dual Scanning Modes
* **Track Mode**
  * Tracks the position of the cube within the live webcam feed

* **Grid Mode**
  * Uses a fixed-position grid, recommended when automatic detection is unreliable
 
You can switch between track and grid mode any time.

<img width="908" height="499" alt="SS3" src="https://github.com/user-attachments/assets/9129deea-ecbb-4b77-bb55-bb6bad0cf724" />

### Interactive Cube Editor
* Displays a full 2D cube net during scanning
* Users can manually correct incorrectly detected colors by clicking on them
* Undo functionality for rescanning faces

### Cube Solving
* Uses the Kociemba two-phase solving algorithm
* Produces near-optimal solutions

### Visual Solution Guidance
* Step-by-step solving instructions
* Dynamic arrow overlays indicating required rotations
* Support for:
  * Clockwise turns
  * Counter-clockwise turns
  * Double turns
  
<img width="905" height="499" alt="SS2" src="https://github.com/user-attachments/assets/8e234bd9-0c99-4636-8dc3-e4884f63b54a" />

---
## Tools Used
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
Cube scanning
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
RubiksCubeSolver/
├── Main.py
├── DetectFace.py
├── Solver.py
├── SolutionVisualizer.py
├── CubeVisualizer.py
├── MainHelper.py
└── README.md
```

| File | Description |
|------|-------------|
| `Main.py` | Controls application flow, GUI logic, webcam interaction, and state transitions. |
| `DetectFace.py` | Handles cube face detection and color classification. |
| `Solver.py` | Generates the solution sequence using the Kociemba algorithm. |
| `SolutionVisualizer.py` | Draws arrow overlays that guide the user through each move. |
| `CubeVisualizer.py` | Displays the interactive cube net used during scanning and editing. |
| `MainHelper.py` | Contains UI utilities, animations, and helper functions. |
---
## Installation
Clone the repository:
```bash
git clone https://github.com/Sude-Kaya/RubiksCubeSolver.git
cd RubiksCubeSolver
```
Install dependencies:
```bash
pip install opencv-python numpy matplotlib kociemba
```

❗ If installation of 'kociemba' fails on Windows, try enabling the Desktop development with C++ workload through Visual Studio Installer.

---

## Usage
Run:
```bash
python Main.py
```

### Scanning Procedure
1. Launch the application.
2. Present the requested cube face to the webcam. (**Note:** All face positions are referenced relative to the Front face of your choice.)
3. Click **SCAN FACE**.
4. Repeat until all six faces are scanned.
5. Review the generated cube net. Correct any incorrectly detected stickers by clicking on them.
6. Click **EDIT DONE**.

### Solving Procedure
1. Wait for solution generation. ❗The Front side of the cube should face your screen during the solving process.
2. Follow the visual move instructions. ❗The rotations should follow the direction of the arrows exactly as shown for a correct solution.
3. Use the buttons:
   * **NEXT MOVE**
   * **PREV MOVE**
4. Continue until the cube is solved.

Tip: Press "q" to force quit the program any time.

---

## Requirements
### Hardware
* Webcam
* 3×3 Rubik's Cube

### Recommended Environment
* Good lighting
* Plain background
* Cube is not in shadow

---

## Limitations
* Poor lighting may reduce color recognition accuracy and cube tracking performance.
* Reflective stickers may cause occasional misclassification.

---
| Platform | Status |
|----------|--------|
| Windows | ✅ Supported |
| macOS | ❌ Not Supported (requires code modifications)|
| Linux | ⚠️ Untested |

---
## Authors
💫 Team Pulsar
