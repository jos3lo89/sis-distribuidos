import socket  # Módulo para sockets en Python 
 
# IP del servidor (cambiar a la IP real del equipo servidor en la LAN) 
HOST = '192.168.101.10' 

PORT  =  5000    #  Debe  coincidir  con  el  puerto  usado  por  el servidor 
 
# Crear socket TCP (SOCK_STREAM) con protocolo IPv4 (AF_INET) 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
# Conectar al servidor usando su IP y puerto 
cliente.connect((HOST, PORT)) 
 
# Solicitar al usuario el nombre del producto a consultar 
producto = input("Ingrese el nombre del producto: ") 
 
# Enviar el producto codificado en bytes 
cliente.send(producto.encode()) 
 
# Recibir respuesta del servidor (máximo 1024 bytes) 
#  1024  es  el  tamaño  del  buffer,  suficiente  para  mensajes pequeños 
respuesta = cliente.recv(1024).decode() 
 
# Mostrar la respuesta del servidor 
print(f"Respuesta del servidor: {respuesta}") 
 
# Cerrar conexión con el servidor 
cliente.close()