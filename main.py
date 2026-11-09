import tkinter as tk
from tkinter import messagebox, simpledialog
import controlContactos
import RegistrosContactos
import ManejoDatos

# +++++
# CONFIGURACIÓN VISUAL
# +++++
COLOR_FONDO = "cyan"
COLOR_BOTON = "yellow"
COLOR_TEXTO = "black"
FUENTE_BOTON = ("Arial", 10, "bold")

# +++++
# FUNCIONES DE INTERFAZ
# +++++
def accion_agregar():
    id_cont = simpledialog.askstring("Entrada", "ID (número):")
    if not id_cont: return
    nombre = simpledialog.askstring("Entrada", "Nombre:")
    tel = simpledialog.askstring("Entrada", "Teléfono:")
    correo = simpledialog.askstring("Entrada", "Correo:")
    ciudad = simpledialog.askstring("Entrada", "Ciudad:")
    
    exito, msg = controlContactos.AGREGAR_CONTACTO(id_cont, nombre, tel, correo, ciudad)
    ManejoDatos.ACTUALIZAR_HASH()
    actualizar_pantalla(msg)
    messagebox.showinfo("Resultado", msg)

def accion_buscar():
    id_cont = simpledialog.askstring("Buscar", "ID a buscar:")
    if not id_cont: return
    contacto, msg = controlContactos.BUSCAR_CONTACTO(id_cont)
    if contacto:
        info = f"--- Contacto Encontrado ---\n\nID: {contacto['id']}\nNombre: {contacto['nombre']}\nTel: {contacto['telefono']}\nCorreo: {contacto['correo']}\nCiudad: {contacto['ciudad']}"
        actualizar_pantalla(info)
    else:
        actualizar_pantalla(msg)
        messagebox.showwarning("Error", msg)

def accion_modificar():
    id_cont = simpledialog.askstring("Modificar", "ID a modificar:")
    if not id_cont: return
    contacto, msg = controlContactos.BUSCAR_CONTACTO(id_cont)
    if not contacto:
        messagebox.showwarning("Error", msg)
        return
        
    nombre = simpledialog.askstring("Modificar", "Nuevo Nombre:", initialvalue=contacto['nombre'])
    tel = simpledialog.askstring("Modificar", "Nuevo Teléfono:", initialvalue=contacto['telefono'])
    correo = simpledialog.askstring("Modificar", "Nuevo Correo:", initialvalue=contacto['correo'])
    ciudad = simpledialog.askstring("Modificar", "Nueva Ciudad:", initialvalue=contacto['ciudad'])
    
    exito, msg = controlContactos.MODIFICAR_CONTACTO(id_cont, nombre, tel, correo, ciudad)
    ManejoDatos.ACTUALIZAR_HASH()
    actualizar_pantalla(msg)
    messagebox.showinfo("Resultado", msg)

def accion_exportar():
    exito, msg = RegistrosContactos.EXPORTAR_A_JSON()
    if exito:
        ex2, msg2 = RegistrosContactos.GENERAR_REPORTE_PDF()
        info = f"{msg}\n{msg2}"
        actualizar_pantalla(info)
        messagebox.showinfo("Exportar", info)
    else:
        actualizar_pantalla(msg)
        messagebox.showwarning("Error", msg)

def accion_respaldo():
    exito, msg = ManejoDatos.CREAR_RESPALDO()
    actualizar_pantalla(msg)
    messagebox.showinfo("Respaldo", msg)

def accion_info():
    exito, msg = ManejoDatos.OBTENER_METADATOS()
    actualizar_pantalla(f"--- Metadatos del Archivo ---\n\n{msg}")
    
def accion_ayuda():
    messagebox.showinfo("Ayuda", "La ayuda no esta ayudando")

def actualizar_pantalla(texto):
    lbl_pantalla.config(text=texto)

# +++++
# INICIALIZACION, MARCOS Y MENU
# +++++
def main():
    global lbl_pantalla
    
    root = tk.Tk()
    root.title("Agenda de Contactos")
    root.geometry("550x350")
    root.config(bg=COLOR_FONDO)
    
    # Validar integridad al iniciar
    integro, msg_integridad = ManejoDatos.VERIFICAR_INTEGRIDAD()
    if not integro:
        messagebox.showwarning("Advertencia de Seguridad", msg_integridad)

    # --- MENÚ SUPERIOR ---
    menubar = tk.Menu(root)
    menu_ayuda = tk.Menu(menubar, tearoff=0)
    menu_ayuda.add_command(label="Ayuda", command=accion_ayuda)
    menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
    root.config(menu=menubar)
    
    # --- DISTRIBUCIÓN CON MARCOS (FRAMES) ---
    # Panel Izquierdo (Botones)
    frame_izquierdo = tk.Frame(root, bg=COLOR_FONDO)
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
    
    tk.Label(frame_izquierdo, text="Menú Rápido", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Arial", 12, "bold")).pack(pady=(0, 10))
    
    botones = [
        ("Agregar Contacto", accion_agregar),
        ("Buscar por ID", accion_buscar),
        ("Modificar Contacto", accion_modificar),
        ("Exportar JSON/PDF", accion_exportar),
        ("Crear Respaldo ZIP", accion_respaldo),
        ("Info. del Archivo", accion_info)
    ]
    
    for texto, comando in botones:
        btn = tk.Button(frame_izquierdo, text=texto, command=comando, 
                        bg=COLOR_BOTON, fg=COLOR_TEXTO, font=FUENTE_BOTON, width=18, relief="raised")
        btn.pack(pady=5)

    # Panel Derecho (Área Central de Información)
    frame_derecho = tk.Frame(root, bg="white", relief="sunken", borderwidth=2)
    frame_derecho.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=15, pady=15)
    
    lbl_titulo_pantalla = tk.Label(frame_derecho, text="Monitor de Sistema", bg="white", font=("Arial", 12, "bold"))
    lbl_titulo_pantalla.pack(pady=10)
    
    lbl_pantalla = tk.Label(frame_derecho, text="Bienvenido a la Agenda de Contactos.\nSeleccione una acción en el panel izquierdo.", 
                            bg="white", font=("Arial", 10), justify=tk.LEFT)
    lbl_pantalla.pack(pady=20, padx=10, anchor="w")
    
    root.mainloop()

if __name__ == "__main__":
    main()