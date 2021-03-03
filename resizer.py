import os
from PIL import Image


# Default dimensions in inches
defaults = [(14, 11), (12, 12), (18, 12), (20, 8),
            (20, 16), (30, 20), (36, 24)]


def create_img_dims(source: str, dimensions=defaults, dpi=300, desination=""):
    """
    Creates copies of differing dimensions for given source image and stores them in a specifed
    destination.
    Arguments:
        source = file or absolute file path
        destination = a path specifying where to save the copies
            DEFAULT: source location
        dimensions = list of tuples holding W x L dimensions in inches
            DEFAULT: predefined sizes
        dpi = number of pixels per inch
            DEFAULT: 300
    """

    file_path = source.rsplit('/', 1)
    if desination:
        try:
            os.chdir(desination)
        except PathError:
            print("ERROR: Couldn't find/create destination path.")
            return False
    elif len(file_path) > 1:
        os.chdir(file_path[0])
        file_name = file_path[1]
    else:
        file_name = source

    file_name = file_name.split('.')

    # Opens the image to process
    im = Image.open(source)

    # The smallest dimension of the the given image will always be the bottleneck.
    # This puts the bottleneck dimension as the first var in originals for the sake
    # of less if statements
    original = (im.width, im.height) if im.height < im.width else (
        im.height, im.width)

    # Creates copies of the given image in the dimensions specified in sizes
    for x, y in dimensions:

        # Desired pixels an inch for the given dimension in inches
        desired = (dpi * x, dpi * y)

        # Calcualtes the aspect ratio
        a = original[0] / original[1]

        # The size in pixels of the non-bottleneck dimension
        new_v = round(a * desired[1])

        # Decides which tuple is neccessary depending on W x L or L x W
        proportions = (new_v, desired[1]) if im.height < im.width else (
            desired[1], new_v)
        try:
            resized = im.resize(proportions, resample=Image.NEAREST)
        except ResizeError:
            print("ERROR: Something went wrong while trying to resize.")
            return False

        # Crops the image on both sides on the non-bottleneck dimension
        b = round((new_v - desired[0]) / 2)
        try:
            if im.height < im.width:
                cropped = resized.crop((b, 0, new_v - b, desired[1]))
                cropped.save(f'{file_name[0]}_{x}x{y}.{file_name[1]}')
            else:
                cropped = resized.crop((0, b, desired[1], new_v - b))
                cropped.save(f'{file_name[0]}_{y}x{x}.{file_name[1]}')
        except CropError:
            print("ERROR: Something went wrong while try to crop.")
            return False

    return True


create_img_dims("0000809_0000809-R1-006-1A.jpg")
