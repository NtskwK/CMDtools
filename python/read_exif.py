import piexif
import logging
from PIL import Image
from PIL.ExifTags import Base as Exif


logger = logging.getLogger(__name__)
image_path = "DJI_0176_with_bps.JPG"


def use_piexif():
    exif = piexif.load(image_path)
    try:
        bps = piexif.load(image_path)["0th"][piexif.ImageIFD.BitsPerSample]
        print(f"BitsPerSample: {bps}")
        if isinstance(bps, int):
            # Always resize single band images
            can_resize = True
        elif isinstance(bps, tuple) and len(bps) > 1:
            # Only resize multiband images if depth is 8bit
            can_resize = bps == (8,) * len(bps)
        else:
            logger.warning(
                "Cannot determine if image %s can be resized, hoping for the best!",
                image_path,
            )
            can_resize = True

    except KeyError:
        logger.warning("Cannot find BitsPerSample tag for %s", image_path)

def use_pillow():
    img = Image.open(image_path)
    exif = img.getexif()
    bps = exif.get(Exif.BitsPerSample.value)
    print(f"BitsPerSample: {bps}")

    # try:
    #     bps = exif.get()
    #     if isinstance(bps, int):
    #         # Always resize single band images
    #         can_resize = True
    #     elif isinstance(bps, tuple) and len(bps) > 1:
    #         # Only resize multiband images if depth is 8bit
    #         can_resize = bps == (8,) * len(bps)
    #     else:
    #         logger.warning(
    #             "Cannot determine if image %s can be resized, hoping for the best!",
    #             image_path,
    #         )
    #         can_resize = True

    # except KeyError:
    #     logger.warning("Cannot find BitsPerSample tag for %s", image_path)


if __name__ == "__main__":
    # use_piexif()
    use_pillow()