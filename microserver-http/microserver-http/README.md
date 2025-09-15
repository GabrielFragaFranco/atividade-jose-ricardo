# Microservidor HTTP de Upload/Download

Servidor HTTP simples para **upload**, **listagem** e **download** de arquivos.

## Pré-requisitos
- **Python 3.10+** instalado
- **pip** instalado
- **VSCode** (opcional como IDE)

> **Não precisa do n8n** para este exercício.

## Instalação e execução

### 1) Criar e ativar *venv*
Linux/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Instalar dependências
```bash
pip install -r requirements.txt
```

### 3) (Opcional) Configurar variáveis de ambiente
Crie um arquivo `.env` ou exporte no shell:
```bash
# Autenticação por API Key (opcional). Se não definir, fica aberto.
export API_KEY=troque-esta-chave

# Limite de tamanho por upload em MB (padrão 50)
export MAX_CONTENT_LENGTH_MB=50
```

No Windows PowerShell:
```powershell
setx API_KEY "troque-esta-chave"
setx MAX_CONTENT_LENGTH_MB "50"
```

### 4) Rodar em modo desenvolvimento
```bash
python server.py
```
Servidor: `http://localhost:8000`

### 5) Rodar com HTTPS de teste (certificado ad-hoc)
Edite a última linha do `server.py` e troque `ssl_context=None` por `'adhoc'`:
```python
app.run(host="0.0.0.0", port=port, threaded=True, ssl_context='adhoc')
```
Depois acesse `https://localhost:8000` (navegador exibirá aviso por ser autoassinado).

### 6) Rodar em "produção" local com gunicorn (Linux/macOS)
```bash
gunicorn -w 4 -k gthread -b 0.0.0.0:8000 server:app
```

---

## Testes com `curl`

### Upload
```bash
curl -F "file=@/caminho/para/arquivo.pdf" http://localhost:8000/upload
# Com API Key:
curl -H "X-API-Key: troque-esta-chave" -F "file=@./exemplo.txt" http://localhost:8000/upload
```

### Listagem
```bash
curl http://localhost:8000/files
curl -H "X-API-Key: troque-esta-chave" http://localhost:8000/files
```

### Download
```bash
curl -OJ http://localhost:8000/files/exemplo.txt
curl -H "X-API-Key: troque-esta-chave" -OJ http://localhost:8000/files/exemplo.txt
```

---

## Estrutura
```
microserver-http/
├─ server.py
├─ requirements.txt
├─ uploads/           # onde os arquivos são salvos
├─ scripts/
│  └─ test_curl.sh    # script de teste
└─ README.md
```

---

## Extensões (para o relatório)
- **HTTPS**: usar `ssl_context='adhoc'` no Flask (dev) ou proxy/Traefik+Let's Encrypt (prod).
- **Concorrência**: `threaded=True` no dev; em prod usar `gunicorn -w 4 -k gthread`.
- **Autenticação**: cabeçalho `X-API-Key` (simples), ou Basic/JWT; ou autenticar no proxy reverso.

---

## Dúvidas comuns
- **Preciso do n8n?** Não.
- **Só o VSCode resolve?** VSCode é só editor. Você precisa do **Python** instalado para rodar.
- **Onde os arquivos ficam?** Na pasta `uploads/` do projeto.
