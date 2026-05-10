from PIL import Image
import io

TARGET_WIDTH = 1200  # Gemini performs best with this size range

def preprocess(image_bytes: bytes) -> bytes:
    """Rescale image to standard width, preserving aspect ratio."""
    img = Image.open(io.BytesIO(image_bytes))
    ratio = TARGET_WIDTH / img.width
    new_height = int(img.height * ratio)
    img = img.resize((TARGET_WIDTH, new_height), Image.LANCZOS)

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=90)
    return output.getvalue()
