#python3

''' utils for deployment'''

import torch
from PIL import Image

def load_img(path):
    img = Image.open(path)
    return img