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