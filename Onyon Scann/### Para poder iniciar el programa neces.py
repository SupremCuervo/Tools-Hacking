### Para poder iniciar el programa necesitas correr Tor Expert Bundle y tener activa una DB PostgreSQL
 
 
 
 
import requests
from bs4 import BeautifulSoup
import sys
import time
import os
import psycopg2 
from psycopg2 import sql
from urllib.parse import urljoin, urlparse
 
# --- CONFIGURACIÓN DE TOR ---
TOR_PORT = 9050 
TOR_PROXY = f"socks5h://127.0.0.1:{TOR_PORT}"
PROXIES = {
    'http': TOR_PROXY,
    'https': TOR_PROXY
}
 
 
 
# --- CONFIGURACIÓN POSTGRESQL ---
# Cambia estos valores por los de tu servidor local/remoto
DB_HOST = "localhost"
DB_NAME = "deepweb_crawler"
DB_USER = "postgres"
DB_PASS = "" # Pone tu contraseña aca
DB_PORT = "5432"
 
# --- CONFIGURACIÓN DE RUTAS Y LÍMITES ---
BASE_DIR = r"C:\Users\TuUser\Desktop\Carpeta"
 
if not os.path.exists(BASE_DIR):
    try:
        os.makedirs(BASE_DIR)
        print(f"[*] Directorio creado: {BASE_DIR}")
    except OSError as e:
        print(f"[!] Advertencia: No se pudo crear el directorio {BASE_DIR}. Error: {e}")
 
SEED_URL = "http://wkkrcvje42625v7g77maufsgvqbu7eh7tgfvwzqrarqptfktqiaa6ayd.onion/darkweb-search-engines-v3/hidden-wiki" # Esta es la semilla, la pagina en la que el crawler va a empezar
OUTPUT_FILE = os.path.join(BASE_DIR, "onion_links.txt")
 
REQUEST_TIMEOUT = 20
MAX_LINKS_PER_DOMAIN = 15  # Esto es cuantas veces puede ser crawleado un dominio antes de empezar a descartarlo. Por ejemplo, si aparece 15 veces el dominio paginaX.onion entonces el crawler va a empezar a omitirlo
 
# --- GESTIÓN DE BASE DE DATOS (POSTGRES) ---
 
def get_db_connection():
    """Crea y retorna una conexión a la base de datos Postgres."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"[!] Error conectando a Postgres: {e}")
        sys.exit(1)
 
def init_db():
    """Inicializa las tablas en Postgres."""
    conn = get_db_connection()
    cursor = conn.cursor()
 
    # 1. Cola Principal (URLs pendientes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE
        );
    ''')
 
    # 2. Páginas Crawleadas (Resultados Exitosos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawled_pages (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            status_code INTEGER
        );
    ''')
 
    # 3. Cola de Reintentos (Errores 404)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS retry_queue (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE
        );
    ''')
 
    # 4. Estadísticas de Dominio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domain_stats (
            domain TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        );
    ''')
 
    conn.commit()
    conn.close()
 
def get_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return None
 
def update_page_title(conn, url, title, status_code):
    """Actualiza el título y status de una página ya visitada."""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE crawled_pages 
            SET title = %s, status_code = %s 
            WHERE url = %s
        """, (title, status_code, url))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[!] Error guardando título en DB: {e}")
 
def add_url_to_main_queue(conn, url):
    domain = get_domain(url)
    if not domain: return False
 
    cursor = conn.cursor()
 
    # Verificar si ya está en crawled_pages
    cursor.execute("SELECT 1 FROM crawled_pages WHERE url = %s", (url,))
    if cursor.fetchone():
        return False
 
    # Verificar límite de dominio
    cursor.execute("SELECT count FROM domain_stats WHERE domain = %s", (domain,))
    row = cursor.fetchone()
    current_count = row[0] if row else 0
 
    if current_count >= MAX_LINKS_PER_DOMAIN:
        return False 
 
    try:
        cursor.execute("INSERT INTO queue (url) VALUES (%s) ON CONFLICT DO NOTHING", (url,))
 
        if cursor.rowcount > 0:
            cursor.execute("""
                INSERT INTO domain_stats (domain, count) VALUES (%s, 1)
                ON CONFLICT (domain) DO UPDATE SET count = domain_stats.count + 1
            """, (domain,))
            conn.commit()
            return True
        conn.rollback()
        return False
 
    except Exception as e:
        conn.rollback()
        return False
 
def add_to_retry_queue(conn, url):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO retry_queue (url) VALUES (%s) ON CONFLICT DO NOTHING", (url,))
        conn.commit()
        print(f"[DB] 404 detectado. Guardado en tabla 'retry_queue': {url}")
    except Exception as e:
        conn.rollback()
 
def remove_from_retry_queue(conn, url):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM retry_queue WHERE url = %s", (url,))
    conn.commit()
 
def rotate_retry_url(conn, url, current_id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM retry_queue WHERE id = %s", (current_id,))
        cursor.execute("INSERT INTO retry_queue (url) VALUES (%s) ON CONFLICT DO NOTHING", (url,))
        conn.commit()
    except Exception:
        conn.rollback()
 
def get_next_url(conn, mode="NORMAL"):
    cursor = conn.cursor()
    table = "queue" if mode == "NORMAL" else "retry_queue"
 
    try:
        if mode == "NORMAL":
            query = sql.SQL("""
                DELETE FROM {table}
                WHERE id = (
                    SELECT id FROM {table} ORDER BY id ASC FOR UPDATE SKIP LOCKED LIMIT 1
                )
                RETURNING id, url;
            """).format(table=sql.Identifier(table))
 
            cursor.execute(query)
            row = cursor.fetchone()
 
            if row:
                id, url = row
                cursor.execute("INSERT INTO crawled_pages (url, status_code) VALUES (%s, 0) ON CONFLICT DO NOTHING", (url,))
                conn.commit()
                return url, id
 
        elif mode == "RETRY":
            cursor.execute("SELECT id, url FROM retry_queue ORDER BY id ASC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return row[1], row[0]
 
        conn.commit()
        return None, None
 
    except Exception as e:
        conn.rollback()
        print(f"[!] Error obteniendo URL: {e}")
        return None, None
 
def get_stats(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM queue")
    q_size = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM retry_queue")
    r_size = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM crawled_pages WHERE title IS NOT NULL")
    c_size = cursor.fetchone()[0]
    return q_size, r_size, c_size
 
# --- FUNCIONES DEL CRAWLER ---
 
def save_link_txt(title, url):
    """Mantiene una copia en TXT para visualización rápida."""
    try:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"TÍTULO: {title}\nURL: {url}\n{'-'*50}\n")
    except Exception:
        pass
 
def is_onion_link(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.endswith('.onion')
    except:
        return False
 
def ask_mode(conn):
    q_size, r_size, c_size = get_stats(conn)
    print("\n" + "="*40)
    print("   SELECTOR DE MODO CRAWLER (POSTGRES)")
    print("="*40)
    print(f"1. Modo Normal (Cola: {q_size} | Completados: {c_size})")
    print(f"2. Modo Reintentos (Cola 404: {r_size} enlaces)")
    print("="*40)
 
    while True:
        choice = input("Selecciona una opción (1 o 2): ").strip()
        if choice == "1": return "NORMAL"
        elif choice == "2": return "RETRY"
        print("Opción inválida.")
 
def crawl():
    init_db()
    conn = get_db_connection()
 
    # Verificar si hay datos iniciales
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM crawled_pages")
    visited_count = cursor.fetchone()[0]
    q_size, r_size, c_size = get_stats(conn)
 
    if q_size == 0 and r_size == 0 and visited_count == 0:
        print("[*] Base de datos nueva. Insertando semilla inicial.")
        add_url_to_main_queue(conn, SEED_URL)
 
    MODE = ask_mode(conn)
    print(f"\n[*] Iniciando en MODO: {MODE}")
    time.sleep(2)
 
    try:
        while True:
            current_url, row_id = get_next_url(conn, MODE)
 
            if not current_url:
                print(f"\n[*] No hay más enlaces en la cola ({MODE}).")
                break
 
            q_s, r_s, c_s = get_stats(conn)
            print(f"\n[Cola: {q_s} | 404s: {r_s} | Ok: {c_s}] Visitando: {current_url}")
 
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                }
                response = requests.get(current_url, proxies=PROXIES, headers=headers, timeout=REQUEST_TIMEOUT)
 
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_title = soup.title.string.strip() if soup.title else "Sin título"
 
                    print(f"[+] Título: {page_title}")
 
                    # 1. Guardar en DB (Actualizar el registro placeholder)
                    update_page_title(conn, current_url, page_title, 200)
 
                    # 2. Guardar en TXT (Copia de seguridad)
                    save_link_txt(page_title, current_url)
 
                    if MODE == "RETRY":
                        print("[+] ¡Recuperado! Eliminando de cola de 404.")
                        remove_from_retry_queue(conn, current_url)
 
                    links_found = 0
                    new_links = 0
                    for link in soup.find_all('a', href=True):
                        raw_url = link['href']
                        full_url = urljoin(current_url, raw_url).split('#')[0]
 
                        if is_onion_link(full_url):
                            if add_url_to_main_queue(conn, full_url):
                                new_links += 1
                            links_found += 1
 
                    print(f"[>] Enlaces: {links_found} | Nuevos agregados: {new_links}")
 
                elif response.status_code == 404:
                    print(f"[-] Error 404.")
                    # Actualizar status en crawled_pages aunque sea error, para registro
                    update_page_title(conn, current_url, "ERROR 404", 404)
 
                    if MODE == "NORMAL":
                        add_to_retry_queue(conn, current_url)
                    elif MODE == "RETRY":
                        rotate_retry_url(conn, current_url, row_id)
 
                else:
                    print(f"[-] Status: {response.status_code}")
                    update_page_title(conn, current_url, f"ERROR {response.status_code}", response.status_code)
                    if MODE == "RETRY":
                         rotate_retry_url(conn, current_url, row_id)
 
            except requests.exceptions.Timeout:
                print("[!] Timeout.")
                update_page_title(conn, current_url, "TIMEOUT", 0)
                if MODE == "RETRY": rotate_retry_url(conn, current_url, row_id)
            except requests.exceptions.ConnectionError:
                print("[!] Error de conexión.")
                update_page_title(conn, current_url, "CONN ERROR", 0)
                if MODE == "RETRY": rotate_retry_url(conn, current_url, row_id)
            except Exception as e:
                print(f"[!] Error: {e}")
 
            time.sleep(2)
 
    except KeyboardInterrupt:
        print("\n\n[!] Detenido por usuario.")
        conn.close()
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error crítico: {e}")
        conn.close()
 
    print("\n[*] Ciclo finalizado.")
    conn.close()
 
if __name__ == "__main__":
    crawl()