import socket
import json
import questionary
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from rich import print
from rich.table import Table
from rich.console import Console

PORT = 8888
NETWORK = "192.168.43.0/24"
console = Console()


def is_slave_alive(ip):
    try:
        s = socket.create_connection((str(ip), PORT), timeout=1)
        s.close()
        return str(ip)
    except:
        return None


def scan_network():
    print("[cyan]\n[🔍] Scan du réseau local...")
    hosts = list(ipaddress.ip_network(NETWORK).hosts())
    alive = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for result in executor.map(is_slave_alive, hosts):
            if result:
                alive.append(result)
    print(f"[green]✅ {len(alive)} esclave(s) actif(s).")
    return [{"name": f"Node {i+1} ({ip})", "host": ip, "port": PORT} for i, ip in enumerate(alive)]


def send_command(host, port, command):
    s = socket.socket()
    try:
        s.connect((host, port))
        payload = json.dumps(command)
        s.send(payload.encode())
        response = s.recv(16384).decode(errors="ignore")
        return response
    except Exception as e:
        return f"[ERREUR] {e}"
    finally:
        s.close()


def show_stats(slaves):
    table = Table(title="📊 Statistiques CPU/RAM des Nœuds")
    table.add_column("Nœud")
    table.add_column("RAM (Mo)")
    table.add_column("Top CPU")

    for node in slaves:
        result = send_command(node["host"], node["port"], {"type": "exec", "cmd": "free -m && top -b -n1 | head -10"})
        lines = result.splitlines()
        ram = lines[1] if len(lines) > 1 else "N/A"
        topcpu = " ".join(lines[2:5]) if len(lines) > 5 else "N/A"
        table.add_row(node["name"], ram, topcpu)

    console.print(table)


def main():
    SLAVES = scan_network()
    if not SLAVES:
        print("[red][❌] Aucun esclave trouvé. Connecte-les au même réseau Wi-Fi.")
        return

    while True:
        action = questionary.select(
            "Que veux-tu faire ?",
            choices=[
                "📥 Lancer une commande shell sur un nœud",
                "📡 Lancer une commande shell sur TOUS",
                "🧠 Voir RAM/CPU (graphique)",
                "⚙️ Lancer un script custom",
                "🪓 Lancer JohnTheRipper",
                "🔄 Rescanner le réseau",
                "❌ Quitter"
            ]
        ).ask()

        if action == "❌ Quitter":
            break

        if action == "🔄 Rescanner le réseau":
            SLAVES = scan_network()
            continue

        if action == "📥 Lancer une commande shell sur un nœud":
            node = questionary.select("Choisis un nœud :", choices=[n["name"] for n in SLAVES]).ask()
            node_info = next(n for n in SLAVES if n["name"] == node)
            cmd = questionary.text("Commande shell à exécuter :").ask()
            result = send_command(node_info["host"], node_info["port"], {"type": "exec", "cmd": cmd})
            print(f"\n--- Résultat de {node_info['name']} ---\n{result}\n")

        if action == "📡 Lancer une commande shell sur TOUS":
            cmd = questionary.text("Commande shell à exécuter :").ask()
            for node_info in SLAVES:
                result = send_command(node_info["host"], node_info["port"], {"type": "exec", "cmd": cmd})
                print(f"\n--- {node_info['name']} ---\n{result}\n")

        if action == "🧠 Voir RAM/CPU (graphique)":
            show_stats(SLAVES)

        if action == "⚙️ Lancer un script custom":
            script = questionary.text("Nom du script dans ./scripts/ :").ask()
            for node_info in SLAVES:
                result = send_command(node_info["host"], node_info["port"], {"type": "runscript", "script": script})
                print(f"\n--- {node_info['name']} ---\n{result}\n")

        if action == "🪓 Lancer JohnTheRipper":
            hashfile = questionary.text("Nom du fichier de hash sur l'esclave (ex: hashes.txt):").ask()
            for node_info in SLAVES:
                result = send_command(node_info["host"], node_info["port"], {"type": "john", "file": hashfile})
                print(f"\n--- {node_info['name']} ---\n{result}\n")


if __name__ == '__main__':
    main()
