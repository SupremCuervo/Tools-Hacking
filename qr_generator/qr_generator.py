#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Generator - Generador de códigos QR
Crea códigos QR para texto, URLs, WiFi y más
"""

import qrcode
from qrcode.image.styledmod import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import sys
from PIL import Image

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

def create_qr_text(text, filename="qr_code.png", size=10, border=4):
	"""Crea un código QR para texto"""
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=size,
		border=border,
	)
	qr.add_data(text)
	qr.make(fit=True)
	
	img = qr.make_image(fill_color="black", back_color="white")
	img.save(filename)
	return filename

def create_qr_url(url, filename="qr_url.png", size=10):
	"""Crea un código QR para URL"""
	return create_qr_text(url, filename, size)

def create_qr_wifi(ssid, password, security="WPA", filename="qr_wifi.png"):
	"""Crea un código QR para WiFi"""
	wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"
	return create_qr_text(wifi_string, filename)

def create_qr_email(email, subject="", body="", filename="qr_email.png"):
	"""Crea un código QR para email"""
	email_string = f"mailto:{email}"
	if subject:
		email_string += f"?subject={subject}"
	if body:
		email_string += f"&body={body}"
	return create_qr_text(email_string, filename)

def create_qr_phone(phone, filename="qr_phone.png"):
	"""Crea un código QR para teléfono"""
	phone_string = f"tel:{phone}"
	return create_qr_text(phone_string, filename)

def create_styled_qr(text, filename="qr_styled.png", size=10):
	"""Crea un código QR con estilo redondeado"""
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=size,
		border=4,
	)
	qr.add_data(text)
	qr.make(fit=True)
	
	img = qr.make_image(
		image_factory=StyledPilImage,
		module_drawer=RoundedModuleDrawer()
	)
	img.save(filename)
	return filename

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║      QR Generator - Generador QR       ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.YELLOW}Tipos de QR disponibles:{Colors.END}")
	print("1. Texto simple")
	print("2. URL")
	print("3. WiFi")
	print("4. Email")
	print("5. Teléfono")
	print("6. QR con estilo (redondeado)")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-6): {Colors.END}").strip()
	
	filename = input(f"{Colors.BLUE}Nombre del archivo (default: qr_code.png): {Colors.END}").strip()
	if not filename:
		filename = "qr_code.png"
	
	if opcion == '1':
		text = input(f"{Colors.BLUE}Ingresa el texto: {Colors.END}").strip()
		if text:
			create_qr_text(text, filename)
			print(f"{Colors.GREEN}[+] QR creado: {filename}{Colors.END}")
	
	elif opcion == '2':
		url = input(f"{Colors.BLUE}Ingresa la URL: {Colors.END}").strip()
		if url:
			if not url.startswith(('http://', 'https://')):
				url = 'https://' + url
			create_qr_url(url, filename)
			print(f"{Colors.GREEN}[+] QR creado: {filename}{Colors.END}")
	
	elif opcion == '3':
		ssid = input(f"{Colors.BLUE}Nombre de la red (SSID): {Colors.END}").strip()
		password = input(f"{Colors.BLUE}Contraseña: {Colors.END}").strip()
		security = input(f"{Colors.BLUE}Tipo de seguridad (WPA/WEP/nopass, default: WPA): {Colors.END}").strip()
		if not security:
			security = "WPA"
		
		if ssid and password:
			create_qr_wifi(ssid, password, security, filename)
			print(f"{Colors.GREEN}[+] QR WiFi creado: {filename}{Colors.END}")
	
	elif opcion == '4':
		email = input(f"{Colors.BLUE}Email: {Colors.END}").strip()
		subject = input(f"{Colors.BLUE}Asunto (opcional): {Colors.END}").strip()
		body = input(f"{Colors.BLUE}Mensaje (opcional): {Colors.END}").strip()
		
		if email:
			create_qr_email(email, subject, body, filename)
			print(f"{Colors.GREEN}[+] QR Email creado: {filename}{Colors.END}")
	
	elif opcion == '5':
		phone = input(f"{Colors.BLUE}Número de teléfono: {Colors.END}").strip()
		if phone:
			create_qr_phone(phone, filename)
			print(f"{Colors.GREEN}[+] QR Teléfono creado: {filename}{Colors.END}")
	
	elif opcion == '6':
		text = input(f"{Colors.BLUE}Ingresa el texto: {Colors.END}").strip()
		if text:
			create_styled_qr(text, filename)
			print(f"{Colors.GREEN}[+] QR con estilo creado: {filename}{Colors.END}")
	
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
		print(f"{Colors.RED}[!] Asegúrate de tener instalado: pip install qrcode[pil]{Colors.END}")
		sys.exit(1)

