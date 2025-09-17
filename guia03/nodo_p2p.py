import socket 
import threading 
import os 
 
# CONFIGURACIÓN DEL NODO 
IP_LOCAL = '0.0.0.0'          # Escuchar en todas las interfaces de red 
PUERTO = 6000                 # Puerto que usa el sistema P2P 
CARPETA_ARCHIVOS = 'compartidos'  # Carpeta compartida

# Crear carpeta si no existe 
if not os.path.exists(CARPETA_ARCHIVOS): 
    os.makedirs(CARPETA_ARCHIVOS) 
 
# Lista de peers (IPs de otros nodos en la red) 
peers = [ 
    ('192.168.101.10', 6000), 
    # ('192.168.1.11', 6000), 
    # ('192.168.1.12', 6000) 
]

# ------------------------ SERVIDOR DEL NODO ---------------------------- 
 
# Escucha y atiende múltiples conexiones 
def atender_conexiones(): 
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    servidor.bind((IP_LOCAL, PUERTO)) 
    servidor.listen(5) 
    print(f"[ESCUCHANDO] Nodo activo en puerto {PUERTO}") 
 
    while True:
        conn, addr = servidor.accept() 
        print(f"[CONEXIÓN] Desde {addr}") 
        threading.Thread(target=gestionar_peticion, args=(conn,)).start() 
 
# Atiende cada tipo de solicitud recibida 
def gestionar_peticion(conn): 
    try: 
        solicitud = conn.recv(1024).decode() 
 
        # Buscar archivo 
        if solicitud.startswith("BUSCAR:"): 
            nombre = solicitud.split(":", 1)[1] 
            ruta = os.path.join(CARPETA_ARCHIVOS, nombre)
            if os.path.exists(ruta): 
                conn.send(b"SI") 
            else: 
                conn.send(b"NO") 

        # Descargar archivo 
        elif solicitud.startswith("DESCARGAR:"): 
            nombre_archivo = solicitud.split(":", 1)[1] 
            ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo) 
            if os.path.exists(ruta): 
                conn.send(b"OK") 
                with open(ruta, 'rb') as f: 
                    while True: 
                        datos = f.read(1024) 
                        if not datos: 
                            break 
                        conn.sendall(datos) 
                print(f"[ENVÍO COMPLETO] {nombre_archivo}") 
            else: 
                conn.send(b"NOFILE") 
    except Exception as e: 
        print(f"[ERROR] {e}")
    finally: 
        conn.close()


# ------------------------ CLIENTE DEL NODO ----------------- 
 
# Busca en todos los peers si tienen el archivo 
def buscar_en_peers(nombre_archivo): 
    disponibles = [] 
    for ip, puerto in peers: 
        try: 
            s = socket.socket() 
            s.settimeout(2) 
            s.connect((ip, puerto)) 
            s.send(f"BUSCAR:{nombre_archivo}".encode()) 
            respuesta = s.recv(1024) 
            if respuesta == b"SI": 
                disponibles.append((ip, puerto)) 
            s.close() 
        except: 
            pass 
    return disponibles 
 
# Descarga el archivo desde el peer seleccionado 
def descargar_archivo(ip_destino, nombre_archivo): 
    try: 
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        cliente.connect((ip_destino, PUERTO)) 
        cliente.send(f"DESCARGAR:{nombre_archivo}".encode()) 
 
        respuesta = cliente.recv(1024) 
        if respuesta == b"OK": 
            ruta_destino = os.path.join(CARPETA_ARCHIVOS, nombre_archivo) 
            with open(ruta_destino, 'wb') as f: 
                while True: 
                    datos = cliente.recv(1024) 
                    if not datos: 
                        break 
                    f.write(datos) 
            print(f"[DESCARGADO EN COMPARTIDOS] {nombre_archivo}") 
        else: 
            print("[NO ENCONTRADO]  El archivo no está disponible.") 
        cliente.close() 
 
    except Exception as e: 
        print(f"[ERROR AL DESCARGAR] {e}") 
 

# ---------------------- INICIO DEL SISTEMA ----------------- 
 
# Lanzar servidor en un hilo aparte 
threading.Thread(target=atender_conexiones, daemon=True).start() 
 
# Menú principal 
while True: 
    print("\n--- MENÚ P2P ---") 
    print("1. Ver archivos compartidos") 
    print("2. Buscar y descargar archivo") 
    print("3. Salir") 
    opcion = input("Seleccione una opción: ") 
 
    if opcion == '1': 
        print("\nArchivos disponibles en este nodo:") 
        for f in os.listdir(CARPETA_ARCHIVOS): 
            print(" -", f) 
 
    elif opcion == '2': 
        archivo = input("Nombre del archivo que deseas buscar: ") 
        disponibles = buscar_en_peers(archivo) 
 
        if not disponibles: 
            print("No se encontró ese archivo en la red.") 
        else: 
            print("Archivo disponible en:")
            for idx, (ip, _) in enumerate(disponibles): 
                print(f"{idx+1}. {ip}") 
            eleccion = int(input("Selecciona de dónde deseas descargar (número): ")) 
            ip_seleccionada = disponibles[eleccion - 1][0] 
            descargar_archivo(ip_seleccionada, archivo) 
 
    elif opcion == '3': 
        print("Saliendo...") 
        break 
    else: 
        print("Opción inválida.")
