import os
import hashlib
import zipfile
import controlContactos

HASH_FILE = "contactos.sha256"
ZIP_FILE = "respaldo_contactos.zip"

# +++++
# VERIFICAR INTEGRIDAD
# +++++
def ACTUALIZAR_HASH():
    if not os.path.exists(controlContactos.ARCHIVO): return
    
    sha256 = hashlib.sha256()
    with open(controlContactos.ARCHIVO, "rb") as archivo:
        sha256.update(archivo.read())
        
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(sha256.hexdigest())

def VERIFICAR_INTEGRIDAD():
    if not os.path.exists(controlContactos.ARCHIVO) or not os.path.exists(HASH_FILE):
        return True, "Archivos no inicializados o falta hash."
        
    sha256 = hashlib.sha256()
    with open(controlContactos.ARCHIVO, "rb") as archivo:
        sha256.update(archivo.read())
    hash_actual = sha256.hexdigest()
    
    with open(HASH_FILE, "r", encoding="utf-8") as f:
        hash_guardado = f.read().strip()
        
    if hash_actual != hash_guardado:
        return False, "ALERTA: El archivo de contactos fue modificado externamente."
    return True, "Integridad verificada correctamente."

# +++++
# CREAR RESPALDO ZIP
# +++++
def CREAR_RESPALDO():
    if not os.path.exists(controlContactos.ARCHIVO) or not os.path.exists(controlContactos.INDICE):
        return False, "Faltan archivos base para respaldar."
        
    tamano_original = os.path.getsize(controlContactos.ARCHIVO) + os.path.getsize(controlContactos.INDICE)
    
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(controlContactos.ARCHIVO)
        zipf.write(controlContactos.INDICE)
        
    tamano_comprimido = os.path.getsize(ZIP_FILE)
    
    return True, f"Respaldo creado.\nTamaño original: {tamano_original} bytes\nTamaño comprimido: {tamano_comprimido} bytes"

# +++++
# METADATOS Y PERMISOS
# +++++
def OBTENER_METADATOS():
    if not os.path.exists(controlContactos.ARCHIVO):
        return False, "El archivo no existe."
        
    stats = os.stat(controlContactos.ARCHIVO)
    lectura = os.access(controlContactos.ARCHIVO, os.R_OK)
    escritura = os.access(controlContactos.ARCHIVO, os.W_OK)
    
    info = (
        f"Tamaño: {stats.st_size} bytes\n"
        f"Última modificación: {stats.st_mtime}\n"
        f"Permisos lectura: {'Sí' if lectura else 'No'}\n"
        f"Permisos escritura: {'Sí' if escritura else 'No'}"
    )
    return True, info