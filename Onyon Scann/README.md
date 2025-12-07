# Deep Web Crawler - Guía de Uso

Crawler para la deep web que utiliza Tor para navegar de forma anónima y PostgreSQL para almacenar los resultados. El programa rastrea enlaces `.onion` de forma automática y organizada.

## 📋 Requisitos Previos

Antes de ejecutar el programa, necesitas tener instalado y configurado lo siguiente:

### 1. Python 3.x
- Asegúrate de tener Python 3 instalado en tu sistema.
- Puedes verificar la versión con: `python --version`

### 2. Tor Expert Bundle
- **Descarga**: [Tor Expert Bundle](https://www.torproject.org/download/tor/)
- **Instalación**: Extrae el archivo en una carpeta de tu elección.
- **Ejecución**: Debes iniciar Tor antes de ejecutar el crawler.
  - En Windows: Ejecuta `tor.exe` desde la carpeta extraída.
  - El puerto por defecto es `9050` (configurado en el script).

### 3. PostgreSQL
- **Descarga e instalación**: [PostgreSQL Download](https://www.postgresql.org/download/)
- Durante la instalación, recuerda la contraseña que configures para el usuario `postgres`.
- Asegúrate de que el servicio de PostgreSQL esté corriendo.

## 🔧 Instalación

### Paso 1: Instalar dependencias de Python

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará las siguientes librerías:
- `requests==2.31.0` - Para realizar peticiones HTTP
- `beautifulsoup4==4.12.2` - Para parsear HTML
- `psycopg2-binary==2.9.9` - Para conectar con PostgreSQL

### Paso 2: Crear la base de datos

Abre PostgreSQL (pgAdmin o línea de comandos) y crea la base de datos:

```sql
CREATE DATABASE deepweb_crawler;
```

El script creará automáticamente las tablas necesarias al ejecutarse por primera vez.

## ⚙️ Configuración

Antes de ejecutar el programa, **DEBES modificar** las siguientes variables en el archivo del script:

### 1. Configuración de PostgreSQL (Líneas 27-31)

```python
DB_HOST = "localhost"        # Cambiar si PostgreSQL está en otro servidor
DB_NAME = "deepweb_crawler"  # Nombre de la base de datos (debe existir)
DB_USER = "postgres"         # Usuario de PostgreSQL
DB_PASS = ""                 # ⚠️ OBLIGATORIO: Poner tu contraseña aquí
DB_PORT = "5432"             # Puerto de PostgreSQL (por defecto 5432)
```

**⚠️ IMPORTANTE**: Debes poner tu contraseña de PostgreSQL en `DB_PASS`.

### 2. Configuración de Rutas (Línea 34)

```python
BASE_DIR = r"C:\Users\TuUser\Desktop\Carpeta"
```

**⚠️ DEBES CAMBIAR** `TuUser` por tu nombre de usuario de Windows, o usar otra ruta válida.

Ejemplo:
```python
BASE_DIR = r"C:\Users\Juan\Desktop\DeepWebLinks"
```

### 3. Configuración de Tor (Líneas 16-21)

Por defecto está configurado para el puerto estándar de Tor:

```python
TOR_PORT = 9050  # Solo cambiar si Tor usa otro puerto
```

Si tu Tor está configurado en otro puerto, cambia este valor.

### 4. Configuración Opcional

#### URL Semilla (Línea 43)
```python
SEED_URL = "http://wkkrcvje42625v7g77maufsgvqbu7eh7tgfvwzqrarqptfktqiaa6ayd.onion/darkweb-search-engines-v3/hidden-wiki"
```
Esta es la URL inicial desde donde comenzará el crawler. Puedes cambiarla por otra URL `.onion` si lo deseas.

#### Timeout de Peticiones (Línea 46)
```python
REQUEST_TIMEOUT = 20  # Segundos de espera antes de considerar timeout
```

#### Límite de Enlaces por Dominio (Línea 47)
```python
MAX_LINKS_PER_DOMAIN = 15  # Máximo de enlaces por dominio antes de descartarlo
```

## 🚀 Ejecución

### Paso 1: Iniciar Tor

Antes de ejecutar el script, asegúrate de que Tor esté corriendo:
- Ejecuta `tor.exe` desde la carpeta de Tor Expert Bundle.
- Espera a que se conecte (verás mensajes en la consola).

### Paso 2: Verificar PostgreSQL

Asegúrate de que el servicio de PostgreSQL esté activo:
- En Windows: Verifica en "Servicios" que PostgreSQL esté corriendo.
- O intenta conectarte con pgAdmin o psql.

### Paso 3: Ejecutar el Script

```bash
python "### Para poder iniciar el programa neces.py"
```

O si renombras el archivo a algo más simple (ej: `crawler.py`):
```bash
python crawler.py
```

### Paso 4: Seleccionar Modo

Al iniciar, el programa te mostrará un menú:

```
========================================
   SELECTOR DE MODO CRAWLER (POSTGRES)
========================================
1. Modo Normal (Cola: X | Completados: Y)
2. Modo Reintentos (Cola 404: Z enlaces)
========================================
```

- **Modo Normal (1)**: Procesa URLs nuevas de la cola principal.
- **Modo Reintentos (2)**: Reintenta URLs que dieron error 404 anteriormente.

## 📊 Funcionamiento

### Inicialización
1. El script crea automáticamente las tablas en PostgreSQL si no existen:
   - `queue`: Cola principal de URLs pendientes
   - `crawled_pages`: Páginas ya visitadas con sus títulos y códigos de estado
   - `retry_queue`: URLs que dieron error 404 para reintentar
   - `domain_stats`: Estadísticas de cuántos enlaces se han encontrado por dominio

2. Si es la primera ejecución, inserta la URL semilla en la cola.

### Proceso de Crawling
1. Toma una URL de la cola (según el modo seleccionado).
2. Realiza una petición HTTP a través de Tor.
3. Si la respuesta es exitosa (200):
   - Extrae el título de la página.
   - Guarda la información en PostgreSQL.
   - Guarda una copia en el archivo TXT.
   - Busca todos los enlaces `.onion` en la página.
   - Agrega los nuevos enlaces a la cola (respetando el límite por dominio).
4. Si hay errores (404, timeout, etc.):
   - Registra el error en la base de datos.
   - En modo Normal: agrega URLs 404 a la cola de reintentos.
   - En modo Reintentos: rota la URL al final de la cola para intentar más tarde.

### Almacenamiento de Datos

#### Base de Datos PostgreSQL
- **`crawled_pages`**: Contiene todas las URLs visitadas con título y código de estado.
- **`queue`**: URLs pendientes de procesar.
- **`retry_queue`**: URLs con error 404 para reintentar.
- **`domain_stats`**: Control de límites por dominio.

#### Archivo de Texto
- Se guarda en: `{BASE_DIR}/onion_links.txt`
- Formato:
  ```
  TÍTULO: Nombre de la página
  URL: http://ejemplo.onion/ruta
  --------------------------------------------------
  ```

## 🛑 Detener el Programa

Para detener el crawler de forma segura:
- Presiona `Ctrl + C` en la terminal.
- El programa guardará el estado y cerrará las conexiones correctamente.

## ⚠️ Notas Importantes

1. **Tor debe estar corriendo**: El programa fallará si Tor no está activo en el puerto 9050.
2. **PostgreSQL debe estar activo**: Verifica que el servicio esté corriendo antes de ejecutar.
3. **Velocidad**: El script espera 2 segundos entre cada petición para no saturar.
4. **Límites**: Cada dominio solo puede tener máximo 15 enlaces en la cola para evitar saturación.
5. **Primera ejecución**: La primera vez puede tardar más mientras se conecta a través de Tor.

## 🔍 Solución de Problemas

### Error: "Error conectando a Postgres"
- Verifica que PostgreSQL esté corriendo.
- Revisa que la contraseña en `DB_PASS` sea correcta.
- Confirma que la base de datos `deepweb_crawler` existe.

### Error: "ConnectionError" o "Timeout"
- Verifica que Tor esté corriendo.
- Espera unos segundos y vuelve a intentar (Tor puede estar iniciando).
- Revisa que el puerto 9050 esté disponible.

### Error: "No se pudo crear el directorio"
- Verifica que la ruta en `BASE_DIR` sea válida.
- Asegúrate de tener permisos de escritura en esa ubicación.

### El programa no encuentra enlaces
- Algunas páginas pueden no tener enlaces `.onion`.
- La URL semilla puede no estar disponible.
- Intenta cambiar la `SEED_URL` por otra.

## 📝 Estructura de Tablas

### Tabla: `queue`
```sql
id (SERIAL PRIMARY KEY)
url (TEXT UNIQUE)
```

### Tabla: `crawled_pages`
```sql
id (SERIAL PRIMARY KEY)
url (TEXT UNIQUE)
title (TEXT)
status_code (INTEGER)
```

### Tabla: `retry_queue`
```sql
id (SERIAL PRIMARY KEY)
url (TEXT UNIQUE)
```

### Tabla: `domain_stats`
```sql
domain (TEXT PRIMARY KEY)
count (INTEGER DEFAULT 0)
```

## 📌 Resumen de Cambios Necesarios

Antes de ejecutar, **DEBES modificar**:

1. ✅ **Línea 30**: `DB_PASS = ""` → Poner tu contraseña de PostgreSQL
2. ✅ **Línea 34**: `BASE_DIR = r"C:\Users\TuUser\Desktop\Carpeta"` → Cambiar `TuUser` por tu usuario

Opcional:
- Línea 43: Cambiar `SEED_URL` si quieres empezar desde otra página
- Línea 46: Ajustar `REQUEST_TIMEOUT` si es necesario
- Línea 47: Cambiar `MAX_LINKS_PER_DOMAIN` para ajustar límites

## 📄 Licencia

Este proyecto es de uso educativo. Úsalo de forma responsable y respetando las leyes de tu país.

