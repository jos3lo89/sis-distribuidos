import socket
import sqlite3
import threading

HOST = '0.0.0.0'
PORT = 5000

def atender_cliente(conn, addr): 
  print(f"[+] Conectado con {addr}") 
  try:
    data = conn.recv(1024).decode()   
    print(f"[{addr}] Consulta recibida: {data}")
    conexion = sqlite3.connect('inventario.db') 
    cursor = conexion.cursor() 
    cursor.execute("SELECT  cantidad  FROM  productos  WHERE nombre = ?", (data,)) 
    resultado = cursor.fetchone() 
    conexion.close()
    if resultado: 
      respuesta = f"Cantidad disponible: {resultado[0]}" 
    else: 
      respuesta = "Producto no encontrado" 
    conn.send(respuesta.encode())
  except Exception as e: 
    print(f"[{addr}] Error: {e}")
    conn.send("Error en la consulta".encode())
  finally:
    conn.close()
    print(f"[-] Conexión con {addr} cerrada")

 
 
# Crear socket del servidor 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
servidor.bind((HOST, PORT)) 
servidor.listen(5)  # Acepta hasta 5 conexiones pendientes 
 
print(f"Servidor  en  ejecución.  Escuchando  en {HOST}:{PORT}...") 
 
# Bucle principal para aceptar clientes 
while True: 
    conn, addr = servidor.accept()  # Esperar conexión 
    # Crear un hilo para manejar al cliente sin bloquear el servidor 
    hilo = threading.Thread(target=atender_cliente, args=(conn, addr)) 
    hilo.start()