#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Analyzer - Analizador de texto
Analiza texto y extrae estadísticas, palabras clave y más
"""

import re
import sys
from collections import Counter
import string

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

class TextAnalyzer:
	def __init__(self, text):
		self.text = text
		self.words = self._extract_words()
	
	def _extract_words(self):
		"""Extrae palabras del texto"""
		text_clean = re.sub(r'[^\w\s]', '', self.text.lower())
		words = text_clean.split()
		return words
	
	def word_count(self):
		"""Cuenta palabras totales"""
		return len(self.words)
	
	def character_count(self, include_spaces=True):
		"""Cuenta caracteres"""
		if include_spaces:
			return len(self.text)
		return len(self.text.replace(' ', ''))
	
	def sentence_count(self):
		"""Cuenta oraciones"""
		sentences = re.split(r'[.!?]+', self.text)
		return len([s for s in sentences if s.strip()])
	
	def paragraph_count(self):
		"""Cuenta párrafos"""
		paragraphs = [p for p in self.text.split('\n\n') if p.strip()]
		return len(paragraphs)
	
	def most_common_words(self, n=10):
		"""Palabras más comunes"""
		word_freq = Counter(self.words)
		return word_freq.most_common(n)
	
	def average_word_length(self):
		"""Longitud promedio de palabras"""
		if not self.words:
			return 0
		total_length = sum(len(word) for word in self.words)
		return total_length / len(self.words)
	
	def average_sentence_length(self):
		"""Longitud promedio de oraciones (en palabras)"""
		sentences = re.split(r'[.!?]+', self.text)
		sentences = [s.strip() for s in sentences if s.strip()]
		if not sentences:
			return 0
		sentence_lengths = [len(re.findall(r'\w+', s)) for s in sentences]
		return sum(sentence_lengths) / len(sentence_lengths)
	
	def find_keywords(self, min_length=4, top_n=20):
		"""Encuentra palabras clave (palabras significativas)"""
		# Filtrar palabras comunes
		stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
		              'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'todo', 'pero',
		              'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese', 'la',
		              'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
		              'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
		              'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
		              'desde', 'grande', 'eso', 'ni', 'nos', 'venir', 'golpe', 'aunque', 'menos',
		              'recibir', 'mejor', 'cual', 'mientras', 'sí', 'tres', 'día', 'luego', 'pasar',
		              'tiempo', 'solo', 'después', 'mismo', 'casa', 'mundo', 'hombre', 'mujer',
		              'trabajo', 'vida', 'persona', 'país', 'ciudad', 'gente', 'parte', 'mano',
		              'ojo', 'cara', 'lugar', 'momento', 'forma', 'caso', 'día', 'noche', 'año',
		              'mes', 'semana', 'hora', 'minuto', 'segundo', 'vez', 'tiempo', 'momento'}
		
		# Filtrar palabras
		keywords = [w for w in self.words if len(w) >= min_length and w not in stop_words]
		keyword_freq = Counter(keywords)
		return keyword_freq.most_common(top_n)
	
	def reading_time(self, words_per_minute=200):
		"""Tiempo estimado de lectura (en minutos)"""
		word_count = self.word_count()
		return word_count / words_per_minute
	
	def analyze_sentiment_simple(self):
		"""Análisis de sentimiento simple (básico)"""
		positive_words = ['bueno', 'excelente', 'genial', 'maravilloso', 'fantástico', 'perfecto',
		                  'feliz', 'alegre', 'contento', 'satisfecho', 'agradable', 'positivo']
		negative_words = ['malo', 'terrible', 'horrible', 'triste', 'deprimido', 'enojado',
		                 'negativo', 'problema', 'error', 'fallo', 'mal', 'difícil']
		
		text_lower = self.text.lower()
		positive_count = sum(1 for word in positive_words if word in text_lower)
		negative_count = sum(1 for word in negative_words if word in text_lower)
		
		if positive_count > negative_count:
			return "Positivo", positive_count, negative_count
		elif negative_count > positive_count:
			return "Negativo", positive_count, negative_count
		else:
			return "Neutral", positive_count, negative_count
	
	def extract_emails(self):
		"""Extrae emails del texto"""
		email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		emails = re.findall(email_pattern, self.text)
		return list(set(emails))  # Remover duplicados
	
	def extract_urls(self):
		"""Extrae URLs del texto"""
		url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
		urls = re.findall(url_pattern, self.text)
		return list(set(urls))
	
	def extract_phone_numbers(self):
		"""Extrae números de teléfono"""
		phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
		phones = re.findall(phone_pattern, self.text)
		return [''.join(p) for p in phones if any(c.isdigit() for c in ''.join(p))]

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}")
	print("╔════════════════════════════════════════╗")
	print("║      Text Analyzer - Analizador        ║")
	print("╚════════════════════════════════════════╝")
	print(f"{Colors.END}\n")
	
	print(f"{Colors.YELLOW}Opciones:{Colors.END}")
	print("1. Analizar texto desde entrada")
	print("2. Analizar texto desde archivo")
	
	opcion = input(f"\n{Colors.BLUE}Selecciona opción (1-2): {Colors.END}").strip()
	
	text = ""
	
	if opcion == '1':
		print(f"\n{Colors.BLUE}Ingresa el texto (Ctrl+D o Ctrl+Z para terminar):{Colors.END}")
		try:
			lines = []
			while True:
				line = input()
				lines.append(line)
		except EOFError:
			text = '\n'.join(lines)
	
	elif opcion == '2':
		file_path = input(f"{Colors.BLUE}Ruta del archivo: {Colors.END}").strip()
		try:
			with open(file_path, 'r', encoding='utf-8') as f:
				text = f.read()
		except Exception as e:
			print(f"{Colors.RED}[!] Error leyendo archivo: {e}{Colors.END}")
			return
	else:
		print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
		return
	
	if not text.strip():
		print(f"{Colors.RED}[!] No se ingresó texto{Colors.END}")
		return
	
	analyzer = TextAnalyzer(text)
	
	print(f"\n{Colors.BOLD}{Colors.GREEN}=== ESTADÍSTICAS BÁSICAS ==={Colors.END}\n")
	print(f"Caracteres (con espacios): {analyzer.character_count(True):,}")
	print(f"Caracteres (sin espacios): {analyzer.character_count(False):,}")
	print(f"Palabras: {analyzer.word_count():,}")
	print(f"Oraciones: {analyzer.sentence_count()}")
	print(f"Párrafos: {analyzer.paragraph_count()}")
	print(f"Longitud promedio de palabra: {analyzer.average_word_length():.2f} caracteres")
	print(f"Longitud promedio de oración: {analyzer.average_sentence_length():.1f} palabras")
	print(f"Tiempo de lectura estimado: {analyzer.reading_time():.1f} minutos")
	
	print(f"\n{Colors.BOLD}{Colors.GREEN}=== PALABRAS MÁS COMUNES ==={Colors.END}\n")
	common_words = analyzer.most_common_words(10)
	for word, count in common_words:
		print(f"  {word}: {count} veces")
	
	print(f"\n{Colors.BOLD}{Colors.GREEN}=== PALABRAS CLAVE ==={Colors.END}\n")
	keywords = analyzer.find_keywords()
	for word, count in keywords[:10]:
		print(f"  {word}: {count} veces")
	
	print(f"\n{Colors.BOLD}{Colors.GREEN}=== ANÁLISIS DE SENTIMIENTO ==={Colors.END}\n")
	sentiment, pos, neg = analyzer.analyze_sentiment_simple()
	print(f"  Sentimiento: {sentiment}")
	print(f"  Palabras positivas: {pos}")
	print(f"  Palabras negativas: {neg}")
	
	emails = analyzer.extract_emails()
	if emails:
		print(f"\n{Colors.BOLD}{Colors.GREEN}=== EMAILS ENCONTRADOS ==={Colors.END}\n")
		for email in emails:
			print(f"  {email}")
	
	urls = analyzer.extract_urls()
	if urls:
		print(f"\n{Colors.BOLD}{Colors.GREEN}=== URLs ENCONTRADAS ==={Colors.END}\n")
		for url in urls:
			print(f"  {url}")
	
	phones = analyzer.extract_phone_numbers()
	if phones:
		print(f"\n{Colors.BOLD}{Colors.GREEN}=== TELÉFONOS ENCONTRADOS ==={Colors.END}\n")
		for phone in phones[:5]:  # Mostrar primeros 5
			print(f"  {phone}")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.YELLOW}[!] Interrumpido por el usuario{Colors.END}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		sys.exit(1)

