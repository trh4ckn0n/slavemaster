# ========== MASTER NODE (master_node.py) ==========
# À exécuter sur le smartphone maître avec Termux/Nethunter

import socket
import json
import questionary
import ipaddress
from concurrent.futures import ThreadPoolExecutor

PORT = 8888
NETWORK = "192.168.43.0/24"  # à adapter selon ta plage IP locale

def is_slave_alive(ip):
    try:
        s = socket.create_connection((str(ip), PORT), timeout=1)
        s.close()
        return str(ip)
    except:
        return None

def scan_network():
    print("[🔍] Scan du réseau local en cours...")
    hosts = list(ipaddress.ip_network(NETWORK).hosts())
    alive = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for result in executor.map(is_slave_alive, hosts):
            if result:
                alive.append(result)
    print(f"[✅] {len(alive)} nœud(s) esclave(s) détecté(s).")
    return [{"name": f"Node {i+1} ({ip})", "host": ip, "port": PORT} for i, ip in enumerate(alive)]

def send_command(host, port, command):
    s = socket.socket()
    try:
        s.connect((host, port))
        payload = json.dumps({"type": "exec", "cmd": command})
        s.send(payload.encode())
        response = s.recv(16384).decode(errors="ignore")
        return response
    except Exception as e:
        return f"[ERREUR] {e}"
    finally:
        s.close()

def main():
    SLAVES = scan_network()
    if not SLAVES:
        print("[❌] Aucun esclave trouvé. Connecte-les au même réseau Wi-Fi/Mobile Hotspot.")
        return

    while True:
        action = questionary.select(
            "Que veux-tu faire ?",
            choices=[
                "📥 Lancer une commande sur un nœud",
                "📡 Lancer une commande sur TOUS les nœuds",
                "🧠 Voir mémoire/CPU d'un nœud",
                "🔄 Rescanner le réseau",
                "❌ Quitter"
            ]
        ).ask()

        if action == "❌ Quitter":
            break

        if action == "🔄 Rescanner le réseau":
            SLAVES = scan_network()
            continue

        if action == "📥 Lancer une commande sur un nœud":
            node = questionary.select("Choisis un nœud :", choices=[n["name"] for n in SLAVES]).ask()
            node_info = next(n for n in SLAVES if n["name"] == node)
            cmd = questionary.text("Commande shell à exécuter :").ask()
            result = send_command(node_info["host"], node_info["port"], cmd)
            print(f"\n--- Résultat de {node_info['name']} ---\n{result}\n")

        if action == "📡 Lancer une commande sur TOUS les nœuds":
            cmd = questionary.text("Commande shell à exécuter :").ask()
            for node_info in SLAVES:
                result = send_command(node_info["host"], node_info["port"], cmd)
                print(f"\n--- {node_info['name']} ---\n{result}\n")

        if action == "🧠 Voir mémoire/CPU d'un nœud":
            node = questionary.select("Choisis un nœud :", choices=[n["name"] for n in SLAVES]).ask()
            node_info = next(n for n in SLAVES if n["name"] == node)
            status_cmd = "free -m && top -n 1 -b | head -15"
            result = send_command(node_info["host"], node_info["port"], status_cmd)
            print(f"\n--- État de {node_info['name']} ---\n{result}\n")

if __name__ == '__main__':
    main()
