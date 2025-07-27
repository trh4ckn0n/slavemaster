# ========== SLAVE NODE (slave_node.py) ==========
# À exécuter sur chaque appareil Android avec Termux/Nethunter

import socket
import subprocess
import json

HOST = '0.0.0.0'  # écoute sur toutes les interfaces
PORT = 8888       # port par défaut utilisé

print("[SLAVE] Lancement du nœud esclave en attente de commandes...")

s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f"[SLAVE] Connexion de {addr}")
    try:
        data = conn.recv(4096)
        command = json.loads(data.decode())

        if command["type"] == "exec":
            try:
                output = subprocess.check_output(command["cmd"], shell=True, timeout=60)
                conn.send(output)
            except subprocess.CalledProcessError as e:
                conn.send(f"Erreur de commande: {e}".encode())
            except Exception as e:
                conn.send(f"Erreur : {e}".encode())
        else:
            conn.send(b"Commande inconnue")
    except Exception as e:
        conn.send(f"Erreur: {e}".encode())
    finally:
        conn.close()
