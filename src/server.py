import socket

TCP_IP = ""
TCP_PORT = 6666
BUFFER_SIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print ('Connection address:', addr)
    data = conn.recv(BUFFER_SIZE)
    if data: 
        print ("received data:", data)
        conn.send(data)  # echo
conn.close()

