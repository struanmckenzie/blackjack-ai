from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw
import numpy as np
import os
import heapq

def loadMaze(imagePath):
    img = Image.open(imagePath).convert('L')
    maze = np.array(img)
    maze = maze < 128
    return img, maze

def isMoveValid(maze, pos):
    x, y = pos
    if 0 <= x < maze.shape[1] and 0 <= y < maze.shape[0]:
        return not maze[y, x]
    return False

def drawPath(img, path, visted):
    draw = ImageDraw.Draw(img)
    for pos in visted:
        x, y = pos
        draw.point((x, y), fill="red")
    for pos in path:
        x, y = pos
        draw.point((x, y), fill="blue")
    return img


def dfs(maze, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = [(start, [start])]
    visited = {start}
    while stack:
        (current_x, current_y), path = stack.pop()
        if (current_x, current_y) == end:
            return path, visited

        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            if isMoveValid(maze, (next_x, next_y)) and (next_x, next_y) not in visited:
                visited.add((next_x, next_y))
                stack.append(((next_x, next_y), path + [(next_x, next_y)]))

    return None, visited

# Function for a breadth-first search to find the shortest path
def bfs(maze, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = [(start, [start])]
    visited = {start}
    while queue:
        (current_x, current_y), path = queue.pop(0)
        if (current_x, current_y) == end:
            return path, visited
        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            if isMoveValid(maze, (next_x, next_y)) and (next_x, next_y) not in visited:
                visited.add((next_x, next_y))
                queue.append(((next_x, next_y), path + [(next_x, next_y)]))
    return None, visited

def a_star(maze, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    priority_queue = []

    heapq.heappush(priority_queue, (heuristic(start, end), 0, start, [start]))

    best_cost = {start: 0}
    visited = {start}

    while priority_queue:
        f_score, g_score, current, path = heapq.heappop(priority_queue)
        current_x, current_y = current

        if current == end:
            return path, visited

        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            if isMoveValid(maze, (next_x, next_y)) and (next_x, next_y) not in visited:
                tenative_g = g_score + 1
                if tenative_g < best_cost.get((next_x, next_y), float("inf")):
                    best_cost[(next_x, next_y)] = tenative_g

                    temp_f_score = tenative_g + heuristic((next_x, next_y), end)
                    visited.add((next_x, next_y))
                    
                    heapq.heappush(priority_queue, (temp_f_score, tenative_g, (next_x, next_y), path + [(next_x, next_y)]))

    return None, visited



def heuristic(position, end):
    x, y = position
    end_x, end_y = end
    return abs(x - end_x) + abs(y - end_y)



def solve_and_save_maze(image_path, output_directory, algorithm):
    maze_img, maze = loadMaze(image_path)

    # Define start and end points
    start_point = (0, 1)  # Example start point
    end_point = (maze.shape[1] - 1, maze.shape[0] - 2)

    # Solve the maze
    solved_path, visited = algorithm(maze, start_point, end_point)

    # Draw the path on the maze and save it
    if solved_path:
        maze_solved_img = drawPath(maze_img, solved_path, visited)
        # Save the solved maze with path
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_directory, filename)
        maze_solved_img.save(output_path)
        return output_path
    else:
        print(f"No solution found for the maze: {image_path}")
        return None

if __name__ == "__main__":
    # Directory paths
    input_directory = 'imperfect_maze_png'
    output_directory_dfs = 'solvedDFS'
    output_directory_bfs = 'solvedBFS'
    output_directory_a_star = 'solvedAStar'

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory_dfs, exist_ok=True)
    os.makedirs(output_directory_bfs, exist_ok=True)
    os.makedirs(output_directory_a_star, exist_ok=True)

    # Get all the image paths
    image_paths = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.endswith('.png')]
    
    # Limit the number of images to process
    max_images = 100
    image_paths = image_paths[:max_images]

    print(f"Will only process {len(image_paths)} images.")

    # Process the images using multiple processes
    with ProcessPoolExecutor() as executor:
        # List to store futures
        futures = []
        for image_path in image_paths:
            futures.append(executor.submit(solve_and_save_maze, image_path, output_directory_dfs, dfs))
            futures.append(executor.submit(solve_and_save_maze, image_path, output_directory_bfs, bfs))
            futures.append(executor.submit(solve_and_save_maze, image_path, output_directory_a_star, a_star))

        # Track the progress and print after every 10 mazes solved
        completed = 0
        total = len(futures)
        update_interval = 10
        for future in futures:
            future.result()
            completed += 1
            if completed % update_interval == 0:
                print(f"Solved {completed}/{total} mazes")