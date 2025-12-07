# Farcry - Herramientas de Seguridad y Hacking

Script interactivo de terminal con menú para diversas utilidades de seguridad, análisis de red, codificación y herramientas de hacking.

## 📋 Descripción

Farcry es una herramienta de línea de comandos que proporciona un conjunto de utilidades de seguridad en un menú interactivo fácil de usar. Incluye funciones para escaneo de puertos, análisis de IP, desofuscación de imágenes, codificación Base64, análisis web, generación de hashes y más.

## ✨ Características

- 🎨 **Interfaz con colores**: Interfaz visual atractiva con colores ANSI
- 🔍 **Escaneo de puertos**: Escanea puertos comunes en hosts remotos
- 🌐 **Análisis de IP**: Obtiene información geográfica y de red de direcciones IP
- 🖼️ **Desofuscación de imágenes**: Convierte datos Base64 o binarios a imágenes
- 🔐 **Codificación Base64**: Codifica y decodifica texto en Base64
- 🌍 **Análisis web**: Analiza headers y metadatos de sitios web
- 🔑 **Generación de hashes**: Genera MD5, SHA1, SHA256 y SHA512
- 💻 **Información del sistema**: Muestra datos del sistema y red local

## 📦 Requisitos

### Sistema Operativo
- Windows 10/11
- Linux (cualquier distribución)
- macOS

### Python
- Python 3.6 o superior

### Dependencias
- `requests` - Para peticiones HTTP

## 🚀 Instalación

### Paso 1: Verificar Python

Verifica que tienes Python instalado:

```bash
python --version
```

O en algunos sistemas:

```bash
python3 --version
```

### Paso 2: Instalar dependencias

Las dependencias ya están en `requirements.txt`. Instálalas con:

```bash
pip install -r requirements.txt
```

O instala solo requests:

```bash
pip install requests==2.31.0
```

### Paso 3: Ejecutar el script

```bash
python Farcry.py
```

O en sistemas Linux/macOS:

```bash
python3 Farcry.py
```

## 📖 Uso

### Menú Principal

Al ejecutar el script, verás un menú con las siguientes opciones:

```
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

Menú Principal:

1. Escanear Puertos
2. Información de IP
3. Crear Imagen Desofuscada
4. Codificar/Decodificar Base64
5. Analizar Sitio Web
6. Generar Hash (MD5, SHA1, SHA256)
7. Información del Sistema
0. Salir
```

### Opción 1: Escanear Puertos

Escanea puertos comunes (21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, etc.) en un host específico.

**Uso:**
1. Selecciona la opción `1`
2. Ingresa la IP o dominio a escanear
3. El script mostrará los puertos abiertos encontrados

**Ejemplo:**
```
Ingresa la IP o dominio a escanear: 192.168.1.1
Escaneando puertos comunes en 192.168.1.1...

[+] Puerto 22 ABIERTO
[+] Puerto 80 ABIERTO
[+] Puerto 443 ABIERTO

[*] Total de puertos abiertos: 3
```

### Opción 2: Información de IP

Obtiene información detallada sobre una dirección IP, incluyendo:
- Hostname
- País y región
- Ciudad
- ISP
- Coordenadas geográficas

**Uso:**
1. Selecciona la opción `2`
2. Ingresa la IP a consultar
3. El script mostrará toda la información disponible

**Ejemplo:**
```
Ingresa la IP a consultar: 8.8.8.8

Información básica:
  IP: 8.8.8.8
  Hostname: dns.google

Información geográfica:
  País: United States
  Región: California
  Ciudad: Mountain View
  ISP: Google LLC
```

### Opción 3: Crear Imagen Desofuscada

Convierte datos codificados (Base64 o binarios) en archivos de imagen.

**Opciones:**
- **Desde Base64**: Decodifica un string Base64 y lo guarda como imagen
- **Desde archivo binario**: Convierte un archivo binario a imagen (detecta automáticamente PNG, JPG, GIF, BMP)

**Uso:**
1. Selecciona la opción `3`
2. Elige entre Base64 (1) o archivo binario (2)
3. Proporciona los datos o ruta del archivo
4. La imagen se guardará con un nombre único

**Ejemplo:**
```
Opciones:
1. Desde Base64
2. Desde archivo binario

Selecciona una opción (1-2): 1
Ingresa el string Base64: iVBORw0KGgoAAAANS...
[+] Imagen guardada como: imagen_desofuscada_20241201_143022.png
```

### Opción 4: Codificar/Decodificar Base64

Codifica texto a Base64 o decodifica Base64 a texto.

**Uso:**
1. Selecciona la opción `4`
2. Elige codificar (1) o decodificar (2)
3. Ingresa el texto o Base64
4. El resultado se mostrará en pantalla

**Ejemplo:**
```
Opciones:
1. Codificar (texto -> Base64)
2. Decodificar (Base64 -> texto)

Selecciona una opción (1-2): 1
Ingresa el texto a codificar: Hola Mundo
[+] Resultado:
SG9sYSBNdW5kbw==
```

### Opción 5: Analizar Sitio Web

Analiza un sitio web y muestra información sobre:
- URL final (después de redirecciones)
- Código de estado HTTP
- Headers de respuesta
- Información del servidor
- Tamaño de la respuesta

**Uso:**
1. Selecciona la opción `5`
2. Ingresa la URL (con o sin http/https)
3. El script mostrará toda la información disponible

**Ejemplo:**
```
Ingresa la URL (ej: https://ejemplo.com): google.com

Información del servidor:
  URL final: https://www.google.com/
  Status Code: 200
  Tamaño: 12345 bytes
  Server: gws

Headers de respuesta:
  Content-Type: text/html; charset=ISO-8859-1
  ...
```

### Opción 6: Generar Hash

Genera múltiples tipos de hash (MD5, SHA1, SHA256, SHA512) de un texto.

**Uso:**
1. Selecciona la opción `6`
2. Ingresa el texto a hashear
3. El script mostrará todos los hashes generados

**Ejemplo:**
```
Ingresa el texto a hashear: password123

Hashes generados:
  MD5:    482c811da5d5b4bc6d497ffa98491e38
  SHA1:   7c6a180b36896a0a8c02787eeafb0e4c
  SHA256: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  SHA512: ...
```

### Opción 7: Información del Sistema

Muestra información detallada sobre el sistema local:
- Sistema operativo y versión
- Arquitectura del procesador
- Hostname
- IP local
- Usuario actual

**Uso:**
1. Selecciona la opción `7`
2. La información se mostrará automáticamente

**Ejemplo:**
```
Información del sistema:
  Sistema Operativo: Windows
  Versión: 10.0.26100
  Arquitectura: AMD64
  Procesador: Intel64 Family 6 Model ...
  Hostname: DESKTOP-ABC123
  Usuario: User

Información de red:
  Hostname: DESKTOP-ABC123
  IP Local: 192.168.1.100
```

## 🛠️ Funcionalidades Técnicas

### Escaneo de Puertos
- Escanea 20 puertos comunes
- Timeout configurable (0.5 segundos por puerto)
- Muestra resultados en tiempo real

### Análisis de IP
- Resolución DNS inversa
- Consulta a API externa (ip-api.com)
- Información geográfica completa

### Desofuscación de Imágenes
- Detección automática de formato (PNG, JPG, GIF, BMP)
- Soporte para Base64 y archivos binarios
- Nombres de archivo únicos con timestamp

### Análisis Web
- Seguimiento de redirecciones
- Análisis completo de headers
- Información del servidor

## ⚠️ Notas Importantes

1. **Uso Ético**: Este script está diseñado para propósitos educativos y pruebas de seguridad autorizadas. Úsalo solo en sistemas que poseas o tengas permiso explícito para probar.

2. **Escaneo de Puertos**: El escaneo de puertos puede ser detectado por sistemas de seguridad. Úsalo responsablemente.

3. **Análisis Web**: Algunos sitios pueden bloquear peticiones automatizadas. Respeta los términos de servicio.

4. **Información de IP**: La información geográfica proviene de servicios externos y puede no ser 100% precisa.

5. **Imágenes Desofuscadas**: Asegúrate de tener permisos para desofuscar y analizar las imágenes.

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'requests'"
**Solución**: Instala requests con `pip install requests`

### Error: "Connection timeout" al escanear puertos
**Solución**: El host puede estar bloqueando conexiones o no estar disponible. Verifica la conectividad.

### Error: "No se pudo obtener información geográfica"
**Solución**: Verifica tu conexión a internet. El servicio externo puede estar temporalmente no disponible.

### Los colores no se muestran en Windows
**Solución**: Asegúrate de usar una terminal moderna (PowerShell, Windows Terminal, o CMD con soporte ANSI).

## 📝 Estructura del Código

```
Farcry.py
├── Clase Colors (colores ANSI)
├── clear_screen() - Limpia la pantalla
├── print_banner() - Muestra el banner
├── escanear_puertos() - Escaneo de puertos
├── obtener_info_ip() - Información de IP
├── crear_imagen_desofuscada() - Desofuscación
├── codificar_base64() - Codificación Base64
├── analizar_web() - Análisis web
├── generar_hash() - Generación de hashes
├── info_sistema() - Info del sistema
├── mostrar_menu() - Menú principal
└── main() - Función principal
```

## 🚫 Limitaciones

- El escaneo de puertos solo verifica puertos comunes (no es un escáner completo)
- La información de IP depende de servicios externos
- El análisis web no incluye análisis de vulnerabilidades profundas
- La desofuscación de imágenes requiere que los datos estén en formato válido

## 📄 Licencia

Este proyecto es de uso educativo. Úsalo de forma responsable y respetando las leyes de tu país.

## 🤝 Contribuciones

Las mejoras y sugerencias son bienvenidas. Recuerda mantener el código limpio y bien documentado.

## 📧 Soporte

Si encuentras problemas o tienes preguntas, revisa la sección de solución de problemas o consulta la documentación del código.

---

**⚠️ ADVERTENCIA LEGAL**: Este software es solo para fines educativos y pruebas de seguridad autorizadas. El uso no autorizado de estas herramientas puede ser ilegal. El autor no se hace responsable del mal uso de este software.

