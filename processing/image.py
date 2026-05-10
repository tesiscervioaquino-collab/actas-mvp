from PIL import Image
import io

TARGET_HEIGHT = 2048

def preprocess(image_bytes: bytes) -> bytes:
    """Rescale image to 2048px height, preserving aspect ratio."""
    img = Image.open(io.BytesIO(image_bytes))
    ratio = TARGET_HEIGHT / img.height
    new_width = int(img.width * ratio)
    img = img.resize((new_width, TARGET_HEIGHT), Image.LANCZOS)

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=90)
    return output.getvalue()