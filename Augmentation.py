import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread(os.path.join("leaves", "Apple", "Apple_Black_rot", "image (1).JPG"))
if image is None:
    print("Could not read the image.")
    exit(1)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def show_image(image):
    plt.figure()
    plt.imshow(image)
    # plt.axis('off')
    plt.show()

show_image(image)
