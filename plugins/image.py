import base64
from os import read


def read_image(image_path):
    """读取图片转base64
    """
    with open(image_path, "rb") as img:
        base64_data = base64.b64encode(img.read())
        return base64_data.decode(encoding="utf-8")
