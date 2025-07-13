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


def ordenar_arte_ascii(arte_ascii, largura):
    linhas = arte_ascii.split('\n')
    n = len(linhas)

    def densidade(i):
        return sum(1 for char in linhas[i] if char != ' ')

    for i in range(n // 2 - 1, -1, -1):
        heapify(linhas, n, i, densidade)

    for i in range(n - 1, 0, -1):
        linhas[i], linhas[0] = linhas[0], linhas[i]
        heapify(linhas, i, 0, densidade)

    return '\n'.join(linhas)


def heapify(arr, n, i, key_func):
    maior = i
    esq = 2 * i + 1
    dir = 2 * i + 2

    if esq < n and key_func(esq) > key_func(maior):
        maior = esq

    if dir < n and key_func(dir) > key_func(maior):
        maior = dir

    if maior != i:
        arr[i], arr[maior] = arr[maior], arr[i]
        heapify(arr, n, maior, key_func)