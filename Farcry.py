#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Farcry - Herramientas de Seguridad y Hacking
Script interactivo con menú para diversas utilidades de seguridad
"""

import os
import sys
import subprocess
import socket
import requests
import base64
from datetime import datetime
import platform

# Colores para terminal
class Colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def clear_screen():
	"""Limpia la pantalla según el sistema operativo"""
	if platform.system() == "Windows":
		os.system('cls')
	else:
		os.system('clear')

def print_banner():
	"""Muestra el banner del programa"""
	banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          ███████╗ █████╗ ██████╗  ██████╗██████╗    ║
║          ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗   ║
║          █████╗  ███████║██████╔╝██║     ██████╔╝   ║
║          ██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██╗   ║
║          ██║     ██║  ██║██║  ██║╚██████╗██║  ██║   ║
║          ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ║
║                                                       ║
║          Herramientas de Seguridad y Hacking         ║
╚═══════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
	print(banner)

def escanear_puertos():
	"""Escanea puertos abiertos en un host"""
	print(f"\n{Colors.OKCYAN}[*] Escaneo de Puertos{Colors.ENDC}")
	print("=" * 50)
	
	host = input(f"{Colors.WARNING}Ingresa la IP o dominio a escanear: {Colors.ENDC}").strip()
	if not host:
		print(f"{Colors.FAIL}[!] Debes ingresar un host válido{Colors.ENDC}")
		return
	
	try:
		puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
		print(f"\n{Colors.OKBLUE}Escaneando puertos comunes en {host}...{Colors.ENDC}\n")
		
		puertos_abiertos = []
		for puerto in puertos_comunes:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.5)
			resultado = sock.connect_ex((host, puerto))
			if resultado == 0:
				puertos_abiertos.append(puerto)
				print(f"{Colors.OKGREEN}[+] Puerto {puerto} ABIERTO{Colors.ENDC}")
			sock.close()
		
		if not puertos_abiertos:
			print(f"{Colors.WARNING}[-] No se encontraron puertos abiertos{Colors.ENDC}")
		else:
			print(f"\n{Colors.OKGREEN}[*] Total de puertos abiertos: {len(puertos_abiertos)}{Colors.ENDC}")
			
	except socket.gaierror:
		print(f"{Colors.FAIL}[!] Error: No se pudo resolver el host{Colors.ENDC}")
	except Exception as e:
		print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def obtener_info_ip():
	"""Obtiene información sobre una IP"""
	print(f"\n{Colors.OKCYAN}[*] Información de IP{Colors.ENDC}")
	print("=" * 50)
	
	ip = input(f"{Colors.WARNING}Ingresa la IP a consultar: {Colors.ENDC}").strip()
	if not ip:
		print(f"{Colors.FAIL}[!] Debes ingresar una IP válida{Colors.ENDC}")
		return
	
	try:
		print(f"\n{Colors.OKBLUE}Consultando información de {ip}...{Colors.ENDC}\n")
		
		# Información básica
		print(f"{Colors.BOLD}Información básica:{Colors.ENDC}")
		print(f"  IP: {ip}")
		
		# Resolución DNS inversa
		try:
			hostname = socket.gethostbyaddr(ip)[0]
			print(f"  Hostname: {hostname}")
		except:
			print(f"  Hostname: No disponible")
		
		# Consulta a API externa (ip-api.com)
		try:
			response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
			if response.status_code == 200:
				data = response.json()
				if data['status'] == 'success':
					print(f"\n{Colors.BOLD}Información geográfica:{Colors.ENDC}")
					print(f"  País: {data.get('country', 'N/A')}")
					print(f"  Región: {data.get('regionName', 'N/A')}")
					print(f"  Ciudad: {data.get('city', 'N/A')}")
					print(f"  ISP: {data.get('isp', 'N/A')}")
					print(f"  Organización: {data.get('org', 'N/A')}")
					print(f"  Latitud: {data.get('lat', 'N/A')}")
					print(f"  Longitud: {data.get('lon', 'N/A')}")
		except:
			print(f"{Colors.WARNING}[!] No se pudo obtener información geográfica{Colors.ENDC}")
			
	except Exception as e:
		print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def crear_imagen_desofuscada():
	"""Crea una imagen desofuscada desde datos codificados"""
	print(f"\n{Colors.OKCYAN}[*] Crear Imagen Desofuscada{Colors.ENDC}")
	print("=" * 50)
	
	print(f"\n{Colors.WARNING}Opciones:{Colors.ENDC}")
	print("1. Desde Base64")
	print("2. Desde archivo binario")
	
	opcion = input(f"\n{Colors.WARNING}Selecciona una opción (1-2): {Colors.ENDC}").strip()
	
	if opcion == "1":
		# Desde Base64
		base64_data = input(f"{Colors.WARNING}Ingresa el string Base64: {Colors.ENDC}").strip()
		if not base64_data:
			print(f"{Colors.FAIL}[!] Debes ingresar datos Base64{Colors.ENDC}")
			return
		
		try:
			# Decodificar Base64
			imagen_data = base64.b64decode(base64_data)
			
			# Guardar imagen
			nombre_archivo = f"imagen_desofuscada_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
			with open(nombre_archivo, 'wb') as f:
				f.write(imagen_data)
			
			print(f"{Colors.OKGREEN}[+] Imagen guardada como: {nombre_archivo}{Colors.ENDC}")
			
		except Exception as e:
			print(f"{Colors.FAIL}[!] Error al decodificar: {e}{Colors.ENDC}")
	
	elif opcion == "2":
		# Desde archivo binario
		ruta_archivo = input(f"{Colors.WARNING}Ingresa la ruta del archivo binario: {Colors.ENDC}").strip()
		if not os.path.exists(ruta_archivo):
			print(f"{Colors.FAIL}[!] El archivo no existe{Colors.ENDC}")
			return
		
		try:
			with open(ruta_archivo, 'rb') as f:
				datos = f.read()
			
			# Intentar detectar el tipo de imagen por header
			extension = ".bin"
			if datos.startswith(b'\x89PNG'):
				extension = ".png"
			elif datos.startswith(b'\xff\xd8\xff'):
				extension = ".jpg"
			elif datos.startswith(b'GIF'):
				extension = ".gif"
			elif datos.startswith(b'BM'):
				extension = ".bmp"
			
			nombre_archivo = f"imagen_desofuscada_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
			with open(nombre_archivo, 'wb') as f:
				f.write(datos)
			
			print(f"{Colors.OKGREEN}[+] Imagen guardada como: {nombre_archivo}{Colors.ENDC}")
			
		except Exception as e:
			print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
	
	else:
		print(f"{Colors.FAIL}[!] Opción inválida{Colors.ENDC}")
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def codificar_base64():
	"""Codifica/Decodifica texto en Base64"""
	print(f"\n{Colors.OKCYAN}[*] Codificador/Decodificador Base64{Colors.ENDC}")
	print("=" * 50)
	
	print(f"\n{Colors.WARNING}Opciones:{Colors.ENDC}")
	print("1. Codificar (texto -> Base64)")
	print("2. Decodificar (Base64 -> texto)")
	
	opcion = input(f"\n{Colors.WARNING}Selecciona una opción (1-2): {Colors.ENDC}").strip()
	
	if opcion == "1":
		texto = input(f"{Colors.WARNING}Ingresa el texto a codificar: {Colors.ENDC}").strip()
		if texto:
			try:
				codificado = base64.b64encode(texto.encode('utf-8')).decode('utf-8')
				print(f"\n{Colors.OKGREEN}[+] Resultado:{Colors.ENDC}")
				print(f"{codificado}")
			except Exception as e:
				print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
	
	elif opcion == "2":
		base64_text = input(f"{Colors.WARNING}Ingresa el Base64 a decodificar: {Colors.ENDC}").strip()
		if base64_text:
			try:
				decodificado = base64.b64decode(base64_text).decode('utf-8')
				print(f"\n{Colors.OKGREEN}[+] Resultado:{Colors.ENDC}")
				print(f"{decodificado}")
			except Exception as e:
				print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
	
	else:
		print(f"{Colors.FAIL}[!] Opción inválida{Colors.ENDC}")
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def analizar_web():
	"""Analiza información de un sitio web"""
	print(f"\n{Colors.OKCYAN}[*] Análisis de Sitio Web{Colors.ENDC}")
	print("=" * 50)
	
	url = input(f"{Colors.WARNING}Ingresa la URL (ej: https://ejemplo.com): {Colors.ENDC}").strip()
	if not url:
		print(f"{Colors.FAIL}[!] Debes ingresar una URL válida{Colors.ENDC}")
		return
	
	if not url.startswith(('http://', 'https://')):
		url = 'https://' + url
	
	try:
		print(f"\n{Colors.OKBLUE}Analizando {url}...{Colors.ENDC}\n")
		
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		}
		response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
		
		print(f"{Colors.BOLD}Información del servidor:{Colors.ENDC}")
		print(f"  URL final: {response.url}")
		print(f"  Status Code: {response.status_code}")
		print(f"  Tamaño: {len(response.content)} bytes")
		
		if 'Server' in response.headers:
			print(f"  Server: {response.headers['Server']}")
		if 'X-Powered-By' in response.headers:
			print(f"  X-Powered-By: {response.headers['X-Powered-By']}")
		
		print(f"\n{Colors.BOLD}Headers de respuesta:{Colors.ENDC}")
		for header, valor in response.headers.items():
			print(f"  {header}: {valor}")
		
	except requests.exceptions.RequestException as e:
		print(f"{Colors.FAIL}[!] Error al conectar: {e}{Colors.ENDC}")
	except Exception as e:
		print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def generar_hash():
	"""Genera hash MD5, SHA1, SHA256 de un texto"""
	print(f"\n{Colors.OKCYAN}[*] Generador de Hash{Colors.ENDC}")
	print("=" * 50)
	
	import hashlib
	
	texto = input(f"{Colors.WARNING}Ingresa el texto a hashear: {Colors.ENDC}").strip()
	if not texto:
		print(f"{Colors.FAIL}[!] Debes ingresar un texto{Colors.ENDC}")
		return
	
	texto_bytes = texto.encode('utf-8')
	
	print(f"\n{Colors.BOLD}Hashes generados:{Colors.ENDC}")
	print(f"  MD5:    {hashlib.md5(texto_bytes).hexdigest()}")
	print(f"  SHA1:   {hashlib.sha1(texto_bytes).hexdigest()}")
	print(f"  SHA256: {hashlib.sha256(texto_bytes).hexdigest()}")
	print(f"  SHA512: {hashlib.sha512(texto_bytes).hexdigest()}")
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def mostrar_menu():
	"""Muestra el menú principal"""
	clear_screen()
	print_banner()
	
	print(f"{Colors.BOLD}Menú Principal:{Colors.ENDC}\n")
	print(f"{Colors.OKGREEN}1.{Colors.ENDC} Escanear Puertos")
	print(f"{Colors.OKGREEN}2.{Colors.ENDC} Información de IP")
	print(f"{Colors.OKGREEN}3.{Colors.ENDC} Crear Imagen Desofuscada")
	print(f"{Colors.OKGREEN}4.{Colors.ENDC} Codificar/Decodificar Base64")
	print(f"{Colors.OKGREEN}5.{Colors.ENDC} Analizar Sitio Web")
	print(f"{Colors.OKGREEN}6.{Colors.ENDC} Generar Hash (MD5, SHA1, SHA256)")
	print(f"{Colors.OKGREEN}7.{Colors.ENDC} Información del Sistema")
	print(f"{Colors.FAIL}0.{Colors.ENDC} Salir")
	print()

def info_sistema():
	"""Muestra información del sistema"""
	print(f"\n{Colors.OKCYAN}[*] Información del Sistema{Colors.ENDC}")
	print("=" * 50)
	
	print(f"\n{Colors.BOLD}Información del sistema:{Colors.ENDC}")
	print(f"  Sistema Operativo: {platform.system()}")
	print(f"  Versión: {platform.version()}")
	print(f"  Arquitectura: {platform.machine()}")
	print(f"  Procesador: {platform.processor()}")
	print(f"  Hostname: {platform.node()}")
	print(f"  Usuario: {os.getenv('USER', os.getenv('USERNAME', 'N/A'))}")
	
	# Información de red
	try:
		hostname = socket.gethostname()
		ip_local = socket.gethostbyname(hostname)
		print(f"\n{Colors.BOLD}Información de red:{Colors.ENDC}")
		print(f"  Hostname: {hostname}")
		print(f"  IP Local: {ip_local}")
	except:
		pass
	
	input(f"\n{Colors.WARNING}Presiona Enter para continuar...{Colors.ENDC}")

def main():
	"""Función principal"""
	while True:
		mostrar_menu()
		
		opcion = input(f"{Colors.WARNING}Selecciona una opción: {Colors.ENDC}").strip()
		
		if opcion == "1":
			escanear_puertos()
		elif opcion == "2":
			obtener_info_ip()
		elif opcion == "3":
			crear_imagen_desofuscada()
		elif opcion == "4":
			codificar_base64()
		elif opcion == "5":
			analizar_web()
		elif opcion == "6":
			generar_hash()
		elif opcion == "7":
			info_sistema()
		elif opcion == "0":
			print(f"\n{Colors.OKGREEN}[*] Saliendo...{Colors.ENDC}")
			sys.exit(0)
		else:
			print(f"\n{Colors.FAIL}[!] Opción inválida. Presiona Enter para continuar...{Colors.ENDC}")
			input()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n\n{Colors.WARNING}[!] Interrumpido por el usuario{Colors.ENDC}")
		sys.exit(0)
	except Exception as e:
		print(f"\n{Colors.FAIL}[!] Error crítico: {e}{Colors.ENDC}")
		sys.exit(1)

