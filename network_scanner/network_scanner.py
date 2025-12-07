#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Scanner - Escáner de red completo
Escanea la red local y muestra dispositivos conectados
"""

import socket
import subprocess
import sys
import platform
from ipaddress import ip_network
import threading
import queue

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	END = '\033[0m'
	BOLD = '\033[1m'

def get_local_ip():
	"""Obtiene la IP local de la máquina"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip = s.getsockname()[0]
		s.close()
		return ip
	except:
		return "127.0.0.1"

def get_network_range(ip):
	"""Obtiene el rango de red basado en la IP"""
	parts = ip.split('.')
	return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

def scan_port(host, port, timeout=0.5):
	"""Escanea un puerto específico"""
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout)
		result = sock.connect_ex((host, port))
		sock.close()
		return result == 0
	except:
		return False

def get_hostname(ip):
	"""Intenta obtener el hostname de una IP"""
	try:
		return socket.gethostbyaddr(ip)[0]
	except:
		return "N/A"

def ping_host(ip):
	"""Verifica si un host está activo mediante ping"""
	param = '-n' if platform.system().lower() == 'windows' else '-c'
	command = ['ping', param, '1', '-w', '1000', ip] if platform.system().lower() == 'windows' else ['ping', param, '1', '-W', '1', ip]
	return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def scan_host(ip, ports=[22, 23, 80, 443, 3389, 8080]):
	"""Escanea un host y sus puertos"""
	if not ping_host(ip):
		return None
	
	hostname = get_hostname(ip)
	open_ports = []
	
	for port in ports:
		if scan_port(ip, port):
			open_ports.append(port)
	
	return {
		'ip': ip,
		'hostname': hostname,
		'ports': open_ports,
		'active': True
	}

def worker(q, results, ports):
	"""Worker thread para escaneo paralelo"""
	while True:
		ip = q.get()
		if ip is None:
			break
		result = scan_host(ip, ports)
		if result:
			results.append(result)
		q.task_done()

def scan_network(network_range, ports=[22, 23, 80, 443, 3389, 8080], threads=50):
	"""Escanea una red completa"""
	print(f"{Colors.BLUE}[*] Escaneando red: {network_range}{Colors.END}")
	print(f"{Colors.BLUE}[*] Puertos a escanear: {', '.join(map(str, ports))}{Colors.END}")
	print(f"{Colors.BLUE}[*] Hilos: {threads}{Colors.END}\n")
	
	network = ip_network(network_range, strict=False)
	q = queue.Queue()
	results = []
	
	# Crear threads
	thread_list = []
	for _ in range(threads):
		t = threading.Thread(target=worker, args=(q, results, ports))
		t.start()
		thread_list.append(t)
	
	# Agregar IPs a la cola
	for ip in network.hosts():
		q.put(str(ip))
	
	# Esperar a que terminen
	q.join()
	
	# Detener threads
	for _ in range(threads):
		q.put(None)
	for t in thread_list:
		t.join()
	
	return results

def main():
	print(f"{Colors.BOLD}{Colors.BLUE}")
	print("╔════════════════════════════════════════╗")
	print("║     Network Scanner - Escáner de Red  ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	# Obtener IP local
	local_ip = get_local_ip()
	network_range = get_network_range(local_ip)
	
	print(f"{Colors.GREEN}[+] IP Local: {local_ip}{Colors.END}")
	print(f"{Colors.GREEN}[+] Rango de red: {network_range}{Colors.END}\n")
	
	# Configurar puertos
	puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
	
	# Escanear
	results = scan_network(network_range, puertos_comunes, threads=50)
	
	# Mostrar resultados
	print(f"\n{Colors.BOLD}{Colors.GREEN}[*] Resultados del escaneo:{Colors.END}\n")
	print(f"{'IP':<18} {'Hostname':<30} {'Puertos Abiertos':<50}")
	print("-" * 100)
	
	for result in results:
		ports_str = ', '.join(map(str, result['ports'])) if result['ports'] else 'Ninguno'
		print(f"{Colors.GREEN}{result['ip']:<18}{Colors.END} {result['hostname']:<30} {ports_str}")
	
	print(f"\n{Colors.GREEN}[+] Total de hosts activos encontrados: {len(results)}{Colors.END}")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.RED}[!] Escaneo interrumpido por el usuario{Colors.END}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		sys.exit(1)

