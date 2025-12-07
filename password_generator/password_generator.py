#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password Generator - Generador de contraseñas
Genera contraseñas seguras y personalizables
"""

import random
import string
import secrets
import sys

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class PasswordGenerator:
	def __init__(self):
		self.lowercase = string.ascii_lowercase
		self.uppercase = string.ascii_uppercase
		self.digits = string.digits
		self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
	
	def generate(self, length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True, exclude_similar=True):
		"""Genera una contraseña segura"""
		charset = ""
		
		if use_lower:
			charset += self.lowercase
		if use_upper:
			charset += self.uppercase
		if use_digits:
			charset += self.digits
		if use_special:
			charset += self.special
		
		if not charset:
			raise ValueError("Debes seleccionar al menos un tipo de carácter")
		
		# Excluir caracteres similares
		if exclude_similar:
			similar = "il1Lo0O"
			charset = ''.join(c for c in charset if c not in similar)
		
		# Asegurar que tenga al menos un carácter de cada tipo seleccionado
		password = []
		if use_lower:
			password.append(secrets.choice(self.lowercase))
		if use_upper:
			password.append(secrets.choice(self.uppercase))
		if use_digits:
			password.append(secrets.choice(self.digits))
		if use_special:
			password.append(secrets.choice(self.special))
		
		# Completar con caracteres aleatorios
		remaining = length - len(password)
		for _ in range(remaining):
			password.append(secrets.choice(charset))
		
		# Mezclar
		random.shuffle(password)
		return ''.join(password)
	
	def generate_memorable(self, word_count=4, separator="-", capitalize=True):
		"""Genera una contraseña memorable usando palabras"""
		words = [
			"gato", "perro", "casa", "arbol", "sol", "luna", "estrella",
			"mar", "rio", "montana", "cielo", "nube", "viento", "fuego",
			"agua", "tierra", "flor", "hoja", "fruto", "semilla",
			"leon", "tigre", "oso", "pajaro", "pez", "mariposa",
			"rojo", "azul", "verde", "amarillo", "naranja", "morado"
		]
		
		selected = secrets.SystemRandom().sample(words, word_count)
		
		if capitalize:
			selected = [w.capitalize() for w in selected]
		
		password = separator.join(selected)
		
		# Agregar número y símbolo
		password += str(secrets.randbelow(100))
		password += secrets.choice("!@#$%")
		
		return password
	
	def calculate_entropy(self, password):
		"""Calcula la entropía de una contraseña"""
		charset_size = 0
		if any(c in self.lowercase for c in password):
			charset_size += 26
		if any(c in self.uppercase for c in password):
			charset_size += 26
		if any(c in self.digits for c in password):
			charset_size += 10
		if any(c in self.special for c in password):
			charset_size += len(self.special)
		
		if charset_size == 0:
			return 0
		
		entropy = len(password) * (charset_size.bit_length() - 1)
		return entropy
	
	def strength_check(self, password):
		"""Verifica la fortaleza de una contraseña"""
		score = 0
		feedback = []
		
		if len(password) >= 8:
			score += 1
		else:
			feedback.append("Muy corta (mínimo 8 caracteres)")
		
		if len(password) >= 12:
			score += 1
		if len(password) >= 16:
			score += 1
		
		if any(c in self.lowercase for c in password):
			score += 1
		else:
			feedback.append("Falta minúsculas")
		
		if any(c in self.uppercase for c in password):
			score += 1
		else:
			feedback.append("Falta mayúsculas")
		
		if any(c in self.digits for c in password):
			score += 1
		else:
			feedback.append("Falta números")
		
		if any(c in self.special for c in password):
			score += 1
		else:
			feedback.append("Falta caracteres especiales")
		
		if len(set(password)) < len(password) * 0.7:
			feedback.append("Muchos caracteres repetidos")
		else:
			score += 1
		
		strength_levels = ["Muy débil", "Débil", "Regular", "Fuerte", "Muy fuerte", "Extremadamente fuerte"]
		strength = strength_levels[min(score, len(strength_levels) - 1)]
		
		return strength, score, feedback

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║   Password Generator - Generador       ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.YELLOW}Tipos de contraseña:{Colors.END}")
	print("1. Contraseña segura (aleatoria)")
	print("2. Contraseña memorable (palabras)")
	print("3. Verificar fortaleza de contraseña")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-3): {Colors.END}").strip()
	
	generator = PasswordGenerator()
	
	if opcion == '1':
		length = input(f"{Colors.BLUE}Longitud (default: 16): {Colors.END}").strip()
		try:
			length = int(length) if length else 16
		except:
			length = 16
		
		use_upper = input(f"{Colors.BLUE}¿Incluir mayúsculas? (s/n, default: s): {Colors.END}").strip().lower() != 'n'
		use_lower = input(f"{Colors.BLUE}¿Incluir minúsculas? (s/n, default: s): {Colors.END}").strip().lower() != 'n'
		use_digits = input(f"{Colors.BLUE}¿Incluir números? (s/n, default: s): {Colors.END}").strip().lower() != 'n'
		use_special = input(f"{Colors.BLUE}¿Incluir especiales? (s/n, default: s): {Colors.END}").strip().lower() != 'n'
		exclude_similar = input(f"{Colors.BLUE}¿Excluir similares (i, l, 1, L, o, O, 0)? (s/n, default: s): {Colors.END}").strip().lower() != 'n'
		
		count = input(f"{Colors.BLUE}¿Cuántas contraseñas generar? (default: 1): {Colors.END}").strip()
		try:
			count = int(count) if count else 1
		except:
			count = 1
		
		print(f"\n{Colors.GREEN}[+] Contraseñas generadas:{Colors.END}\n")
		for i in range(count):
			password = generator.generate(length, use_upper, use_lower, use_digits, use_special, exclude_similar)
			entropy = generator.calculate_entropy(password)
			print(f"{i+1}. {Colors.CYAN}{password}{Colors.END} (Entropía: {entropy} bits)")
	
	elif opcion == '2':
		word_count = input(f"{Colors.BLUE}Número de palabras (default: 4): {Colors.END}").strip()
		try:
			word_count = int(word_count) if word_count else 4
		except:
			word_count = 4
		
		separator = input(f"{Colors.BLUE}Separador (default: -): {Colors.END}").strip() or "-"
		capitalize = input(f"{Colors.BLUE}¿Capitalizar palabras? (s/n, default: s): {Colors.END}").strip().lower() != 'n'
		
		password = generator.generate_memorable(word_count, separator, capitalize)
		entropy = generator.calculate_entropy(password)
		strength, score, _ = generator.strength_check(password)
		
		print(f"\n{Colors.GREEN}[+] Contraseña memorable:{Colors.END}")
		print(f"{Colors.CYAN}{password}{Colors.END}")
		print(f"Entropía: {entropy} bits")
		print(f"Fortaleza: {strength}")
	
	elif opcion == '3':
		password = input(f"{Colors.BLUE}Ingresa la contraseña a verificar: {Colors.END}").strip()
		if password:
			strength, score, feedback = generator.strength_check(password)
			entropy = generator.calculate_entropy(password)
			
			strength_color = Colors.RED if score < 3 else Colors.YELLOW if score < 5 else Colors.GREEN
			
			print(f"\n{Colors.BOLD}Análisis de contraseña:{Colors.END}")
			print(f"  Contraseña: {Colors.CYAN}{password}{Colors.END}")
			print(f"  Longitud: {len(password)} caracteres")
			print(f"  Entropía: {entropy} bits")
			print(f"  Fortaleza: {strength_color}{strength}{Colors.END} (Puntuación: {score}/8)")
			
			if feedback:
				print(f"\n{Colors.YELLOW}Recomendaciones:{Colors.END}")
				for item in feedback:
					print(f"  - {item}")
	
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

