import qrcode
from io import BytesIO
import base64


def get_qr(data: str) -> str:
    """二维码
    """
    if not data:
        return None
    img = qrcode.make(data)
    output_buffer = BytesIO()
    img.save(output_buffer, format="PNG")
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode(encoding="utf-8")