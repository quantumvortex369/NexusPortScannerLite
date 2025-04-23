NexusPortScannerLite es un escáner de puertos ultraligero, escrito en Python, diseñado para ser rápido, limpio y fácil de usar desde la terminal.
Ideal tanto para principiantes que están aprendiendo sobre redes como para entusiastas de la ciberseguridad que quieren una herramienta sencilla pero efectiva para identificar servicios expuestos en un objetivo.


Características
-Escaneo de puertos TCP rápido y multihilo

-Detección de banners básicos de servicios

-Modo silencioso: solo muestra puertos abiertos

-Registro automático de resultados en un archivo de texto con timestamp

-Uso simple con argumentos por CLI

-Compatibilidad con dominios e IPs

-Valores por defecto para lanzarlo sin complicaciones


📦 Requisitos
-Python 3.7 o superior

-Bibliotecas: colorama, rich


Instálalos con:

pip install colorama rich

Uso:
python NexusPortScannerLite.py -t <objetivo> -sp <puerto_inicial> -ep <puerto_final>

Ejemplo:
python NexusPortScannerLite.py -t 192.168.1.1 -sp 20 -ep 80

Los resultados se guardan automáticamente en un archivo con nombre tipo:
nexus_scan_127_0_0_1_20250423_123456.txt
