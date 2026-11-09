import os
import json

ARCHIVO = "contactos.dat"
INDICE = "indice.json"

# Tamaño fijo: id(10), nombre(30), telefono(15), correo(25), ciudad(20) = 100 caracteres
TAMANIO_REGISTRO = 100

# +++++
# CARGAR INDICE
# +++++
def CARGAR_INDICE():
    if not os.path.exists(INDICE):
        return {}
    try:
        with open(INDICE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except Exception:
        return {}

# +++++
# GUARDAR INDICE
# +++++
def GUARDAR_INDICE(indice):
    with open(INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4, ensure_ascii=False)

# +++++
# AGREGAR CONTACTO
# +++++
def AGREGAR_CONTACTO(id_cont, nombre, telefono, correo, ciudad):
    indice = CARGAR_INDICE()
    if str(id_cont) in indice:
        return False, "El ID ya existe."

    # Formateando con ljust() para completar cada campo con espacios
    registro = (
        str(id_cont).ljust(10) +
        nombre.ljust(30)[:30] +
        telefono.ljust(15)[:15] +
        correo.ljust(25)[:25] +
        ciudad.ljust(20)[:20]
    )

    with open(ARCHIVO, "a", encoding="utf-8") as archivo:
        posicion = archivo.tell() // TAMANIO_REGISTRO
        archivo.write(registro)
    
    indice[str(id_cont)] = posicion
    GUARDAR_INDICE(indice)
    return True, "Contacto almacenado correctamente."

# +++++
# BUSCAR CONTACTO
# +++++
def BUSCAR_CONTACTO(id_cont):
    indice = CARGAR_INDICE()
    if str(id_cont) not in indice:
        return None, "El id no existe."
    
    posicion_registro = indice[str(id_cont)]
    posicion_byte = posicion_registro * TAMANIO_REGISTRO

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            archivo.seek(posicion_byte)
            print(f"Posición actual dentro del archivo (tell): {archivo.tell()}")
            datos = archivo.read(TAMANIO_REGISTRO)
            
            if len(datos) == TAMANIO_REGISTRO:
                contacto = {
                    "id": datos[0:10].strip(),
                    "nombre": datos[10:40].strip(),
                    "telefono": datos[40:55].strip(),
                    "correo": datos[55:80].strip(),
                    "ciudad": datos[80:100].strip()
                }
                return contacto, "Éxito"
    except FileNotFoundError:
        pass
    
    return None, "Error al leer el archivo."

# +++++
# MODIFICAR CONTACTO
# +++++
def MODIFICAR_CONTACTO(id_cont, nombre, telefono, correo, ciudad):
    indice = CARGAR_INDICE()
    if str(id_cont) not in indice:
        return False, "El id no existe."
    
    posicion_byte = indice[str(id_cont)] * TAMANIO_REGISTRO
    registro = (
        str(id_cont).ljust(10) +
        nombre.ljust(30)[:30] +
        telefono.ljust(15)[:15] +
        correo.ljust(25)[:25] +
        ciudad.ljust(20)[:20]
    )

    with open(ARCHIVO, "r+", encoding="utf-8") as archivo:
        archivo.seek(posicion_byte)
        archivo.write(registro)
    
    return True, "Contacto actualizado correctamente."