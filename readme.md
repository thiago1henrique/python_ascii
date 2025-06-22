Conversor de Imagem para Arte ASCII
✨ Funcionalidades

    Converte qualquer imagem suportada pela biblioteca Pillow.
    Redimensiona a imagem para uma largura definida, mantendo a proporção.
    Ajusta a proporção de altura para uma exibição mais correta em terminais de texto.
    Converte a imagem para escala de cinza para mapear os níveis de brilho.
    Exibe a arte ASCII colorida no terminal.
    Salva o resultado final em um arquivo ascii_art.txt.

⚙️ Pré-requisitos

Para executar este script, você precisará ter:

    Python 3.x
    A biblioteca Pillow

🚀 Instalação e Configuração

Siga os passos abaixo para preparar o ambiente e executar o projeto.

    Clone ou baixe o script para a sua máquina local.

    Abra um terminal na pasta onde você salvou o projeto.

    (Altamente Recomendado) Crie e ative um ambiente virtual:
    Isso isola as dependências do projeto e evita conflitos com outros projetos Python.
    Bash

# Cria o ambiente virtual
python -m venv venv

Bash

# Ativa o ambiente (Windows)
.\venv\Scripts\activate

Bash

# Ativa o ambiente (macOS/Linux)
source venv/bin/activate

Instale as dependências necessárias:
O único requisito para este projeto é a biblioteca Pillow.
Bash

pip install Pillow

(Opcional) Crie um arquivo requirements.txt para facilitar a instalação para outros usuários:
Bash

    pip freeze > requirements.txt

    Da próxima vez, qualquer pessoa poderá instalar as dependências apenas com pip install -r requirements.txt.

▶️ Como Usar

    Com o ambiente virtual ativado e as dependências instaladas, execute o script principal:
    Bash

    python seu_script.py

    (Substitua seu_script.py pelo nome que você deu ao seu arquivo Python)

    O programa solicitará que você insira o caminho para o arquivo de imagem:

    Insira o caminho para a imagem:

    Forneça o caminho completo para a sua imagem e pressione Enter.
        Exemplo no Windows: C:\Users\SeuUsuario\Downloads\minha_foto.jpg
        Exemplo no macOS/Linux: /home/usuario/Imagens/paisagem.png

    A arte ASCII será impressa no terminal, e um arquivo chamado ascii_art.txt será criado na mesma pasta do script com o resultado.

🎨 Exemplo de Saída

A saída no terminal e no arquivo .txt será algo parecido com isto, dependendo da imagem de entrada:

          ++++*????????S#S?*+;:,           
         +*?S#S??????????S#S?*+;:          
        ;*?S#S????????????S#S?*+;          
        *?S#S??????????????S#S?*;          
       ;*?S#S????????????????S#S?* *?S#S??????????????????S#S?         
      ;*?S#S???????????????????S#S         
      *?S#S?????????????????????S#         
      *?S#S?????????????????????S#         
      *?S#S?????????????????????S#         
      ;*?S#S???????????????????S#          
       *?S#S??????????????????S#S          
       ;*?S#S????????????????S#S?          
        *?S#S??????????????S#S?* ;*?S#S????????????S#S?*+           
         ;+*?S#S??????????S#S?*+           
           ,;+*?S#####S??S#S?*+;            