#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper - Extractor de datos web
Extrae información de sitios web de forma automatizada
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import sys
from urllib.parse import urljoin, urlparse
import time
import os

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class WebScraper:
	def __init__(self, base_url, delay=1):
		self.base_url = base_url
		self.delay = delay
		self.session = requests.Session()
		self.session.headers.update({
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		})
		self.visited_urls = set()
		self.data = []
	
	def fetch_page(self, url):
		"""Obtiene el contenido de una página"""
		if url in self.visited_urls:
			return None
		
		try:
			time.sleep(self.delay)
			response = self.session.get(url, timeout=10)
			response.raise_for_status()
			self.visited_urls.add(url)
			return response
		except Exception as e:
			print(f"{Colors.RED}[!] Error obteniendo {url}: {e}{Colors.END}")
			return None
	
	def extract_links(self, soup, base_url):
		"""Extrae todos los enlaces de una página"""
		links = []
		for link in soup.find_all('a', href=True):
			full_url = urljoin(base_url, link['href'])
			if urlparse(full_url).netloc == urlparse(base_url).netloc:
				links.append(full_url)
		return links
	
	def scrape_text(self, url):
		"""Extrae todo el texto de una página"""
		response = self.fetch_page(url)
		if not response:
			return None
		
		soup = BeautifulSoup(response.content, 'html.parser')
		
		# Remover scripts y estilos
		for script in soup(["script", "style"]):
			script.decompose()
		
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = ' '.join(chunk for chunk in chunks if chunk)
		
		return {
			'url': url,
			'title': soup.title.string if soup.title else 'Sin título',
			'text': text
		}
	
	def scrape_images(self, url):
		"""Extrae todas las imágenes de una página"""
		response = self.fetch_page(url)
		if not response:
			return []
		
		soup = BeautifulSoup(response.content, 'html.parser')
		images = []
		
		for img in soup.find_all('img'):
			img_url = urljoin(url, img.get('src', ''))
			alt = img.get('alt', 'Sin descripción')
			images.append({
				'url': img_url,
				'alt': alt
			})
		
		return images
	
	def scrape_forms(self, url):
		"""Extrae formularios de una página"""
		response = self.fetch_page(url)
		if not response:
			return []
		
		soup = BeautifulSoup(response.content, 'html.parser')
		forms = []
		
		for form in soup.find_all('form'):
			form_data = {
				'action': form.get('action', ''),
				'method': form.get('method', 'GET'),
				'inputs': []
			}
			
			for input_tag in form.find_all(['input', 'textarea', 'select']):
				form_data['inputs'].append({
					'type': input_tag.get('type', input_tag.name),
					'name': input_tag.get('name', ''),
					'id': input_tag.get('id', '')
				})
			
			forms.append(form_data)
		
		return forms
	
	def crawl(self, max_pages=10):
		"""Crawlea múltiples páginas"""
		to_visit = [self.base_url]
		visited = set()
		results = []
		
		while to_visit and len(visited) < max_pages:
			url = to_visit.pop(0)
			if url in visited:
				continue
			
			print(f"{Colors.BLUE}[*] Visitando: {url}{Colors.END}")
			response = self.fetch_page(url)
			
			if not response:
				continue
			
			visited.add(url)
			soup = BeautifulSoup(response.content, 'html.parser')
			
			# Extraer datos
			title = soup.title.string if soup.title else 'Sin título'
			results.append({
				'url': url,
				'title': title
			})
			
			# Encontrar más enlaces
			links = self.extract_links(soup, url)
			for link in links:
				if link not in visited and link not in to_visit:
					to_visit.append(link)
		
		return results
	
	def save_csv(self, data, filename):
		"""Guarda datos en CSV"""
		if not data:
			return
		
		keys = data[0].keys()
		with open(filename, 'w', newline='', encoding='utf-8') as f:
			writer = csv.DictWriter(f, fieldnames=keys)
			writer.writeheader()
			writer.writerows(data)
		
		print(f"{Colors.GREEN}[+] Datos guardados en: {filename}{Colors.END}")
	
	def save_json(self, data, filename):
		"""Guarda datos en JSON"""
		with open(filename, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2, ensure_ascii=False)
		
		print(f"{Colors.GREEN}[+] Datos guardados en: {filename}{Colors.END}")

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║        Web Scraper - Extractor         ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	url = input(f"{Colors.BLUE}Ingresa la URL a scrapear: {Colors.END}").strip()
	if not url:
		print(f"{Colors.RED}[!] Debes ingresar una URL{Colors.END}")
		return
	
	if not url.startswith(('http://', 'https://')):
		url = 'https://' + url
	
	print(f"\n{Colors.YELLOW}Opciones:{Colors.END}")
	print("1. Extraer texto")
	print("2. Extraer imágenes")
	print("3. Extraer formularios")
	print("4. Crawlear sitio (múltiples páginas)")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-4): {Colors.END}").strip()
	
	scraper = WebScraper(url, delay=1)
	
	if opcion == '1':
		print(f"\n{Colors.BLUE}[*] Extrayendo texto...{Colors.END}")
		data = scraper.scrape_text(url)
		if data:
			print(f"\n{Colors.GREEN}[+] Título: {data['title']}{Colors.END}")
			print(f"{Colors.GREEN}[+] Texto extraído: {len(data['text'])} caracteres{Colors.END}")
			
			# Guardar
			save = input(f"\n{Colors.BLUE}¿Guardar en archivo? (s/n): {Colors.END}").strip().lower()
			if save == 's':
				format_op = input(f"{Colors.BLUE}Formato (1=JSON, 2=TXT): {Colors.END}").strip()
				if format_op == '1':
					scraper.save_json([data], 'scraped_text.json')
				else:
					with open('scraped_text.txt', 'w', encoding='utf-8') as f:
						f.write(f"URL: {data['url']}\n")
						f.write(f"Título: {data['title']}\n\n")
						f.write(data['text'])
					print(f"{Colors.GREEN}[+] Guardado en scraped_text.txt{Colors.END}")
	
	elif opcion == '2':
		print(f"\n{Colors.BLUE}[*] Extrayendo imágenes...{Colors.END}")
		images = scraper.scrape_images(url)
		print(f"{Colors.GREEN}[+] Imágenes encontradas: {len(images)}{Colors.END}")
		
		for img in images[:10]:  # Mostrar primeras 10
			print(f"  - {img['url']} ({img['alt']})")
		
		if len(images) > 10:
			print(f"  ... y {len(images) - 10} más")
		
		save = input(f"\n{Colors.BLUE}¿Guardar en CSV? (s/n): {Colors.END}").strip().lower()
		if save == 's':
			scraper.save_csv(images, 'scraped_images.csv')
	
	elif opcion == '3':
		print(f"\n{Colors.BLUE}[*] Extrayendo formularios...{Colors.END}")
		forms = scraper.scrape_forms(url)
		print(f"{Colors.GREEN}[+] Formularios encontrados: {len(forms)}{Colors.END}")
		
		for i, form in enumerate(forms, 1):
			print(f"\n  Formulario {i}:")
			print(f"    Action: {form['action']}")
			print(f"    Method: {form['method']}")
			print(f"    Inputs: {len(form['inputs'])}")
		
		save = input(f"\n{Colors.BLUE}¿Guardar en JSON? (s/n): {Colors.END}").strip().lower()
		if save == 's':
			scraper.save_json(forms, 'scraped_forms.json')
	
	elif opcion == '4':
		max_pages = input(f"{Colors.BLUE}Máximo de páginas a crawlear (default: 10): {Colors.END}").strip()
		try:
			max_pages = int(max_pages) if max_pages else 10
		except:
			max_pages = 10
		
		print(f"\n{Colors.BLUE}[*] Crawleando sitio...{Colors.END}")
		results = scraper.crawl(max_pages=max_pages)
		
		print(f"\n{Colors.GREEN}[+] Páginas visitadas: {len(results)}{Colors.END}")
		scraper.save_csv(results, 'crawled_pages.csv')
	
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

