import os
import uuid
import threading
from flask import Flask, render_template, request, jsonify
from queue import Queue
from conversor_ascii import gerar_arte_ascii

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

tasks_db = {}
task_queue = Queue()

def worker():
    """Função que roda em background para processar as tarefas da fila."""
    while True:
        task_id = task_queue.get()
        if task_id is None: break

        task = tasks_db[task_id]
        try:
            task['status'] = 'processando'
            resultado_ascii = gerar_arte_ascii(task['caminho_imagem'])
            task['resultado'] = resultado_ascii
            task['status'] = 'concluido'
        except Exception as e:
            task['status'] = 'erro'
            task['resultado'] = f"Erro no processamento: {e}"
        task_queue.task_done()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    files = request.files.getlist('images')
    task_ids = []

    for file in files:
        if file.filename == '': continue

        task_id = str(uuid.uuid4())
        # Usa o UPLOAD_FOLDER definido na configuração
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{file.filename}")

        # O erro provavelmente está aqui!
        file.save(caminho_imagem)

        tasks_db[task_id] = {
            'id': task_id,
            'status': 'pendente',
            'nome_original': file.filename,
            'caminho_imagem': caminho_imagem,
            'resultado': None
        }
        task_queue.put(task_id)
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


if __name__ == '__main__':
    threading.Thread(target=worker, daemon=True).start()
    app.run(debug=True)