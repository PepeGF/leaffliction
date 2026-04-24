import math
import os
import sys
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterator
import random


def iter_images_from_folder(folder) -> Iterator[dict[str, str | np.ndarray]]:
    """Generador que itera imágenes del árbol de carpetas
    sin cargarlas todas en memoria."""
    for category in os.listdir(folder):
        category_path = os.path.join(folder, category)
        if os.path.isdir(category_path):
            for status in os.listdir(category_path):
                status_path = os.path.join(category_path, status)
                if os.path.isdir(status_path):
                    for filename in os.listdir(status_path):
                        img_path = os.path.join(status_path, filename)
                        img = cv2.imread(img_path)
                        if img is not None:
                            yield {
                                "image": img,
                                "category": category,
                                "status": status,
                                "filename": filename
                                }


def create_augmented_directories():
    try:
        root = os.getcwd()
        apple_path = os.path.join(root, "augmented_directory", "Apple")
        grape_path = os.path.join(root, "augmented_directory", "Grape")
        apple_statuses = [
            "Apple_Black_rot",
            "Apple_healthy",
            "Apple_rust",
            "Apple_scab"]
        grape_statuses = [
            "Grape_Black_rot",
            "Grape_Esca",
            "Grape_healthy",
            "Grape_spot"
        ]
        os.makedirs(apple_path, exist_ok=True)
        os.makedirs(grape_path, exist_ok=True)
        for status in apple_statuses:
            os.makedirs(os.path.join(apple_path, status), exist_ok=True)
        for status in grape_statuses:
            os.makedirs(os.path.join(grape_path, status), exist_ok=True)
    except Exception as e:
        print(f"Error creating augmented directories: {e}")
        sys.exit(1)


def show_image(image):
    plt.figure()
    plt.imshow(image)
    # plt.axis('off')
    plt.show()


def save_augmented_image(
        image: np.ndarray,
        category: str,
        status: str,
        filename: str,
        augmentation: str):
    root = "augmented_directory"
    filename_without_ext, ext = os.path.splitext(filename)
    new_filename = f"{filename_without_ext}_{augmentation}{ext}"
    save_path = os.path.join(root, category, status, new_filename)
    cv2.imwrite(save_path, image)


def apply_rotation(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    height, width, _ = image.shape
    angle = random.randrange(15, 45) if random.choice([True, False]) \
        else random.randrange(-45, -15)
    T = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    image = cv2.warpAffine(
        image,
        T,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )
    save_augmented_image(
        image,
        category,
        status,
        filename,
        augmentation="Rotate")


def apply_flip(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    flip_code = random.choice([-1, 0, 1])  # Flip horizontal, vertical o ambos
    flipped_image = cv2.flip(image, flip_code)
    save_augmented_image(
        flipped_image,
        category,
        status,
        filename,
        augmentation="Flip")


def apply_blur(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    ksize = random.choice([(3, 3), (5, 5), (7, 7)])
    blurred_image = cv2.GaussianBlur(image, ksize, 0)
    save_augmented_image(
        blurred_image,
        category,
        status,
        filename,
        augmentation="Blur")


def apply_skew(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    height, width, _ = image.shape
    k: float = random.choice(
        [random.uniform(-0.3, -0.1), random.uniform(0.1, 0.3)]
    )
    M = random.choice([
        np.array([[1, k, 0], [0, 1, 0]], dtype=np.float32),
        np.array([[1, 0, 0], [k, 1, 0]], dtype=np.float32)
    ])
    skewed_image = cv2.warpAffine(
        src=image,
        M=M,
        dsize=(width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )
    save_augmented_image(
        skewed_image,
        category,
        status,
        filename,
        augmentation="Skew")


def apply_shear(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    height, width, _ = image.shape
    M = random_shear_matrix(width, height)
    sheared_image = cv2.warpAffine(
        src=image,
        M=M,
        dsize=(width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )
    save_augmented_image(
        sheared_image,
        category,
        status,
        filename,
        augmentation="Shear")


def random_shear_matrix(
        width: int,
        height: int,
        angle_max_deg: float = 15
        ) -> np.ndarray:
    angle_radx = math.radians(random.uniform(-angle_max_deg, angle_max_deg))
    angle_rady = math.radians(random.uniform(-angle_max_deg, angle_max_deg))
    shx = math.tan(angle_radx)
    shy = math.tan(angle_rady)
    tx = -shx * height if shx < 0 else 0
    ty = -shy * width if shy < 0 else 0
    M = np.array([
        [1,   shx, tx],
        [shy, 1,   ty]
    ], dtype=np.float32)
    return M


def apply_crop(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    height, width, _ = image.shape
    crop_size = random.uniform(0.8, 0.95)
    new_width = int(width * crop_size)
    new_height = int(height * crop_size)
    x_start = random.randint(0, width - new_width)
    y_start = random.randint(0, height - new_height)
    cropped_image = image[y_start:y_start + new_height, x_start:x_start + new_width]
    cropped_image = cv2.resize(cropped_image, (width, height))
    save_augmented_image(
        cropped_image,
        category,
        status,
        filename,
        augmentation="Crop")


def apply_distorsion(image_info: dict[str, str | np.ndarray]) -> None:
    image: np.ndarray = image_info.get("image")  # type: ignore
    category: str = image_info.get("category")  # type: ignore
    status: str = image_info.get("status")  # type: ignore
    filename: str = image_info.get("filename")  # type: ignore
    height, width, _ = image.shape
    k1 = random.uniform(-0.0005, 0.0005)
    k2 = random.uniform(-0.0005, 0.0005)
    k3 = random.uniform(-0.0005, 0.0005)
    dist_coeffs = np.array([k1, k2, k3], dtype=np.float32)
    camera_matrix = np.array([
        [width, 0, width / 2],
        [0, width, height / 2],
        [0, 0, 1]
    ], dtype=np.float32)
    distorted_image = cv2.undistort(
        image,
        camera_matrix,
        dist_coeffs,
        None,
        camera_matrix
    )
    save_augmented_image(
        distorted_image,
        category,
        status,
        filename,
        augmentation="Distortion")


if __name__ == "__main__":
    start = time.time()
    create_augmented_directories()
    images_iterator = iter_images_from_folder("leaves")
    for i, image_info in enumerate(images_iterator):
        if i > 50:  # Solo procesar las primeras 5 imágenes para pruebas
            break
        # apply_rotation(image_info)
        # apply_flip(image_info)
        # apply_blur(image_info)
        # apply_skew(image_info)
        # apply_shear(image_info)
        # apply_crop(image_info)
        # apply_distorsion(image_info)
        # print(f"Processing image {i + 1}")
        pass
    duration = time.time() - start
    print(f"Processed {i + 1} images in {duration:.2f} seconds.")
    pass
