import base64
from io import BytesIO

from PIL.Image import Image
from pytesseract import image_to_string


def encode_pil_image(pil_image: Image) -> str:
    """
    Encode a PIL Image object to base64 without saving to disk

    Args:
        pil_image (PIL.Image.Image): The PIL Image object to encode

    Returns:
        str: Base64 encoded string of the image
    """
    buffered = BytesIO()
    # You can specify the format and quality here
    pil_image.convert("RGB").save(buffered, format="JPEG")
    # Get the byte data and encode it
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")


def get_text_from_img(image: Image) -> str:
    """
    Convert a PIL Image to string with pytesseract

    Args:
        pil_image (PIL.Image.Image): The PIL Image object to encode

    Returns:
        str: text extracted from an image
    """
    text = image_to_string(
        image=image,
        lang="pol",
    )
    return text
