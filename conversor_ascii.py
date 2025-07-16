import PIL.Image

# Lista de caracteres ASCII usados para representar diferentes níveis de brilho
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    """
    Redimensiona a imagem mantendo a proporção original,
    ajustando a altura para compensar a diferença de proporção dos caracteres ASCII.
    """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)  # Multiplica por 0.5 para ajustar a proporção vertical
    return image.resize((new_width, new_height))  # Retorna a imagem redimensionada

def grayify(image):
    """
    Converte a imagem para escala de cinza (tons de cinza),
    facilitando a conversão para caracteres ASCII baseados em brilho.
    """
    return image.convert("L")

def pixels_to_ascii(image):
    """
    Converte cada pixel da imagem em um caractere ASCII,
    baseado no nível de brilho do pixel.
    """
    pixels = image.getdata()  # Obtém todos os pixels da imagem em uma lista
    # Para cada pixel, escolhe um caractere da lista ASCII_CHARS proporcional ao brilho do pixel
    characters = "".join([
        ASCII_CHARS[
            min(pixel * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)
        ]
        for pixel in pixels
    ])
    return characters  # Retorna a string com todos os caracteres concatenados

def gerar_arte_ascii(caminho_imagem, new_width=100):
    """
    Abre a imagem do caminho especificado, processa e converte em arte ASCII.
    """
    try:
        with PIL.Image.open(caminho_imagem) as img:
            # Caso a imagem tenha canal alfa (transparência), converte para RGB
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            resized_img = resize_image(img, new_width)  # Redimensiona
            grayscaled_img = grayify(resized_img)       # Converte para tons de cinza
            new_image_data = pixels_to_ascii(grayscaled_img)  # Converte para ASCII

            pixel_count = len(new_image_data)
            # Divide a longa string de caracteres em linhas de comprimento new_width
            ascii_image = "\n".join(
                new_image_data[i:(i + new_width)]
                for i in range(0, pixel_count, new_width)
            )
            return ascii_image  # Retorna a arte ASCII formatada

    except Exception as e:
        # Em caso de erro, retorna uma mensagem descritiva
        return f"Erro no processamento: {str(e)}"

def ordenar_arte_ascii(arte_ascii, largura):
    """
    Ordena as linhas da arte ASCII usando Heapsort baseado na 'densidade' de caracteres,
    onde linhas com mais caracteres diferentes de espaço têm maior prioridade.
    """
    linhas = arte_ascii.split('\n')  # Separa a arte ASCII em linhas
    n = len(linhas)

    def densidade(i):
        # Calcula a quantidade de caracteres que não são espaço na linha i
        return sum(1 for char in linhas[i] if char != ' ')

    # Constroi o heap max (max-heap) usando a função densidade como chave
    for i in range(n // 2 - 1, -1, -1):
        heapify(linhas, n, i, densidade)

    # Extrai elementos do heap para ordenar a lista
    for i in range(n - 1, 0, -1):
        linhas[i], linhas[0] = linhas[0], linhas[i]  # Troca o maior com o último item
        heapify(linhas, i, 0, densidade)            # Reconstrói o heap para o resto da lista

    return '\n'.join(linhas)  # Retorna as linhas ordenadas como uma única string

def heapify(arr, n, i, key_func):
    """
    Função auxiliar para manter a propriedade de heap em uma subárvore.
    - arr: lista a ser organizada
    - n: tamanho da heap
    - i: índice do nó atual
    - key_func: função que retorna a chave para comparação
    """
    maior = i  # Assume que o maior é o nó atual
    esq = 2 * i + 1  # índice do filho esquerdo
    dir = 2 * i + 2  # índice do filho direito

    # Verifica se filho esquerdo existe e é maior que o atual
    if esq < n and key_func(esq) > key_func(maior):
        maior = esq

    # Verifica se filho direito existe e é maior que o maior atual
    if dir < n and key_func(dir) > key_func(maior):
        maior = dir

    # Se o maior não é o nó atual, troca e continua a heapify recursivamente
    if maior != i:
        arr[i], arr[maior] = arr[maior], arr[i]
        heapify(arr, n, maior, key_func)