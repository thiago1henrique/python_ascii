import PIL.Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[min(pixel * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)] for pixel in pixels])
    return characters


def gerar_arte_ascii(caminho_imagem, new_width=100):
    try:
        with PIL.Image.open(caminho_imagem) as img:
            # Converter para RGB se for PNG com transparência
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            resized_img = resize_image(img, new_width)
            grayscaled_img = grayify(resized_img)
            new_image_data = pixels_to_ascii(grayscaled_img)

            pixel_count = len(new_image_data)
            ascii_image = "\n".join(
                new_image_data[i:(i + new_width)]
                for i in range(0, pixel_count, new_width)
            )
            return ascii_image

    except Exception as e:
        return f"Erro no processamento: {str(e)}"