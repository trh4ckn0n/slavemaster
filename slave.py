import socket
import subprocess
import json
import os

HOST = '0.0.0.0'
PORT = 8888

print("[SLAVE] En attente de commandes sur le port 8888...")

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
                output = subprocess.check_output(command["cmd"], shell=True, timeout=120)
                conn.send(output)
            except subprocess.CalledProcessError as e:
                conn.send(f"Erreur: {e}".encode())
            except Exception as e:
                conn.send(f"Erreur: {e}".encode())

        elif command["type"] == "runscript":
            script_path = f"./scripts/{command['script']}"
            if os.path.isfile(script_path):
                try:
                    output = subprocess.check_output(f"bash {script_path}", shell=True, timeout=180)
                    conn.send(output)
                except Exception as e:
                    conn.send(f"Erreur exécution script: {e}".encode())
            else:
                conn.send(b"Script introuvable")

        elif command["type"] == "john":
            hashfile = command.get("file", "hashes.txt")
            try:
                output = subprocess.check_output(f"john {hashfile}", shell=True, timeout=300)
                conn.send(output)
            except Exception as e:
                conn.send(f"Erreur John: {e}".encode())

        else:
            conn.send(b"Commande inconnue")
    except Exception as e:
        conn.send(f"Erreur: {e}".encode())
    finally:
        conn.close()
