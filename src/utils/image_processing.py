import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

def apply_watermark_sync(avatar_path: str, watermark_image_path: str):
    try:
        avatar_image = Image.open(avatar_path).convert("RGBA")
        
        watermark = Image.open(watermark_image_path).convert("RGBA")
        
        # Масштабируем вотермарку
        scale_factor = 0.3
        avatar_width, avatar_height = avatar_image.size
        new_width = int(avatar_width * scale_factor)
        aspect_ratio = watermark.size[1] / watermark.size[0]
        new_height = int(new_width * aspect_ratio)
        
        watermark = watermark.resize((new_width, new_height), Image.LANCZOS)

        position = (avatar_width - new_width - 10, avatar_height - new_height - 10)
        
        # Накладываем вотермарку на изображение
        avatar_image.paste(watermark, position, watermark)

        watermarked_path = os.path.splitext(avatar_path)[0] + "_watermarked.png"
        avatar_image.convert("RGB").save(watermarked_path, "PNG")

        return watermarked_path
    except Exception as e:
        print(f"Ошибка при обработке аватара: {e}")
        return None
    

async def apply_watermark(avatar_path: str, watermark_image_path: str):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, apply_watermark_sync, avatar_path, watermark_image_path)