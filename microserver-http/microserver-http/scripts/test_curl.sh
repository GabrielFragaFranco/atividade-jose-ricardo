#!/usr/bin/env bash
# Testes rápidos com curl
set -e

API="${API_KEY:-}"
HOST="${HOST:-http://localhost:8000}"

echo "[1/3] Listando arquivos (pode estar vazio):"
if [ -n "$API" ]; then
  curl -s -H "X-API-Key: $API" "$HOST/files" | jq . || true
else
  curl -s "$HOST/files" | jq . || true
fi

echo "[2/3] Enviando este README.md como upload:"
if [ -n "$API" ]; then
  curl -s -H "X-API-Key: $API" -F "file=@README.md" "$HOST/upload" | jq .
else
  curl -s -F "file=@README.md" "$HOST/upload" | jq .
fi

echo "[3/3] Baixando README.md (nome pode ter sufixo)"
NAME="README.md"
curl -s -OJ "$HOST/files/$NAME" || true
echo "Concluído."
