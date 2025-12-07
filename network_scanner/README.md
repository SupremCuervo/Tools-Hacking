# Network Scanner

Escáner de red completo que identifica dispositivos activos en tu red local y escanea puertos abiertos.

## 📋 Descripción

Network Scanner es una herramienta que escanea tu red local para encontrar dispositivos activos, obtener sus hostnames y detectar puertos abiertos. Utiliza threading para realizar escaneos rápidos y eficientes.

## ✨ Características

- 🔍 **Detección automática de red**: Detecta automáticamente tu red local
- 🚀 **Escaneo rápido**: Utiliza múltiples threads para escaneo paralelo
- 🌐 **Detección de hostnames**: Intenta obtener el nombre de cada dispositivo
- 🔌 **Escaneo de puertos**: Escanea puertos comunes en cada host
- 📊 **Resultados organizados**: Muestra resultados en formato tabla

## 🚀 Instalación

No requiere dependencias externas. Solo usa librerías estándar de Python 3.

```bash
python network_scanner.py
```

## 📖 Uso

### Uso Básico

Simplemente ejecuta el script:

```bash
python network_scanner.py
```

El script automáticamente:
1. Detecta tu IP local
2. Calcula el rango de red (ej: 192.168.1.0/24)
3. Escanea todos los hosts en el rango
4. Muestra dispositivos activos con sus puertos abiertos

## ⚠️ Notas Importantes

1. **Permisos**: En algunos sistemas puede requerir permisos de administrador
2. **Firewall**: Asegúrate de que el firewall no bloquee las conexiones
3. **Velocidad**: El escaneo puede tardar varios minutos dependiendo del tamaño de la red
4. **Uso ético**: Solo escanea redes que poseas o tengas permiso para escanear

