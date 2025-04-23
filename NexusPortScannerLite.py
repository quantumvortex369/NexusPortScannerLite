import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, init
from rich.progress import track
import os

# Inicializar colorama
init(autoreset=True)

# 🎯 Argumentos con valores por defecto
parser = argparse.ArgumentParser(description="🔎 NexusPortScannerLite")
parser.add_argument('-t', '--target', type=str, default='127.0.0.1', help='IP o dominio objetivo (default: localhost)')
parser.add_argument('-sp', '--start-port', type=int, default=1, help='Puerto inicial (default: 1)')
parser.add_argument('-ep', '--end-port', type=int, default=1024, help='Puerto final (default: 1024)')
args = parser.parse_args()

# 🎯 Resolución de IP y host
try:
    ip = socket.gethostbyname(args.target)
    host = socket.gethostbyaddr(ip)[0]
except socket.gaierror:
    print(Fore.RED + "❌ No se pudo resolver el dominio.")
    exit()

print(Fore.CYAN + f"\n🎯 Escaneando: {ip} ({host})")
print(Fore.YELLOW + f"📡 Rango de puertos: {args.start_port} - {args.end_port}")

# 📁 Archivo de salida
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"nexus_scan_{ip.replace('.', '_')}_{timestamp}.txt"

# ✍️ Cabecera del archivo
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"📅 Scan: {datetime.now()}\n🎯 Objetivo: {ip} ({host})\n🔢 Puertos: {args.start_port} - {args.end_port}\n\n")

# 🧠 Función para obtener banner del servicio
def grab_banner(sock):
    try:
        sock.send(b"HEAD / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return None

# 🚪 Función de escaneo por puerto
def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                s.settimeout(1)
                banner = grab_banner(s)
                latencia = f" | Latencia: {round(s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) / 1000, 5)}s"
                banner_info = f" | Banner: {banner}" if banner else ""
                result = f"🔓 Puerto {port} ABIERTO{banner_info}"
                print(Fore.GREEN + result)
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(result + "\n")
    except:
        pass  # Silencio total para puertos cerrados

# ⚡ Escaneo en paralelo
print(Fore.CYAN + f"\n⏳ Escaneando puertos del {args.start_port} al {args.end_port}...\n")
with ThreadPoolExecutor(max_workers=100) as executor:
    list(track(executor.map(scan_port, range(args.start_port, args.end_port + 1)), description="🚀 Escaneando"))

# ✅ Final
ruta_absoluta = os.path.abspath(output_file)
print(Fore.MAGENTA + f"\n✅ Scan finalizado. Resultados guardados en: {ruta_absoluta}")
