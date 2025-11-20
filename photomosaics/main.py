from PIL import Image

IMAGE_EXAMPLE_1 = './fall_pexels-designecologist-1389460.jpg'

def load_image(path: str):
    return Image.open(path)


