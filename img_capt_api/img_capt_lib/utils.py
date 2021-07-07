import os
from typing import List, Tuple
from .lib import predict


def list_all_images(path: str) -> List[str]:
    full_path = os.path.expanduser(path)
    if not os.path.isdir(full_path):
        raise FileNotFoundError
    img_ext = ['.jpg', '.jpeg', '.png']
    images = list(filter(lambda x: os.path.splitext(x)[-1] in img_ext, os.listdir(full_path)))
    images = list(map(lambda x: f"{full_path}/{x}", images))
    return images


def get_caption_of_all_images(path: str) -> List[Tuple[str, str]]:
    images = list_all_images(path)
    return list(map(lambda x: (x, str(predict(x).numpy().tolist())), images))
