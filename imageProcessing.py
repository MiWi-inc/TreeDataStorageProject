import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
import os

def loadImage(path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content/image1.png')):
    img = cv2.imread(path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (128, 128), interpolation = cv2.INTER_AREA)
    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    print(rgb.shape)
    return(resized)

image = loadImage()

print(image)