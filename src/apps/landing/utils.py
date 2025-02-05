import os


def content_image_upload_to(instance, filename):
    return os.path.join("content", filename)

def main_image_upload_to(instance, filename):
    return os.path.join("main", filename)