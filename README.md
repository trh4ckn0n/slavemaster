# 🔗 Android RAM+Cluster Tool — Trhacknon Edition

Outil complet pour créer un mini-cluster Android via Termux/Nethunter où un smartphone principal (Master) utilise les ressources RAM/CPU de plusieurs esclaves.

## 🔧 Fonctions principales

- 📡 Détection automatique des esclaves sur le réseau
- 🧠 Monitor RAM & CPU (graphiques temps réel)
- 📥 Exécution de commandes et scripts à distance
- 🔐 Support John The Ripper (hash cracking distribué)
- 📁 Execution de scripts personnalisés dans `./scripts/`
- 💻 Interface interactive avec `questionary` (CLI intuitive)
- 🧾 Logs d’exécution sur les esclaves (`slave_logs.txt`)

---

## 📁 Arborescence du projet

```
cluster_manager/
├── master.py
├── slave.py
├── scripts/
│   ├── johnrun.sh
│   └── bruteforce_wordlist.txt
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Sur tous les appareils (Termux / Nethunter) :

```bash
pkg install python git net-tools
pip install -r requirements.txt
```

JTR:

```
apt install john
```

rockyou and others wordlists:

```
sudo apt update
sudo apt install -y john wordlists
```

```
gzip -d /usr/share/wordlists/rockyou.txt.gz
```

```
cp /usr/share/wordlists/rockyou.txt ./scripts/bruteforce_wordlist.txt
```


Sur les esclaves :

```
python slave.py
```

Sur le maître :

```
python master.py
```

