from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

def apply_distortions(img: Image.Image):
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.8)
    np_img = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 10, np_img.shape).astype(np.float32)
    np_img += noise
    np_img = np.clip(np_img, 0, 255).astype(np.uint8)
    return Image.fromarray(np_img)
