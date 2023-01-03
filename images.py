import os
from PIL import Image
import numpy as np


def isImage(item):
    return item.endswith(".png") or item.endswith(".jpg") or item.endswith(".jpeg")


def countImagesIn(src_dir):
    subdir = os.listdir(src_dir)
    filterimage = [isImage(item) for item in subdir]
    return filterimage.count(True)


# =========================
# imagePreprocessing: Function to preprocess card images into
# corresponding sizes for use in Vassal.
# =========================
def imagePreprocessing(image_url, directory_url=None):
    if directory_url is None: directory_url = image_url

    layer_mask = Image.open("layermask.png")
    layer_mask_np = np.asarray(layer_mask)[:, :, 1]

    image = Image.open(image_url)
    new_image = image.resize((350, 490))
    if new_image.mode != "RGBA":
        new_image = new_image.convert("RGBA")

    new_image_np = np.array(new_image)
    new_image_np[:, :, 3] = layer_mask_np
    new_image = Image.fromarray(new_image_np, 'RGBA')
    new_image.save(directory_url)


# =========================
# copyImagesFromTo: Copy images from directory to directory.
# -  check: Integer, check the number of images, if not matching, escape.
#     - Default: 0
# -  preprocess: Boolean,  determine if image preprocessing is required before copy.
#     - Default: True
# =========================
def copyImagesFromTo(from_dir, to_dir, check=None, preprocess=None):
    # default parameters
    if check is None: check = 0
    if preprocess is None: preprocess = True

    # if check is required
    if check > 0:
        imagecount = countImagesIn(from_dir)
        if imagecount != check: return -1

    # copy images from / to
    from_dir_list = os.listdir(from_dir)
    for item in from_dir_list:
        if isImage(item):
            image_dir = os.path.join(from_dir, item)
            save_dir = f"{to_dir}/{item}"

            if preprocess:
                imagePreprocessing(image_dir, save_dir)
                continue
            image = Image.open(image_dir)
            image.save(to_dir)


def makeImgDir(src_url, dir_url):
    for item in os.listdir(src_url):
        if item.startswith("_"): continue
        if item.startswith("._"): continue

        # if the card is a one-sided card
        if item.endswith(".png") or item.endswith(".jpg") or item.endswith(".jpeg"):
            image_url = f"{src_url}/{item}"
            save_url = f"{dir_url}/{item}"
            imagePreprocessing(image_url, save_url)
            continue

        # if the card is a two-sided card
        tensei_dir = os.path.join(src_url, item)
        if os.path.isdir(tensei_dir):
            subdir = os.listdir(tensei_dir)
            filterimage = [item.endswith(".png") for item in subdir]
            if filterimage.count(True) != 2:
                continue
            else:
                dest_url = f"{dir_url}/{item}"
                if not os.path.exists(dest_url):
                    os.makedirs(dest_url)
                copyImagesFromTo(tensei_dir, dest_url)
    return 1
