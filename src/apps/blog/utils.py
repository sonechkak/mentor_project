import os


def article_image_upload_to(instance, filename):
    return os.path.join('src/media/articles', filename)


def tag_icon_upload_to(instance, filename):
    return os.path.join('src/media/tags', filename)