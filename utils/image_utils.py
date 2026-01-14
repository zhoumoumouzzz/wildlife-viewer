import os

def image_exists(path):
    return path and os.path.exists(path)
