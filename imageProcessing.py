import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
import os
from sklearn.cluster import MiniBatchKMeans
from numpy import unique
from scipy.stats import entropy as scipy_entropy
import skimage.measure 


def loadImage(path):
    img = cv2.imread(path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (128, 128), interpolation = cv2.INTER_AREA)
    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    print(rgb.shape)
    return(resized)

#image = loadImage()

#print(image)

def resizing(img_path):

    input = cv2.imread(img_path)

    image = cv2.resize(input, (128,128)) 

    return(image)

def quantizer(clusters, img_path, task):
    """Quantizes an image based on a colour palette that K-means creates
    and saves the quantized image on the disk
    Args:
        clusters (int): The number of the clusters i.e. the number of colours
        img_path (str): The path of the input image
    """
    # Load the image
    # image = cv2.imread(img_path)
    image = resizing(img_path)
    h, w = image.shape[:2]

    # Conversion to L*a*b* gamut for perptual meaning
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # reshape the image into a feature vector for k-means
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # Apply K-means and create the quantized image
    clf = MiniBatchKMeans(n_clusters = clusters)
    labels = clf.fit_predict(image)
    quantized = clf.cluster_centers_.astype("uint8")[labels]

    # Reshape the feature vectors to back to images
    quantized = quantized.reshape((h, w, 3))
    image = image.reshape((h, w, 3))

    # Convert from L*a*b* to RGB
    quantized = cv2.cvtColor(quantized, cv2.COLOR_LAB2RGB, cv2.CV_8U)
    image = cv2.cvtColor(image, cv2.COLOR_LAB2RGB, cv2.CV_8U)

    if task == 'preprocessing':
      return quantized

    if task == 'see_preprocessed_img':
      plt.imshow(np.hstack([image, quantized]))
      plt.show()
      
    if task == 'save_preprocessed_img':
      quantized = cv2.cvtColor(quantized, cv2.COLOR_RGB2BGR, cv2.CV_8U)
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR, cv2.CV_8U)
      cv2.imwrite(f"color_quantization_{clusters}.jpg", np.hstack([image, quantized]))


"""def entropy(n_colors, img_path):

    image = quantizer(n_colors, img_path, 'preprocessing')

    value, counts = unique(image, return_counts=True)
    entropy =  scipy_entropy(counts, base=2)

    # return(print(f"Image Entropy scipy {entropy}"))
    return entropy"""

def entropy(n_colors, img):

    value, counts = unique(img, return_counts=True)
    entropy =  scipy_entropy(counts, base=2)
    print(entropy)
    # return(print(f"Image Entropy scipy {entropy}"))
    return entropy

"""def shannon_entropy(n_colors, img_path):

    image = quantizer(n_colors, img_path, 'preprocessing')

    entropy = skimage.measure.shannon_entropy(image)

    # return(print(f"Image Entropy skimage {entropy}"))
    return entropy"""

def shannon_entropy(n_colors, img):

    entropy = skimage.measure.shannon_entropy(img)
    print(entropy)
    # return(print(f"Image Entropy skimage {entropy}"))
    return entropy

def getNumOfColors(img):
    # Convert image to 1D array
    img_1d = img.reshape(-1, img.shape[-1])
    # Get unique colors
    unique_colors = np.unique(img_1d, axis=0)
    # Return number of unique colors
    return len(unique_colors)

def editImage(image, point, data, lvl):
    scale = pow(2, lvl)
    x, y = point
    x -= 5
    y -= 5
    x = math.floor(x*128/1000/scale)*scale
    y = math.floor(y*128/1000/scale)*scale
    for i in range(scale):
       for j in range(scale):
           image[y+j, x+i] = np.array(data)
    return image
