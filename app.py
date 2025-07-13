import os
import uuid
import threading
import heapq
import time
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename, send_from_directory
from conversor_ascii import gerar_arte_ascii, ordenar_arte_ascii

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

tasks_db = {}
task_heap = []
heap_id_counter = 0


class HistoricoNode:
    __slots__ = ('task_id', 'timestamp', 'next')

    def __init__(self, task_id):
        self.task_id = task_id
        self.timestamp = time.time()
        self.next = None


historico_head = None
historico_tail = None
HISTORICO_MAX = 10

@app.route('/templates/<path:filename>')
def custom_static(filename):
    return send_from_directory('templates', filename)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def worker():
    global task_heap
    while True:
        if task_heap:
            # Extrai a tarefa de maior prioridade (menor tamanho de arquivo)
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
                # Remover arquivo após processamento
                if os.path.exists(task['caminho_imagem']):
                    os.remove(task['caminho_imagem'])
            # Adicionar ao histórico
            adicionar_ao_historico(task_id)
        else:
            time.sleep(0.5)


def adicionar_ao_historico(task_id):
    global historico_head, historico_tail
    new_node = HistoricoNode(task_id)

    if historico_head is None:
        historico_head = new_node
        historico_tail = new_node
    else:
        historico_tail.next = new_node
        historico_tail = new_node

    count = 1
    current = historico_head

    while current and count < HISTORICO_MAX:
        current = current.next
        count += 1

    if current and current.next:
        current.next = None
        historico_tail = current


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    global heap_id_counter
    if 'images' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    files = request.files.getlist('images')
    task_ids = []

    for file in files:
        if file.filename == '':
            continue

        if not allowed_file(file.filename):
            continue

        task_id = str(uuid.uuid4())
        filename = secure_filename(f"{task_id}_{file.filename}")
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(caminho_imagem)

        # Calcular prioridade (tamanho do arquivo)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Volta para o início

        tasks_db[task_id] = {
            'id': task_id,
            'status': 'pendente',
            'nome_original': file.filename,
            'caminho_imagem': caminho_imagem,
            'resultado': None
        }

        # Adicionar à fila de prioridade (heap)
        heap_id = heap_id_counter
        heap_id_counter += 1
        heapq.heappush(task_heap, (file_size, heap_id, task_id))

        task_ids.append(task_id)

    return jsonify({'task_ids': task_ids})


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


@app.route('/ordenar/<task_id>', methods=['POST'])
def ordenar_arte(task_id):
    task = tasks_db.get(task_id)
    if not task or task['status'] != 'concluido':
        return jsonify({'error': 'Tarefa não disponível'}), 404

    # Largura original usada para a arte
    data = request.get_json()
    largura = data.get('largura', 100)

    try:
        arte_ordenada = ordenar_arte_ascii(task['resultado'], largura)
    except Exception as e:
        return jsonify({'error': f'Erro ao ordenar: {str(e)}'}), 500

    return jsonify({'arte_ordenada': arte_ordenada})


if __name__ == '__main__':
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()
    app.run(debug=True)