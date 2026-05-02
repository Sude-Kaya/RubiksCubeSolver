import numpy as np
import kociemba

moves_translation = {
    "U": "Rotate UP face 90 degrees clockwise",
    "U'": "Rotate UP face 90 degrees counter-clockwise",
    "U2": "Rotate UP face 180 degrees",
    "D": "Rotate DOWN face 90 degrees clockwise",
    "D'": "Rotate DOWN face 90 degrees counter-clockwise",
    "D2": "Rotate DOWN face 180 degrees",
    "F": "Rotate FRONT face 90 degrees clockwise",
    "F'": "Rotate FRONT face 90 degrees counter-clockwise",
    "F2": "Rotate FRONT face 180 degrees",
    "B": "Rotate BACK face 90 degrees clockwise",
    "B'": "Rotate BACK face 90 degrees counter-clockwise",
    "B2": "Rotate BACK face 180 degrees",
    "R": "Rotate RIGHT face 90 degrees clockwise",
    "R'": "Rotate RIGHT face 90 degrees counter-clockwise",
    "R2": "Rotate RIGHT face 180 degrees",
    "L": "Rotate LEFT face 90 degrees clockwise",
    "L'": "Rotate LEFT face 90 degrees counter-clockwise",
    "L2": "Rotate LEFT face 180 degrees",
}

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

        combined_faces = np.concatenate([face_u, face_r, face_f, face_d, face_l, face_b])

        if "unknown" in combined_faces:
            return ["Error: Cube not fully scanned"]

        kociemba_input = ''.join([ color_to_pos[color] for color in combined_faces ])

        raw_output = kociemba.solve(kociemba_input)
        raw_moves = raw_output.split()

        translated_moves = [ moves_translation.get(move, move) for move in raw_moves ]

        return translated_moves

    except KeyError:
        return ["Error: Color mismatch"]

    except Exception as e:
        return [f"Error: {str(e)}"]
      
