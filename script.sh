#!/bin/bash

# Verifica se foi passado exatamente 1 argumento
if [ $# -ne 1 ]; then
    echo "Uso: $0 \"Título do post\""
    exit 1
fi

TITLE="$1"
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%d\ %H:%M:%S\ -0300)

# Gera o slug a partir do título: minúsculo, sem caracteres especiais, espaços viram hífens
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-zA-Z0-9 ]//g' | sed 's/ /-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

FILENAME="_posts/${DATE}-${SLUG}.md"

cat > "$FILENAME" <<EOF
---
title: "$TITLE"
date: $DATETIME
---

# Hello World
EOF

echo "Post criado com sucesso: $FILENAME"
