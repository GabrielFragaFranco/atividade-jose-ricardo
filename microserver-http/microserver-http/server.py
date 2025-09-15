import os
import logging
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---- Config -----------------------------------------------------------------
app = Flask(__name__)

# Limite de 50 MB por upload (ajuste conforme necessidade)
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024

# Chave de API opcional (defina API_KEY para ativar autenticação)
API_KEY = os.environ.get("API_KEY")

# Logging básico no console
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def require_api_key(f):
    """Protege endpoint com API Key via cabeçalho X-API-Key.
       Se API_KEY não estiver definida, a autenticação fica desativada.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if API_KEY:
            key = request.headers.get("X-API-Key")
            if key != API_KEY:
                return jsonify(error="unauthorized"), 401
        return f(*args, **kwargs)
    return wrapper


# ---- Endpoints ---------------------------------------------------------------
@app.post("/upload")
@require_api_key
def upload_file():
    if "file" not in request.files:
        logging.warning("Upload sem campo 'file'")
        return jsonify(error="campo 'file' ausente"), 400

    f = request.files["file"]
    if not f or f.filename.strip() == "":
        return jsonify(error="nome de arquivo vazio"), 400

    filename = secure_filename(f.filename)
    if not filename:
        return jsonify(error="nome de arquivo inválido"), 400

    try:
        # Evita sobrescrever: se existir, acrescenta um sufixo incremental
        save_name = filename
        name, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(UPLOAD_DIR, save_name)):
            save_name = f"{name}_{i}{ext}"
            i += 1

        save_path = os.path.join(UPLOAD_DIR, save_name)
        f.save(save_path)
        size = os.path.getsize(save_path)
        logging.info("Upload concluído: %s (%d bytes) de %s",
                     save_name, size, request.remote_addr)
        return jsonify(message="upload concluído", file=save_name, size=size), 201
    except Exception:
        logging.exception("Falha ao salvar arquivo")
        return jsonify(error="falha ao salvar arquivo"), 500


@app.get("/files")
@require_api_key
def list_files():
    try:
        items = []
        for name in sorted(os.listdir(UPLOAD_DIR)):
            path = os.path.join(UPLOAD_DIR, name)
            if os.path.isfile(path):
                st = os.stat(path)
                items.append({
                    "name": name,
                    "size": st.st_size,
                    "modified": datetime.fromtimestamp(st.st_mtime).isoformat()
                })
        return jsonify(files=items), 200
    except Exception:
        logging.exception("Falha ao listar arquivos")
        return jsonify(error="falha ao listar"), 500


@app.get("/files/<path:filename>")
@require_api_key
def download_file(filename):
    safe = secure_filename(filename)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        return jsonify(error="arquivo não encontrado"), 404
    try:
        return send_from_directory(UPLOAD_DIR, safe, as_attachment=True)
    except Exception:
        logging.exception("Falha no download")
        return jsonify(error="falha no download"), 500


if __name__ == "__main__":
    # Para HTTPS de teste: troque ssl_context=None por 'adhoc'
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, threaded=True, ssl_context=None)
