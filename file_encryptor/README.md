# File Encryptor

Encriptador y desencriptador de archivos usando cifrado AES (Fernet).

## 📋 Descripción

File Encryptor permite encriptar y desencriptar archivos individuales o directorios completos usando contraseñas. Utiliza el algoritmo AES a través de la librería Fernet de cryptography.

## ✨ Características

- 🔐 **Cifrado AES**: Usa cifrado simétrico seguro
- 🔑 **Basado en contraseña**: Deriva clave desde contraseña usando PBKDF2
- 📁 **Archivos y directorios**: Encripta archivos individuales o carpetas completas
- 🛡️ **Seguro**: Usa iteraciones PBKDF2 para protección contra fuerza bruta
- 💾 **Preserva originales**: Crea archivos .encrypted sin modificar originales

## 🚀 Instalación

### Requisitos

```bash
pip install cryptography==41.0.7
```

### Ejecución

```bash
python file_encryptor.py
```

## ⚠️ Advertencias

1. **Pérdida de contraseña**: Si olvidas la contraseña, los archivos son irrecuperables
2. **No encripta en lugar**: Crea archivos .encrypted, no modifica originales
3. **Elimina originales manualmente**: Si quieres, elimina los originales después de verificar

