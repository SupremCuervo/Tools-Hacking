#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Encryptor - Encriptador de archivos
Encripta y desencripta archivos usando AES
"""

import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class FileEncryptor:
	def __init__(self, password):
		self.password = password.encode()
		self.key = self._derive_key()
		self.cipher = Fernet(self.key)
	
	def _derive_key(self):
		"""Deriva una clave desde la contraseña"""
		salt = b'fixed_salt_for_demo'  # En producción, usa salt aleatorio
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=100000,
		)
		key = base64.urlsafe_b64encode(kdf.derive(self.password))
		return key
	
	def encrypt_file(self, file_path):
		"""Encripta un archivo"""
		if not os.path.exists(file_path):
			print(f"{Colors.RED}[!] Archivo no encontrado: {file_path}{Colors.END}")
			return False
		
		try:
			with open(file_path, 'rb') as f:
				data = f.read()
			
			encrypted_data = self.cipher.encrypt(data)
			
			output_path = file_path + '.encrypted'
			with open(output_path, 'wb') as f:
				f.write(encrypted_data)
			
			print(f"{Colors.GREEN}[+] Archivo encriptado: {output_path}{Colors.END}")
			return True
		except Exception as e:
			print(f"{Colors.RED}[!] Error encriptando: {e}{Colors.END}")
			return False
	
	def decrypt_file(self, file_path, output_path=None):
		"""Desencripta un archivo"""
		if not os.path.exists(file_path):
			print(f"{Colors.RED}[!] Archivo no encontrado: {file_path}{Colors.END}")
			return False
		
		try:
			with open(file_path, 'rb') as f:
				encrypted_data = f.read()
			
			decrypted_data = self.cipher.decrypt(encrypted_data)
			
			if not output_path:
				if file_path.endswith('.encrypted'):
					output_path = file_path[:-10]  # Remover .encrypted
				else:
					output_path = file_path + '.decrypted'
			
			with open(output_path, 'wb') as f:
				f.write(decrypted_data)
			
			print(f"{Colors.GREEN}[+] Archivo desencriptado: {output_path}{Colors.END}")
			return True
		except Exception as e:
			print(f"{Colors.RED}[!] Error desencriptando: {e}{Colors.END}")
			return False
	
	def encrypt_directory(self, dir_path):
		"""Encripta todos los archivos en un directorio"""
		if not os.path.isdir(dir_path):
			print(f"{Colors.RED}[!] Directorio no encontrado: {dir_path}{Colors.END}")
			return False
		
		encrypted_count = 0
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.encrypted'):
					continue
				file_path = os.path.join(root, file)
				print(f"{Colors.BLUE}[*] Encriptando: {file_path}{Colors.END}")
				if self.encrypt_file(file_path):
					encrypted_count += 1
		
		print(f"\n{Colors.GREEN}[+] Archivos encriptados: {encrypted_count}{Colors.END}")
		return True

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║      File Encryptor - Encriptador      ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.YELLOW}Opciones:{Colors.END}")
	print("1. Encriptar archivo")
	print("2. Desencriptar archivo")
	print("3. Encriptar directorio")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-3): {Colors.END}").strip()
	
	password = input(f"{Colors.BLUE}Ingresa la contraseña: {Colors.END}").strip()
	if not password:
		print(f"{Colors.RED}[!] Debes ingresar una contraseña{Colors.END}")
		return
	
	encryptor = FileEncryptor(password)
	
	if opcion == '1':
		file_path = input(f"{Colors.BLUE}Ruta del archivo a encriptar: {Colors.END}").strip()
		if file_path:
			encryptor.encrypt_file(file_path)
	
	elif opcion == '2':
		file_path = input(f"{Colors.BLUE}Ruta del archivo encriptado: {Colors.END}").strip()
		if file_path:
			output = input(f"{Colors.BLUE}Ruta de salida (Enter para auto): {Colors.END}").strip()
			encryptor.decrypt_file(file_path, output if output else None)
	
	elif opcion == '3':
		dir_path = input(f"{Colors.BLUE}Ruta del directorio a encriptar: {Colors.END}").strip()
		if dir_path:
			confirm = input(f"{Colors.YELLOW}¿Encriptar todos los archivos? (s/n): {Colors.END}").strip().lower()
			if confirm == 's':
				encryptor.encrypt_directory(dir_path)
	
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

