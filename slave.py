# slave_node.py
import socket
import subprocess
import json

HOST = '0.0.0.0'
PORT = 8888

def handle_command(command):
    if command["type"] == "exec":
        try:
            output = subprocess.check_output(command["cmd"], shell=True, timeout=60)
            return output.decode()
        except Exception as e:
            return str(e)
    return "Unknown command"

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print(f"[SLAVE] En écoute sur {PORT}")

while True:
    conn, addr = s.accept()
    print(f"[SLAVE] Connexion de {addr}")
    data = conn.recv(2048)
    try:
        command = json.loads(data.decode())
        result = handle_command(command)
        conn.send(result.encode())
    except Exception as e:
        conn.send(str(e).encode())
    conn.close()
