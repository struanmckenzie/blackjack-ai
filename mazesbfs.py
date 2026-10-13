from PIL import Image, ImageDraw
import numpy as np
import os

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

def drawPath(img, path):
    draw = ImageDraw.Draw(img)
    for pos in path:
        x, y = pos
        draw.point((x, y), fill="red")
    return img

def bfs(maze, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = [(start, [start])]
    visited = set()
    while queue:
        (currX, currY), path = queue.pop(0)
        if (currX, currY) == end:
            return path
        for dx, dy in directions:
            nextX, nextY = currX +dx, currY + dy
            if isMoveValid(maze, (nextX, nextY)) and (nextX, nextY) not in visited:
                visited.add((nextX, nextY))
                queue.append((nextX, nextY), path + [(nextX, nextY)])