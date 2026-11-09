import json
import os
from reportlab.pdfgen import canvas
import controlContactos

JSON_EXPORT = "contactos_exportados.json"

# +++++
# EXPORTAR JSON
# +++++
def EXPORTAR_A_JSON():
    if not os.path.exists(controlContactos.ARCHIVO):
        return False, "El archivo de contactos no existe."
        
    contactos = []
    with open(controlContactos.ARCHIVO, "r", encoding="utf-8") as archivo:
        while True:
            datos = archivo.read(controlContactos.TAMANIO_REGISTRO)
            if not datos or len(datos) < controlContactos.TAMANIO_REGISTRO:
                break
                
            contacto = {
                "id": datos[0:10].strip(),
                "nombre": datos[10:40].strip(),
                "telefono": datos[40:55].strip(),
                "correo": datos[55:80].strip(),
                "ciudad": datos[80:100].strip()
            }
            contactos.append(contacto)

    with open(JSON_EXPORT, "w", encoding="utf-8") as archivo_json:
        json.dump(contactos, archivo_json, indent=4, ensure_ascii=False)
        
    return True, "Información exportada a JSON correctamente."

# +++++
# GENERAR REPORTE PDF
# +++++
def GENERAR_REPORTE_PDF():
    if not os.path.exists(JSON_EXPORT):
        return False, "Debe exportar a JSON primero."
        
    try:
        with open(JSON_EXPORT, "r", encoding="utf-8") as archivo:
            contactos = json.load(archivo)
            
        pdf = canvas.Canvas("reporte_contactos.pdf")
        pdf.drawString(100, 800, "REPORTE DE CONTACTOS (Generado desde JSON)")
        
        y = 760
        for cont in contactos:
            if y < 50: # Salto de página simple
                pdf.showPage()
                y = 800
                
            texto = f"ID: {cont['id']} | Nombre: {cont['nombre']} | Tel: {cont['telefono']}"
            pdf.drawString(50, y, texto)
            y = y - 20
            
        pdf.save()
        return True, "PDF básico generado."
    except Exception as e:
        return False, f"Error al generar PDF: {e}"