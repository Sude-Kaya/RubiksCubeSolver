import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches


COLORS = {
    'W': '#FFFFFF', 'Y': '#FEFE33', 'R': '#EE0000',
    'O': '#FF5900', 'G': '#009B48', 'B': '#0000FF',
    'unknown': '#A0A0A0'
}


FACE_POSITIONS = [(3, 3), (3, 6), (0, 3), (6, 3), (3, 0), (9, 3)]
FACE_NAMES = ["FRONT", "UP", "LEFT", "RIGHT", "DOWN", "BACK"]

def setup_screen():
    """Initializes the interactive Matplotlib window."""
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.set_facecolor('#F0F0F0')
    plt.axis('off')
    plt.show()
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
    
    plt.title(f"Last Scanned: {FACE_NAMES[face_index]}", fontweight='bold')
    ax.figure.canvas.draw_idle()   
    ax.figure.canvas.flush_events() 
    plt.pause(0.01)
