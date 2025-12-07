#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Monitor - Monitor del sistema
Monitorea CPU, memoria, disco y red en tiempo real
"""

import psutil
import time
import os
import sys
from datetime import datetime

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def format_bytes(bytes):
	"""Formatea bytes a formato legible"""
	for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
		if bytes < 1024.0:
			return f"{bytes:.2f} {unit}"
		bytes /= 1024.0
	return f"{bytes:.2f} PB"

def get_cpu_info():
	"""Obtiene información de CPU"""
	cpu_percent = psutil.cpu_percent(interval=1)
	cpu_count = psutil.cpu_count()
	cpu_freq = psutil.cpu_freq()
	
	return {
		'percent': cpu_percent,
		'count': cpu_count,
		'freq': cpu_freq.current if cpu_freq else 'N/A'
	}

def get_memory_info():
	"""Obtiene información de memoria"""
	mem = psutil.virtual_memory()
	swap = psutil.swap_memory()
	
	return {
		'total': mem.total,
		'used': mem.used,
		'free': mem.free,
		'percent': mem.percent,
		'swap_total': swap.total,
		'swap_used': swap.used,
		'swap_percent': swap.percent
	}

def get_disk_info():
	"""Obtiene información de disco"""
	disks = []
	for partition in psutil.disk_partitions():
		try:
			usage = psutil.disk_usage(partition.mountpoint)
			disks.append({
				'device': partition.device,
				'mountpoint': partition.mountpoint,
				'fstype': partition.fstype,
				'total': usage.total,
				'used': usage.used,
				'free': usage.free,
				'percent': usage.percent
			})
		except PermissionError:
			continue
	return disks

def get_network_info():
	"""Obtiene información de red"""
	net_io = psutil.net_io_counters()
	net_if = psutil.net_if_addrs()
	
	interfaces = []
	for interface_name, addresses in net_if.items():
		for addr in addresses:
			if addr.family == 2:  # IPv4
				interfaces.append({
					'name': interface_name,
					'ip': addr.address,
					'netmask': addr.netmask
				})
	
	return {
		'bytes_sent': net_io.bytes_sent,
		'bytes_recv': net_io.bytes_recv,
		'packets_sent': net_io.packets_sent,
		'packets_recv': net_io.packets_recv,
		'interfaces': interfaces
	}

def get_processes_info():
	"""Obtiene información de procesos"""
	processes = []
	for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
		try:
			processes.append(proc.info)
		except (psutil.NoSuchProcess, psutil.AccessDenied):
			continue
	
	# Ordenar por uso de CPU
	processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
	return processes[:10]  # Top 10

def print_dashboard():
	"""Imprime el dashboard completo"""
	clear_screen()
	
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔═══════════════════════════════════════════════════════╗")
	print("║            System Monitor - Monitor del Sistema      ║")
	print("╚═══════════════════════════════════════════════════════╝")
	print(f"{Colors.END}")
	print(f"{Colors.BLUE}Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")
	
	# CPU
	cpu = get_cpu_info()
	cpu_color = Colors.GREEN if cpu['percent'] < 50 else Colors.YELLOW if cpu['percent'] < 80 else Colors.RED
	print(f"{Colors.BOLD}CPU:{Colors.END}")
	print(f"  Uso: {cpu_color}{cpu['percent']:.1f}%{Colors.END}")
	print(f"  Núcleos: {cpu['count']}")
	print(f"  Frecuencia: {cpu['freq']} MHz\n")
	
	# Memoria
	mem = get_memory_info()
	mem_color = Colors.GREEN if mem['percent'] < 70 else Colors.YELLOW if mem['percent'] < 90 else Colors.RED
	print(f"{Colors.BOLD}Memoria:{Colors.END}")
	print(f"  Total: {format_bytes(mem['total'])}")
	print(f"  Usada: {mem_color}{format_bytes(mem['used'])} ({mem['percent']:.1f}%){Colors.END}")
	print(f"  Libre: {format_bytes(mem['free'])}")
	print(f"  Swap: {format_bytes(mem['swap_used'])} / {format_bytes(mem['swap_total'])} ({mem['swap_percent']:.1f}%)\n")
	
	# Disco
	disks = get_disk_info()
	print(f"{Colors.BOLD}Discos:{Colors.END}")
	for disk in disks[:3]:  # Mostrar primeros 3
		disk_color = Colors.GREEN if disk['percent'] < 70 else Colors.YELLOW if disk['percent'] < 90 else Colors.RED
		print(f"  {disk['device']} ({disk['mountpoint']})")
		print(f"    Usado: {disk_color}{format_bytes(disk['used'])} / {format_bytes(disk['total'])} ({disk['percent']:.1f}%){Colors.END}\n")
	
	# Red
	net = get_network_info()
	print(f"{Colors.BOLD}Red:{Colors.END}")
	print(f"  Enviado: {format_bytes(net['bytes_sent'])}")
	print(f"  Recibido: {format_bytes(net['bytes_recv'])}")
	print(f"  Paquetes enviados: {net['packets_sent']:,}")
	print(f"  Paquetes recibidos: {net['packets_recv']:,}")
	if net['interfaces']:
		print(f"  Interfaces:")
		for iface in net['interfaces'][:3]:
			print(f"    {iface['name']}: {iface['ip']}\n")
	
	# Procesos
	processes = get_processes_info()
	print(f"{Colors.BOLD}Top 10 Procesos (por CPU):{Colors.END}")
	print(f"{'PID':<8} {'Nombre':<25} {'CPU %':<10} {'Mem %':<10}")
	print("-" * 55)
	for proc in processes:
		cpu_p = proc['cpu_percent'] or 0
		mem_p = proc['memory_percent'] or 0
		print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {cpu_p:<10.1f} {mem_p:<10.1f}")

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║      System Monitor - Monitor          ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	interval = input(f"{Colors.BLUE}Intervalo de actualización (segundos, default: 2): {Colors.END}").strip()
	try:
		interval = float(interval) if interval else 2.0
	except:
		interval = 2.0
	
	print(f"\n{Colors.YELLOW}[!] Presiona Ctrl+C para salir{Colors.END}\n")
	time.sleep(1)
	
	try:
		while True:
			print_dashboard()
			time.sleep(interval)
	except KeyboardInterrupt:
		print(f"\n{Colors.YELLOW}[!] Monitor detenido{Colors.END}")

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		print(f"{Colors.RED}[!] Asegúrate de tener psutil instalado: pip install psutil{Colors.END}")
		sys.exit(1)

