import os
import numpy as np

def loadMaze(imagePath):
    img = Image.open(imagePath).convert('L')
    maze = np.array(img)
    maze = maze < 128
    return img, maze

