import qrcode
import os
from io import BytesIO

# Ensure the directory for storing QR codes exists
if not os.path.exists('qrcodes'):
    os.makedirs('qrcodes')

def generate_qr_code(data: str, filename: str) -> str:
    """
    Generates a QR code from the given data and saves it as an image.

    Args:
        data (str): The data to encode in the QR code.
        filename (str): The filename to save the QR code image.

    Returns:
        str: The path to the generated QR code image.
    """
    img = qrcode.make(data)
    img_path = os.path.join('qrcodes', filename)
    img.save(img_path)
    return img_path

def generate_qr_code_in_memory(data: str) -> BytesIO:
    """
    Generates a QR code and returns it as an in-memory BytesIO object.
    This is useful for sending the QR code directly without saving to a file.

    Args:
        data (str): The data to encode in the QR code.

    Returns:
        BytesIO: An in-memory buffer containing the QR code image.
    """
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
