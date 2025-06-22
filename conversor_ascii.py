import PIL.Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels])
    return characters

def gerar_arte_ascii(caminho_imagem, new_width=100):
    """
    Função principal que recebe o caminho de uma imagem e retorna a arte ASCII.
    """
    try:
        img = PIL.Image.open(caminho_imagem)
    except Exception:
        return "Erro: Não foi possível abrir a imagem."

    # Encadeia as operações
    resized_img = resize_image(img, new_width)
    grayscaled_img = grayify(resized_img)
    new_image_data = pixels_to_ascii(grayscaled_img)

    # Formata a string de caracteres
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i + new_width)] for i in range(0, pixel_count, new_width))

    return ascii_image