# utils.py
import math

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def smooth_move(current_pos, target_pos, smoothing_factor=0.2, min_move_threshold=5):
    new_x = current_pos[0] + (target_pos[0] - current_pos[0]) * smoothing_factor
    new_y = current_pos[1] + (target_pos[1] - current_pos[1]) * smoothing_factor
    if abs(new_x - current_pos[0]) < min_move_threshold and abs(new_y - current_pos[1]) < min_move_threshold:
        return current_pos  # Retorna a posição atual se o movimento for menor que o limiar
    return new_x, new_y
