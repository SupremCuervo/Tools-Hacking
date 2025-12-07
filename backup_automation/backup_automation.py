#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backup Automation - Automatizador de respaldos
Crea respaldos automáticos de archivos y directorios
"""

import os
import shutil
import sys
from datetime import datetime
import zipfile
import json

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class BackupAutomation:
	def __init__(self, backup_dir="backups"):
		self.backup_dir = backup_dir
		if not os.path.exists(backup_dir):
			os.makedirs(backup_dir)
	
	def create_backup(self, source_path, backup_name=None, compress=True):
		"""Crea un respaldo de un archivo o directorio"""
		if not os.path.exists(source_path):
			print(f"{Colors.RED}[!] Ruta no encontrada: {source_path}{Colors.END}")
			return False
		
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		if not backup_name:
			backup_name = os.path.basename(source_path)
		
		backup_filename = f"{backup_name}_{timestamp}"
		
		try:
			if os.path.isfile(source_path):
				# Backup de archivo
				if compress:
					backup_path = os.path.join(self.backup_dir, f"{backup_filename}.zip")
					with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
						zipf.write(source_path, os.path.basename(source_path))
				else:
					backup_path = os.path.join(self.backup_dir, backup_filename)
					shutil.copy2(source_path, backup_path)
			
			else:
				# Backup de directorio
				if compress:
					backup_path = os.path.join(self.backup_dir, f"{backup_filename}.zip")
					with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
						for root, dirs, files in os.walk(source_path):
							for file in files:
								file_path = os.path.join(root, file)
								arcname = os.path.relpath(file_path, source_path)
								zipf.write(file_path, arcname)
				else:
					backup_path = os.path.join(self.backup_dir, backup_filename)
					shutil.copytree(source_path, backup_path)
			
			size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
			print(f"{Colors.GREEN}[+] Backup creado: {backup_path}{Colors.END}")
			print(f"{Colors.GREEN}[+] Tamaño: {size:.2f} MB{Colors.END}")
			
			# Guardar metadata
			self._save_metadata(backup_path, source_path, timestamp)
			return True
		
		except Exception as e:
			print(f"{Colors.RED}[!] Error creando backup: {e}{Colors.END}")
			return False
	
	def _save_metadata(self, backup_path, source_path, timestamp):
		"""Guarda metadata del backup"""
		metadata = {
			'backup_path': backup_path,
			'source_path': source_path,
			'timestamp': timestamp,
			'size': os.path.getsize(backup_path)
		}
		
		metadata_file = backup_path + '.meta'
		with open(metadata_file, 'w') as f:
			json.dump(metadata, f, indent=2)
	
	def list_backups(self):
		"""Lista todos los backups"""
		backups = []
		for file in os.listdir(self.backup_dir):
			if file.endswith('.meta'):
				meta_path = os.path.join(self.backup_dir, file)
				with open(meta_path, 'r') as f:
					metadata = json.load(f)
					backups.append(metadata)
		
		backups.sort(key=lambda x: x['timestamp'], reverse=True)
		return backups
	
	def restore_backup(self, backup_path, restore_to=None):
		"""Restaura un backup"""
		if not os.path.exists(backup_path):
			print(f"{Colors.RED}[!] Backup no encontrado: {backup_path}{Colors.END}")
			return False
		
		try:
			if backup_path.endswith('.zip'):
				# Restaurar desde ZIP
				if not restore_to:
					restore_to = backup_path[:-4]  # Remover .zip
				
				with zipfile.ZipFile(backup_path, 'r') as zipf:
					zipf.extractall(restore_to)
				
				print(f"{Colors.GREEN}[+] Backup restaurado en: {restore_to}{Colors.END}")
			else:
				# Restaurar directorio
				if not restore_to:
					restore_to = os.path.dirname(backup_path)
				
				if os.path.isdir(backup_path):
					dest = os.path.join(restore_to, os.path.basename(backup_path))
					if os.path.exists(dest):
						shutil.rmtree(dest)
					shutil.copytree(backup_path, dest)
					print(f"{Colors.GREEN}[+] Backup restaurado en: {dest}{Colors.END}")
			
			return True
		
		except Exception as e:
			print(f"{Colors.RED}[!] Error restaurando backup: {e}{Colors.END}")
			return False
	
	def cleanup_old_backups(self, days=30):
		"""Elimina backups más antiguos que X días"""
		import time
		cutoff_time = time.time() - (days * 24 * 60 * 60)
		deleted = 0
		
		for file in os.listdir(self.backup_dir):
			file_path = os.path.join(self.backup_dir, file)
			if os.path.isfile(file_path):
				if os.path.getmtime(file_path) < cutoff_time:
					os.remove(file_path)
					if file.endswith('.meta'):
						# También eliminar el backup asociado
						backup_file = file_path[:-5]
						if os.path.exists(backup_file):
							os.remove(backup_file)
					deleted += 1
		
		print(f"{Colors.GREEN}[+] Backups eliminados: {deleted}{Colors.END}")
		return deleted

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║    Backup Automation - Automatizador   ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	backup_dir = input(f"{Colors.BLUE}Directorio de backups (default: backups): {Colors.END}").strip()
	if not backup_dir:
		backup_dir = "backups"
	
	automation = BackupAutomation(backup_dir)
	
	print(f"\n{Colors.YELLOW}Opciones:{Colors.END}")
	print("1. Crear backup")
	print("2. Listar backups")
	print("3. Restaurar backup")
	print("4. Limpiar backups antiguos")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-4): {Colors.END}").strip()
	
	if opcion == '1':
		source = input(f"{Colors.BLUE}Ruta a respaldar: {Colors.END}").strip()
		if source:
			name = input(f"{Colors.BLUE}Nombre del backup (Enter para auto): {Colors.END}").strip()
			compress = input(f"{Colors.BLUE}¿Comprimir? (s/n, default: s): {Colors.END}").strip().lower()
			automation.create_backup(source, name if name else None, compress != 'n')
	
	elif opcion == '2':
		backups = automation.list_backups()
		print(f"\n{Colors.GREEN}[*] Backups encontrados: {len(backups)}{Colors.END}\n")
		for i, backup in enumerate(backups, 1):
			size_mb = backup['size'] / (1024 * 1024)
			print(f"{i}. {os.path.basename(backup['backup_path'])}")
			print(f"   Origen: {backup['source_path']}")
			print(f"   Fecha: {backup['timestamp']}")
			print(f"   Tamaño: {size_mb:.2f} MB\n")
	
	elif opcion == '3':
		backup_path = input(f"{Colors.BLUE}Ruta del backup a restaurar: {Colors.END}").strip()
		if backup_path:
			restore_to = input(f"{Colors.BLUE}¿Dónde restaurar? (Enter para auto): {Colors.END}").strip()
			automation.restore_backup(backup_path, restore_to if restore_to else None)
	
	elif opcion == '4':
		days = input(f"{Colors.BLUE}Eliminar backups más antiguos que (días, default: 30): {Colors.END}").strip()
		try:
			days = int(days) if days else 30
			automation.cleanup_old_backups(days)
		except:
			print(f"{Colors.RED}[!] Días inválidos{Colors.END}")
	
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

