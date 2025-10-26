#!/bin/bash

# Checa se recebeu dois argumentos
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <diretorio> <substring_para_remover>"
    exit 1
fi

DIR="$1"
SUBSTRING="$2"

# Vai para o diretório especificado
cd "$DIR" || { echo "Diretório não encontrado: $DIR"; exit 1; }

# Loop para renomear arquivos que contêm a substring
for file in *"$SUBSTRING"*; do
    [ -f "$file" ] || continue
    new_name="${file//$SUBSTRING/}"  # Remove todas as ocorrências da substring
    # Só renomeia se o nome mudou
    if [ "$file" != "$new_name" ]; then
        mv "$file" "$new_name"
        echo "Renomeado: '$file' → '$new_name'"
    fi
done
