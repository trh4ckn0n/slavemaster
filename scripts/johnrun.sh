#!/bin/bash

HASH_FILE="$1"
WORDLIST="$2"

if [[ -z "$HASH_FILE" || -z "$WORDLIST" ]]; then
    echo "[❌] Utilisation : ./johnrun.sh <hashfile> <wordlist>"
    exit 1
fi

if ! command -v john &> /dev/null; then
    echo "[❌] John the Ripper n'est pas installé. Installe-le avec : pkg install john"
    exit 1
fi

echo "[🔐] Lancement de John sur le fichier $HASH_FILE avec la wordlist $WORDLIST"
john --wordlist="$WORDLIST" "$HASH_FILE"
john --show "$HASH_FILE"
