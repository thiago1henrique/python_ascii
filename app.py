# Importações necessárias
import os
import uuid
import threading
import heapq
import time
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename, send_from_directory
from conversor_ascii import gerar_arte_ascii, ordenar_arte_ascii

# Inicializa o app Flask
app = Flask(__name__)

# Configuração da pasta de uploads\UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Tipos de arquivos permitidos para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Banco de dados em memória para armazenar tarefas e fila de prioridade
tasks_db = {}
task_heap = []
heap_id_counter = 0  # usado para desempatar tarefas com mesmo tamanho

#  Estrutura de lista encadeada para manter histórico limitado
class HistoricoNode:
    __slots__ = ('task_id', 'timestamp', 'next')

    def __init__(self, task_id):
        self.task_id = task_id
        self.timestamp = time.time()
        self.next = None

# Ponteiros da lista encadeada
historico_head = None
historico_tail = None
HISTORICO_MAX = 10  # Limite de histórico

# Rota para servir arquivos HTML manualmente, se necessário
@app.route('/templates/<path:filename>')
def custom_static(filename):
    return send_from_directory('templates', filename)

#Verifica se o arquivo tem uma extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Thread que processa as imagens em segundo plano
def worker():
    global task_heap
    while True:
        if task_heap:
            # Retira a tarefa de maior prioridade (menor tamanho)
            _, heap_id, task_id = heapq.heappop(task_heap)
            task = tasks_db.get(task_id)
            if not task:
                continue

            try:
                task['status'] = 'processando'
                resultado_ascii = gerar_arte_ascii(task['caminho_imagem'])
                task['resultado'] = resultado_ascii
                task['status'] = 'concluido'
            except Exception as e:
                task['status'] = 'erro'
                task['resultado'] = f"Erro no processamento: {e}"
            finally:
                # Apaga a imagem após o processamento
                if os.path.exists(task['caminho_imagem']):
                    os.remove(task['caminho_imagem'])
            #Adiciona ao histórico encadeado
            adicionar_ao_historico(task_id)
        else:
            time.sleep(0.5)  # espera um pouco caso não haja tarefas

# Adiciona uma tarefa ao histórico limitado
def adicionar_ao_historico(task_id):
    global historico_head, historico_tail
    new_node = HistoricoNode(task_id)

    if historico_head is None:
        historico_head = new_node
        historico_tail = new_node
    else:
        historico_tail.next = new_node
        historico_tail = new_node

    # Mantém apenas os últimos 10 nós
    count = 1
    current = historico_head

    while current and count < HISTORICO_MAX:
        current = current.next
        count += 1

    if current and current.next:
        current.next = None
        historico_tail = current

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para upload de imagens
@app.route('/upload', methods=['POST'])
def upload_files():
    global heap_id_counter
    if 'images' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    files = request.files.getlist('images')
    task_ids = []

    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            continue

        # Gera ID único e salva o arquivo
        task_id = str(uuid.uuid4())
        filename = secure_filename(f"{task_id}_{file.filename}")
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(caminho_imagem)

        # Prioridade baseada no tamanho do arquivo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        tasks_db[task_id] = {
            'id': task_id,
            'status': 'pendente',
            'nome_original': file.filename,
            'caminho_imagem': caminho_imagem,
            'resultado': None
        }

        # Insere na fila de prioridade
        heapq.heappush(task_heap, (file_size, heap_id_counter, task_id))
        heap_id_counter += 1

        task_ids.append(task_id)

    return jsonify({'task_ids': task_ids})

# Verifica o status de uma tarefa
@app.route('/status/<task_id>')
def get_status(task_id):
    task = tasks_db.get(task_id)
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    return jsonify({
        'id': task['id'],
        'status': task['status'],
        'nome_original': task['nome_original'],
        'resultado': task.get('resultado')
    })

# Retorna histórico das últimas tarefas
@app.route('/historico')
def get_historico():
    historico = []
    current = historico_head
    while current:
        task = tasks_db.get(current.task_id)
        if task:
            historico.append({
                'id': task['id'],
                'nome_original': task['nome_original'],
                'timestamp': current.timestamp,
                'status': task['status']
            })
        current = current.next
    return jsonify(historico)

#Ordena a arte ASCII pelo número de caracteres em cada linha
@app.route('/ordenar/<task_id>', methods=['POST'])
def ordenar_arte(task_id):
    task = tasks_db.get(task_id)
    if not task or task['status'] != 'concluido':
        return jsonify({'error': 'Tarefa não disponível'}), 404

    data = request.get_json()
    largura = data.get('largura', 100)

    try:
        arte_ordenada = ordenar_arte_ascii(task['resultado'], largura)
    except Exception as e:
        return jsonify({'error': f'Erro ao ordenar: {str(e)}'}), 500

    return jsonify({'arte_ordenada': arte_ordenada})

# Inicia o servidor e a thread de processamento
if __name__ == '__main__':
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()
    app.run(debug=True)
