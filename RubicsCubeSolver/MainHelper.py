import random
import cv2 as cv
import random

COLOR_CYCLE = ["yellow", "orange", "blue", "white", "green", "red"]
NAVY_COLOR = (128, 0, 0)
NUM_PARTICLES = 100

confetti_x = [random.randint(20, 1180) for _ in range(NUM_PARTICLES)]
confetti_y = [random.randint(-100, 0) for _ in range(NUM_PARTICLES)]
confetti_speed_y = [random.uniform(4, 10) for _ in range(NUM_PARTICLES)]
confetti_speed_x = [random.uniform(-2, 2) for _ in range(NUM_PARTICLES)]
confetti_colors = [(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for _ in range(NUM_PARTICLES)]
confetti_sizes = [random.randint(4, 8) for _ in range(NUM_PARTICLES)]

def update_and_draw_confetti(canvas):
    """Konfeti parçacıklarının pozisyonlarını günceller ve ekrana çizer."""
    for i in range(NUM_PARTICLES):
        confetti_y[i] += confetti_speed_y[i]
        confetti_x[i] += confetti_speed_x[i]
        
        if confetti_y[i] > 630:
            confetti_y[i] = random.randint(-50, 0)
            confetti_x[i] = random.randint(20, 1180)
            confetti_speed_y[i] = random.uniform(4, 10)
            confetti_speed_x[i] = random.uniform(-2, 2)
            
        cv.circle(canvas, (int(confetti_x[i]), int(confetti_y[i])), confetti_sizes[i], confetti_colors[i], -1)

