# Opcional: container para execução
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./
RUN mkdir -p uploads

# Exponha a porta padrão
EXPOSE 8000

# Para produção, prefira gunicorn
CMD ["gunicorn", "-w", "4", "-k", "gthread", "-b", "0.0.0.0:8000", "server:app"]
