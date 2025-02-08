import random

def get_direction(head, food):
    if head["x"] < food["x"]:
        return "right"  # Движение вправо по оси X
    elif head["x"] > food["x"]:
        return "left"   # Движение влево по оси X
    elif head["y"] < food["y"]:
        return "up"     # Движение вверх по оси Y
    elif head["y"] > food["y"]:
        return "down"   # Движение вниз по оси Y
    return None

def find_closest_food(head, food_list):
    min_distance = float("inf")
    closest_food = None
    for food in food_list:
        distance = abs(head["x"] - food["x"]) + abs(head["y"] - food["y"])
        if distance < min_distance:
            min_distance = distance
            closest_food = food
    return closest_food

def get_occupied_cells(snakes_data):
    occupied = set()
    for snake in snakes_data:
        for segment in snake["body"][:-1]:
            occupied.add((segment["x"], segment["y"]))
    return occupied

def handle_move(game_state: dict) -> dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    my_head = game_state["you"]["body"][0]  # Coords of your head
    my_neck = game_state["you"]["body"][1]  # Coords of your "neck"
    my_body = game_state['you']['body']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    # Prevent from moving backwards
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent out of bounds
    if my_head["x"] + 1 >= board_width:
        is_move_safe["right"] = False
    if my_head["x"] - 1 < 0:
        is_move_safe["left"] = False
    if my_head["y"] + 1 >= board_height:
        is_move_safe["up"] = False
    if my_head["y"] - 1 < 0:
        is_move_safe["down"] = False

    # Prevent collisions with itself
    for segment in my_body[1:]:
        if (my_head["x"] + 1, my_head["y"]) == (segment["x"], segment["y"]):
            is_move_safe["right"] = False
        if (my_head["x"] - 1, my_head["y"]) == (segment["x"], segment["y"]):
            is_move_safe["left"] = False
        if (my_head["x"], my_head["y"] + 1) == (segment["x"], segment["y"]):
            is_move_safe["up"] = False
        if (my_head["x"], my_head["y"] - 1) == (segment["x"], segment["y"]):
            is_move_safe["down"] = False

    # Prevent collisions with other snakes
    opponents = game_state['board']['snakes']
    occupied_cells = get_occupied_cells(opponents)
    for (x, y) in occupied_cells:
        if (my_head["x"] + 1, my_head["y"]) == (x, y):
            is_move_safe["right"] = False
        if (my_head["x"] - 1, my_head["y"]) == (x, y):
            is_move_safe["left"] = False
        if (my_head["x"], my_head["y"] + 1) == (x, y):
            is_move_safe["up"] = False
        if (my_head["x"], my_head["y"] - 1) == (x, y):
            is_move_safe["down"] = False

    # Collect safe moves
    safe_moves = [move for move, is_safe in is_move_safe.items() if is_safe]

    # If no safe moves, return a fallback move (e.g., "down")
    if not safe_moves:
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
    return {"move": next_move}