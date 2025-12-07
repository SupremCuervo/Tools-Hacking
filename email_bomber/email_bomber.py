#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Bomber - Enviador masivo de emails
Envía múltiples emails (SOLO PARA FINES EDUCATIVOS)
"""

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class EmailBomber:
	def __init__(self, smtp_server, smtp_port, email, password):
		self.smtp_server = smtp_server
		self.smtp_port = smtp_port
		self.email = email
		self.password = password
		self.server = None
	
	def connect(self):
		"""Conecta al servidor SMTP"""
		try:
			self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
			self.server.starttls()
			self.server.login(self.email, self.password)
			print(f"{Colors.GREEN}[+] Conectado a {self.smtp_server}{Colors.END}")
			return True
		except Exception as e:
			print(f"{Colors.RED}[!] Error conectando: {e}{Colors.END}")
			return False
	
	def send_email(self, to_email, subject, body):
		"""Envía un email"""
		try:
			msg = MIMEMultipart()
			msg['From'] = self.email
			msg['To'] = to_email
			msg['Subject'] = subject
			msg.attach(MIMEText(body, 'plain'))
			
			text = msg.as_string()
			self.server.sendmail(self.email, to_email, text)
			return True
		except Exception as e:
			print(f"{Colors.RED}[!] Error enviando email: {e}{Colors.END}")
			return False
	
	def send_bulk(self, to_email, subject, body, count, delay=1):
		"""Envía múltiples emails"""
		print(f"{Colors.BLUE}[*] Enviando {count} emails a {to_email}{Colors.END}")
		print(f"{Colors.BLUE}[*] Delay entre emails: {delay} segundos{Colors.END}\n")
		
		sent = 0
		failed = 0
		
		for i in range(count):
			if self.send_email(to_email, subject, body):
				sent += 1
				print(f"{Colors.GREEN}[+] Email {i+1}/{count} enviado{Colors.END}")
			else:
				failed += 1
				print(f"{Colors.RED}[-] Email {i+1}/{count} falló{Colors.END}")
			
			if i < count - 1:  # No esperar después del último
				time.sleep(delay)
		
		print(f"\n{Colors.GREEN}[+] Emails enviados: {sent}{Colors.END}")
		if failed > 0:
			print(f"{Colors.RED}[-] Emails fallidos: {failed}{Colors.END}")
	
	def disconnect(self):
		"""Desconecta del servidor"""
		if self.server:
			self.server.quit()
			print(f"{Colors.GREEN}[+] Desconectado{Colors.END}")

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║      Email Bomber - Enviador Masivo     ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.RED}{Colors.BOLD}⚠️  ADVERTENCIA LEGAL ⚠️{Colors.END}")
	print(f"{Colors.RED}Este software es SOLO para fines educativos.{Colors.END}")
	print(f"{Colors.RED}El spam es ILEGAL en la mayoría de jurisdicciones.{Colors.END}\n")
	
	confirm = input(f"{Colors.YELLOW}¿Continuar? (s/n): {Colors.END}").strip().lower()
	if confirm != 's':
		print(f"{Colors.BLUE}[*] Cancelado{Colors.END}")
		return
	
	# Configuración SMTP
	print(f"\n{Colors.YELLOW}Configuración SMTP:{Colors.END}")
	smtp_server = input(f"{Colors.BLUE}Servidor SMTP (ej: smtp.gmail.com): {Colors.END}").strip()
	smtp_port = input(f"{Colors.BLUE}Puerto SMTP (default: 587): {Colors.END}").strip()
	smtp_port = int(smtp_port) if smtp_port else 587
	
	email = input(f"{Colors.BLUE}Tu email: {Colors.END}").strip()
	password = input(f"{Colors.BLUE}Contraseña (o App Password): {Colors.END}").strip()
	
	# Configuración del email
	print(f"\n{Colors.YELLOW}Configuración del email:{Colors.END}")
	to_email = input(f"{Colors.BLUE}Email destino: {Colors.END}").strip()
	subject = input(f"{Colors.BLUE}Asunto: {Colors.END}").strip()
	body = input(f"{Colors.BLUE}Mensaje: {Colors.END}").strip()
	
	count = input(f"{Colors.BLUE}Cantidad de emails a enviar: {Colors.END}").strip()
	try:
		count = int(count)
	except:
		print(f"{Colors.RED}[!] Cantidad inválida{Colors.END}")
		return
	
	delay = input(f"{Colors.BLUE}Delay entre emails (segundos, default: 1): {Colors.END}").strip()
	try:
		delay = float(delay) if delay else 1.0
	except:
		delay = 1.0
	
	# Enviar
	bomber = EmailBomber(smtp_server, smtp_port, email, password)
	
	if bomber.connect():
		bomber.send_bulk(to_email, subject, body, count, delay)
		bomber.disconnect()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.YELLOW}[!] Interrumpido por el usuario{Colors.END}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		sys.exit(1)

