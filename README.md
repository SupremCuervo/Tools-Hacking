# Linux - Herramientas de Seguridad para Kali Linux / Predator OS

Colección de scripts de seguridad diseñados para Kali Linux y Predator OS, cada uno con su propio banner ASCII de anime único.

## 📋 Descripción

Esta carpeta contiene 15 herramientas de seguridad especializadas para pruebas de penetración y análisis de seguridad en entornos Linux. Cada herramienta está diseñada para facilitar el uso de herramientas comunes de Kali Linux.

## 🛠️ Herramientas Incluidas

### Escaneo y Reconocimiento
1. **nmap_scanner** - Generador de comandos Nmap para escaneo de puertos y servicios
2. **nikto_scanner** - Asistente para escaneo de vulnerabilidades web con Nikto
3. **dirb_scanner** - Generador de comandos DirB para descubrimiento de directorios

### Explotación y Pruebas
4. **metasploit_helper** - Generador de payloads y comandos de Metasploit Framework
5. **sql_injection_tester** - Probador automático de vulnerabilidades SQL injection
6. **sqlmap_helper** - Asistente para automatización de SQLMap

### Fuerza Bruta y Cracking
7. **hydra_bruteforce** - Generador de comandos Hydra para fuerza bruta
8. **john_cracker** - Asistente para John the Ripper password cracker

### Análisis de Red
9. **wireshark_capture** - Asistente para captura de paquetes con tcpdump/Wireshark
10. **aircrack_helper** - Herramienta para auditoría WiFi con Aircrack-ng

### Utilidades
11. **burp_helper** - Tips y configuraciones para Burp Suite
12. **linux_exploit_suggester** - Sugeridor de exploits basado en versión de kernel
13. **wordlist_generator** - Generador de wordlists personalizadas
14. **hash_identifier** - Identificador de tipos de hash
15. **enum4linux_helper** - Enumeración SMB/Samba con Enum4linux

## 🚀 Instalación

### Requisitos del Sistema

- Kali Linux o Predator OS (recomendado)
- Python 3.6 o superior
- Herramientas de Kali Linux instaladas (nmap, metasploit, etc.)

### Instalación de Dependencias

```bash
# Instalar herramientas de Kali
sudo apt update
sudo apt install nmap metasploit-framework sqlmap hydra john aircrack-ng nikto dirb enum4linux

# Instalar dependencias Python
pip install requests
```

## 📖 Uso

Cada herramienta tiene su propio README con instrucciones detalladas. Ejemplo:

```bash
cd Linux/nmap_scanner
python nmap_scanner.py
```

## ⚠️ Uso Ético

**IMPORTANTE**: Todas estas herramientas están diseñadas para:
- ✅ Pruebas de penetración autorizadas
- ✅ Auditorías de seguridad en sistemas propios
- ✅ Aprendizaje y educación
- ✅ Investigación con consentimiento

**NO uses estas herramientas para:**
- ❌ Acceso no autorizado a sistemas
- ❌ Actividades ilegales
- ❌ Violación de privacidad
- ❌ Cualquier actividad sin permiso explícito

## 📁 Estructura

```
Linux/
├── README.md (este archivo)
├── nmap_scanner/
│   ├── nmap_scanner.py
│   └── README.md
├── metasploit_helper/
│   ├── metasploit_helper.py
│   └── README.md
├── sql_injection_tester/
│   ├── sql_injection_tester.py
│   └── README.md
... (y así para cada herramienta)
```

## 🎨 Características

- **Banners ASCII únicos**: Cada script tiene su propio banner de anime
- **Interfaz colorida**: Salida con colores para mejor legibilidad
- **Generación de comandos**: Facilita el uso de herramientas complejas
- **Documentación completa**: Cada herramienta incluye su README

## 📝 Notas

- Algunas herramientas requieren permisos de root
- Asegúrate de tener las herramientas base instaladas antes de usar los scripts
- Los scripts generan comandos que puedes ejecutar manualmente o automáticamente

## ⚠️ ADVERTENCIA LEGAL

El uso no autorizado de estas herramientas es ilegal. Solo úsalas en sistemas que poseas o tengas permiso explícito para probar. Los autores no se hacen responsables del mal uso de este software.

