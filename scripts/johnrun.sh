#!/bin/bash

# === CONFIGURATION ===
HASH_FILE="./hashes.txt"
WORDLIST="./bruteforce_wordlist.txt"
JOHN_PATH="$(which john)"

# === VÉRIFICATIONS ===
if [[ ! -f "$HASH_FILE" ]]; then
    echo "[❌] Fichier de hash manquant: $HASH_FILE"
    exit 1
fi

if [[ ! -f "$WORDLIST" ]]; then
    echo "[❌] Wordlist introuvable: $WORDLIST"
    exit 1
fi

if [[ -z "$JOHN_PATH" ]]; then
    echo "[❌] John the Ripper n'est pas installé."
    exit 1
fi

# === LANCEMENT DE L'ATTAQUE ===
echo "[⚔️] Lancement de John the Ripper sur $HASH_FILE avec $WORDLIST..."
$JOHN_PATH --wordlist="$WORDLIST" "$HASH_FILE"

# === AFFICHAGE DES RÉSULTATS ===
echo -e "\n[✅] Résultats :"
$JOHN_PATH --show "$HASH_FILE"
