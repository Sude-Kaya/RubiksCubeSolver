import matplotlib
import cv2 as cv
import numpy as np
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches


COLORS = {
    'W': '#FFFFFF', 'Y': '#FEFE33', 'R': '#EE0000',
    'O': '#FF5900', 'G': '#009B48', 'B': '#0000FF',
    'unknown': '#A0A0A0'
}


FACE_POSITIONS = [(3, 3), (0,3), (9, 3), (6, 3), (3, 6), (3,0)]
FACE_NAMES = ["FRONT", "RIGHT" "BACK", "LEFT", "UP", "DOWN"]

def setup_screen():
    """Initializes the interactive Matplotlib window."""
    fig, ax = plt.subplots(figsize=(6,4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.set_facecolor('#F0F0F0')
    plt.axis('off')
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    plt.subplots_adjust(
        left=0,
        right=1,
        top=1,
        bottom=0
    )
    return fig, ax

def draw_face(ax, face_data, face_index):
    """Draws a single face onto the existing grid."""
    if face_index < 0 or face_index >= 6:
        return

    base_x, base_y = FACE_POSITIONS[face_index]
    
    for i in range(9):
        row, col = i // 3, i % 3
       
        color_letter = face_data[i]
        
        if color_letter in COLORS:
            x, y = base_x + col, base_y + (2 - row)
            rect = patches.Rectangle(
                (x, y), 0.95, 0.95, 
                linewidth=2, edgecolor='black',
                facecolor=COLORS[color_letter]
            )
            ax.add_patch(rect)

def render_Cube_Net(fig, blank):
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    img = cv.resize(img, (500, 400))

    overlay = img[:, :, :3]
    overlay = cv.cvtColor(overlay, cv.COLOR_RGB2BGR)
    alpha = img[:, :, 3] / 255.0

    y1, y2 = 120, 520
    x1, x2 = 680, 1180

    region = blank[y1:y2, x1:x2]

    for c in range(3):
        region[:, :, c] = (
            alpha * overlay[:, :, c] +
            (1 - alpha) * region[:, :, c]
        )
    blank[y1:y2, x1:x2] = region
