import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def draw_animated_cube(matrix):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_facecolor('#121212')
    colors = {
        'W': '#FFFFFF',
        'Y': '#FEFE33',
        'R': '#EE0000',
        'O': '#FF5900',
        'G': '#009B48',
        'B': '#0000FF'
    }
    face_positions = [(3, 6), (3, 0), (3, 3), (9, 3), (0, 3), (6, 3)]

    def init():
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 9)
        ax.set_aspect('equal')
        plt.axis('off') 
        return []
    def update(face_index):
        face_data = matrix[face_index]
        base_x, base_y = face_positions[face_index]
        for i in range(9):
            row = i // 3
            col = i % 3
            color_letter = face_data[i]

            if color_letter in colors:
                x = base_x + col
                y = base_y + (2 - row) 

                square = patches.Rectangle(  
                    (x, y), 1, 1, 
                    linewidth=1.5,
                    edgecolor='black',
                    facecolor=colors[color_letter]
                )
                ax.add_patch(square)

        plt.title(f"Face {face_index + 1} being placed...", color='black', fontsize=10)
        return []
    animation = FuncAnimation(
        fig,
        update,
        frames=range(6), 
        init_func=init,
        interval=2000,
        repeat=False
    )
    plt.show()
data = [
    ['R', 'W', 'G', 'B', 'Y', 'O', 'W', 'R', 'G'],  
    ['Y', 'B', 'O', 'R', 'G', 'W', 'Y', 'B', 'O'],  
    ['G', 'Y', 'R', 'W', 'B', 'O', 'G', 'Y', 'R'], 
    ['B', 'R', 'O', 'G', 'W', 'Y', 'B', 'R', 'O'],  
    ['O', 'W', 'B', 'R', 'G', 'Y', 'O', 'W', 'B'], 
    ['W', 'G', 'R', 'B', 'O', 'Y', 'W', 'G', 'R']   
]
draw_animated_cube(data)