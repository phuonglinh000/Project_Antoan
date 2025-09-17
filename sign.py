from PIL import Image
import stepic
import os
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH

def hide_watermark(input_image: str, output_image: str, author: str):
    make_secret_key()

    secret = read_key_from_file(KEY_PATH)

    signature = create_hmac(author, secret)

    watermark_data = f"Author: {author} | Signature: {signature}"

    img = Image.open(input_image)

    encoded_img = stepic.encode(img, watermark_data.encode("utf-8"))

    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    encoded_img.save(output_image, "PNG")
    print(f"Da nhung watermark vào {output_image}")