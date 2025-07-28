#!/bin/bash

# === CONFIGURATION ===
HASH_FILE="./scripts/hashes.txt"
WORDLIST="./scripts/bruteforce_wordlist.txt"
JOHN_PATH="$(which john)"
HASHID_PATH="$(which hashid || which hash-identifier)"

# === FONCTIONS ===
detect_hash_type() {
    echo "[🔍] Détection du type de hash..."
    local first_hash=$(head -n 1 "$HASH_FILE")
    if [[ -n "$HASHID_PATH" ]]; then
        echo "[ℹ️] Hash détecté : $first_hash"
        hashid -m "$first_hash" 2>/dev/null | grep -E "^\[[+\* ]\]" || echo "[❌] Type non identifié"
    else
        echo "[⚠️] hashid ou hash-identifier non installé. Skipping type detection."
    fi
}

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

# === DÉTECTION DE TYPE DE HASH ===
detect_hash_type

# === LANCEMENT DE L'ATTAQUE ===
echo -e "\n[⚔️] Lancement de John the Ripper sur $HASH_FILE avec $WORDLIST..."
$JOHN_PATH --wordlist="$WORDLIST" "$HASH_FILE"

# === AFFICHAGE DES RÉSULTATS ===
echo -e "\n[✅] Résultats :"
$JOHN_PATH --show "$HASH_FILE"
