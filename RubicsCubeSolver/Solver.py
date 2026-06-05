import numpy as np
import kociemba

moves_translation = {
    "U": "Rotate the top 90 degrees clockwise",
    "U'": "Rotate the top 90 degrees counter-clockwise",
    "U2": "Rotate the top 180 degrees",
    "D": "Rotate the bottom 90 degrees clockwise",
    "D'": "Rotate the bottom 90 degrees counter-clockwise",
    "D2": "Rotate the bottom 180 degrees",
    "F": "Rotate the front 90 degrees clockwise",
    "F'": "Rotate the front 90 degrees counter-clockwise",
    "F2": "Rotate the front 180 degrees",
    "B": "Rotate the back 90 degrees clockwise",
    "B'": "Rotate the back 90 degrees counter-clockwise",
    "B2": "Rotate the back 180 degrees",
    "R": "Rotate the right 90 degrees clockwise",
    "R'": "Rotate the right 90 degrees counter-clockwise",
    "R2": "Rotate the right 180 degrees",
    "L": "Rotate the left 90 degrees clockwise",
    "L'": "Rotate the left 90 degrees counter-clockwise",
    "L2": "Rotate the left 180 degrees",
}

SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"


def solve_from_colors(face_u, face_r, face_f, face_d, face_l, face_b):
    try:
       
        color_to_pos = {
            face_u[4]: 'U',
            face_r[4]: 'R',
            face_f[4]: 'F',
            face_d[4]: 'D',
            face_l[4]: 'L',
            face_b[4]: 'B',
        }

        combined_faces = np.concatenate([
            face_u, face_r, face_f,
            face_d, face_l, face_b
        ])

        if "unknown" in combined_faces:
            return ["Error: Cube not fully scanned"]

        try:
            kociemba_input = ''.join([color_to_pos[color] for color in combined_faces])
        except KeyError:
            return ["Error: Color mismatch (centers may be incorrect)"]

        
        if kociemba_input == SOLVED_STATE:
            return ["Cube is already solved"]

        raw_output = kociemba.solve(kociemba_input)
        raw_moves = raw_output.split()

        translated_moves = [
            move for move in raw_moves
        ]

        return translated_moves

    except Exception as e:
        return [f"{str(e)}"]
      