#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password Cracker - Herramienta de fuerza bruta
Prueba contraseñas contra hashes o archivos protegidos
"""

import hashlib
import itertools
import string
import time
import sys
from threading import Thread
import queue

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class PasswordCracker:
	def __init__(self, hash_type='md5', max_length=6, charset=string.ascii_lowercase + string.digits):
		self.hash_type = hash_type.lower()
		self.max_length = max_length
		self.charset = charset
		self.found = False
		self.password = None
		self.attempts = 0
		self.start_time = None
	
	def hash_password(self, password):
		"""Genera hash de una contraseña"""
		password_bytes = password.encode('utf-8')
		
		if self.hash_type == 'md5':
			return hashlib.md5(password_bytes).hexdigest()
		elif self.hash_type == 'sha1':
			return hashlib.sha1(password_bytes).hexdigest()
		elif self.hash_type == 'sha256':
			return hashlib.sha256(password_bytes).hexdigest()
		elif self.hash_type == 'sha512':
			return hashlib.sha512(password_bytes).hexdigest()
		else:
			raise ValueError(f"Tipo de hash no soportado: {self.hash_type}")
	
	def crack_brute_force(self, target_hash, num_threads=4):
		"""Fuerza bruta con múltiples threads"""
		print(f"{Colors.BLUE}[*] Iniciando fuerza bruta...{Colors.END}")
		print(f"{Colors.BLUE}[*] Tipo de hash: {self.hash_type.upper()}{Colors.END}")
		print(f"{Colors.BLUE}[*] Longitud máxima: {self.max_length}{Colors.END}")
		print(f"{Colors.BLUE}[*] Charset: {len(self.charset)} caracteres{Colors.END}")
		print(f"{Colors.BLUE}[*] Threads: {num_threads}{Colors.END}\n")
		
		self.start_time = time.time()
		q = queue.Queue()
		
		# Generar todas las combinaciones posibles
		for length in range(1, self.max_length + 1):
			if self.found:
				break
			for combo in itertools.product(self.charset, repeat=length):
				if self.found:
					break
				q.put(''.join(combo))
		
		# Crear threads
		threads = []
		for _ in range(num_threads):
			t = Thread(target=self._worker, args=(q, target_hash))
			t.start()
			threads.append(t)
		
		# Esperar resultados
		while not self.found and not q.empty():
			time.sleep(0.1)
			if self.attempts % 10000 == 0 and self.attempts > 0:
				elapsed = time.time() - self.start_time
				rate = self.attempts / elapsed if elapsed > 0 else 0
				print(f"{Colors.YELLOW}[*] Intentos: {self.attempts:,} | Velocidad: {rate:.0f} hash/s{Colors.END}")
		
		# Detener threads
		for _ in range(num_threads):
			q.put(None)
		for t in threads:
			t.join()
		
		return self.password
	
	def _worker(self, q, target_hash):
		"""Worker thread para probar contraseñas"""
		while not self.found:
			try:
				password = q.get(timeout=1)
				if password is None:
					break
				
				self.attempts += 1
				hashed = self.hash_password(password)
				
				if hashed.lower() == target_hash.lower():
					self.found = True
					self.password = password
					elapsed = time.time() - self.start_time
					print(f"\n{Colors.GREEN}[+] ¡Contraseña encontrada!{Colors.END}")
					print(f"{Colors.GREEN}[+] Contraseña: {password}{Colors.END}")
					print(f"{Colors.GREEN}[+] Intentos: {self.attempts:,}{Colors.END}")
					print(f"{Colors.GREEN}[+] Tiempo: {elapsed:.2f} segundos{Colors.END}")
					break
				
				q.task_done()
			except queue.Empty:
				continue
	
	def crack_wordlist(self, target_hash, wordlist_file):
		"""Crack usando lista de palabras"""
		print(f"{Colors.BLUE}[*] Usando wordlist: {wordlist_file}{Colors.END}")
		print(f"{Colors.BLUE}[*] Tipo de hash: {self.hash_type.upper()}{Colors.END}\n")
		
		self.start_time = time.time()
		
		try:
			with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
				for line in f:
					if self.found:
						break
					
					password = line.strip()
					if not password:
						continue
					
					self.attempts += 1
					hashed = self.hash_password(password)
					
					if hashed.lower() == target_hash.lower():
						self.found = True
						self.password = password
						elapsed = time.time() - self.start_time
						print(f"\n{Colors.GREEN}[+] ¡Contraseña encontrada!{Colors.END}")
						print(f"{Colors.GREEN}[+] Contraseña: {password}{Colors.END}")
						print(f"{Colors.GREEN}[+] Intentos: {self.attempts:,}{Colors.END}")
						print(f"{Colors.GREEN}[+] Tiempo: {elapsed:.2f} segundos{Colors.END}")
						return password
					
					if self.attempts % 10000 == 0:
						elapsed = time.time() - self.start_time
						rate = self.attempts / elapsed if elapsed > 0 else 0
						print(f"{Colors.YELLOW}[*] Intentos: {self.attempts:,} | Velocidad: {rate:.0f} hash/s{Colors.END}")
		
		except FileNotFoundError:
			print(f"{Colors.RED}[!] Archivo no encontrado: {wordlist_file}{Colors.END}")
			return None
		
		if not self.found:
			print(f"\n{Colors.RED}[-] Contraseña no encontrada en la wordlist{Colors.END}")
			print(f"{Colors.RED}[-] Intentos: {self.attempts:,}{Colors.END}")
		
		return None

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║    Password Cracker - Fuerza Bruta    ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.YELLOW}Opciones:{Colors.END}")
	print("1. Fuerza bruta (combinaciones)")
	print("2. Wordlist (diccionario)")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-2): {Colors.END}").strip()
	
	if opcion not in ['1', '2']:
		print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
		return
	
	# Tipo de hash
	print(f"\n{Colors.YELLOW}Tipos de hash disponibles:{Colors.END}")
	print("1. MD5")
	print("2. SHA1")
	print("3. SHA256")
	print("4. SHA512")
	
	hash_opcion = input(f"\n{Colors.BLUE}Selecciona tipo de hash (1-4): {Colors.END}").strip()
	hash_map = {'1': 'md5', '2': 'sha1', '3': 'sha256', '4': 'sha512'}
	hash_type = hash_map.get(hash_opcion, 'md5')
	
	# Hash objetivo
	target_hash = input(f"\n{Colors.BLUE}Ingresa el hash a crackear: {Colors.END}").strip()
	if not target_hash:
		print(f"{Colors.RED}[!] Debes ingresar un hash{Colors.END}")
		return
	
	cracker = PasswordCracker(hash_type=hash_type)
	
	if opcion == '1':
		# Fuerza bruta
		max_len = input(f"{Colors.BLUE}Longitud máxima de contraseña (1-8): {Colors.END}").strip()
		try:
			max_len = int(max_len) if max_len else 6
			max_len = min(max(max_len, 1), 8)  # Limitar entre 1 y 8
		except:
			max_len = 6
		
		charset_opcion = input(f"{Colors.BLUE}Charset (1=minúsculas+números, 2=mayúsculas+minúsculas+números, 3=todos): {Colors.END}").strip()
		if charset_opcion == '2':
			cracker.charset = string.ascii_letters + string.digits
		elif charset_opcion == '3':
			cracker.charset = string.ascii_letters + string.digits + string.punctuation
		else:
			cracker.charset = string.ascii_lowercase + string.digits
		
		cracker.max_length = max_len
		cracker.crack_brute_force(target_hash)
	
	elif opcion == '2':
		# Wordlist
		wordlist = input(f"{Colors.BLUE}Ruta del archivo wordlist: {Colors.END}").strip()
		if not wordlist:
			print(f"{Colors.RED}[!] Debes ingresar una ruta de wordlist{Colors.END}")
			return
		cracker.crack_wordlist(target_hash, wordlist)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.RED}[!] Interrumpido por el usuario{Colors.END}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		sys.exit(1)

