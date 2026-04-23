import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterator
import random


image = cv2.imread(os.path.join("leaves", "Apple", "Apple_Black_rot", "image (1).JPG"))
if image is None:
    print("Could not read the image.")
    exit(1)
height, width, _ = image.shape
T = cv2.getRotationMatrix2D((width / 2, height / 2), 45, 1)
image = cv2.warpAffine(image, T, (width, height))

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



# leer todas las imágenes de la carpeta leaves y las subcarpetas:
def load_images_from_folder(folder) -> list[np.ndarray]:
    images: list[np.ndarray] = []
    for category in os.listdir(folder):
        category_path = os.path.join(folder, category)
        if os.path.isdir(category_path):
            for subfolder in os.listdir(category_path):
                subfolder_path = os.path.join(category_path, subfolder)
                if os.path.isdir(subfolder_path):
                    for filename in os.listdir(subfolder_path):
                        img_path = os.path.join(subfolder_path, filename)
                        img = cv2.imread(img_path)
                        if img is not None:
                            images.append(img)
    return images


def iter_images_from_folder(folder) -> Iterator[np.ndarray]:
    """Generador que itera imágenes del árbol de carpetas sin cargarlas todas en memoria."""
    for category in os.listdir(folder):
        category_path = os.path.join(folder, category)
        if os.path.isdir(category_path):
            for subfolder in os.listdir(category_path):
                subfolder_path = os.path.join(category_path, subfolder)
                if os.path.isdir(subfolder_path):
                    for filename in os.listdir(subfolder_path):
                        img_path = os.path.join(subfolder_path, filename)
                        img = cv2.imread(img_path)
                        if img is not None:
                            yield img






def show_image(image):
    plt.figure()
    plt.imshow(image)
    # plt.axis('off')
    plt.show()

def create_augmented_directories():
    root = os.getcwd()
    apple_path = os.path.join(root, "augmented_directory", "Apple")
    grape_path = os.path.join(root, "augmented_directory", "Grape")
    os.makedirs(apple_path, exist_ok=True)
    os.makedirs(grape_path, exist_ok=True)




if __name__ == "__main__":
    # print size of the generator object in bytes
    # print("Size of generator object:", sys.getsizeof(wololo), "bytes")

    # Ejemplo de uso: usar el generador para no cargar todas las imágenes en memoria
    images_iterator = iter_images_from_folder("leaves")
    for i, image in enumerate(images_iterator):
        if i >= 5:  # Solo procesar las primeras 5 imágenes para la demostración
            break
        print(f"Processing image {i + 1}")
        # Aquí podrías aplicar tus transformaciones de aumento de datos a cada imagen
    # first_img = next(images_iterator, None)
    # if image is not None:
        height, width, _ = image.shape
        angle = random.randrange(-30, 30)
        print(f"Rotating image by {angle} degrees")
        T = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        image = cv2.warpAffine(
            image,
            T,
            (width, height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255)
        )
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        show_image(image_rgb)
    # create_augmented_directories()
    # show_image(image_rgb)
    pass