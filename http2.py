
import socket

SERVER_HOST = '0.0.0.0' #This means All IP adresses are allowed
SERVER_PORT = 8000 #the computer is listening on port 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print('Listening on Port %s ....' % SERVER_PORT)

while True:         #this is a loop that tells to continue to keep the socket open otherwise it would be closed after just one connection but this keeps it going (one connection connects it does its work disconnects then next one can connect)

    client_connection,client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)



    headers = request.split('\n')
    parts = headers[0].split()
    if len(parts)<2:
        client_connection.close()
        return
    method,path = parts[0],parts[1]

    if path == '/health':
        response_b = {'Status:','Alive'}
        response = ('HTTP/1.0 200 OK\n'
            'Content-Type:application/json\n'
            f"Content-Length: {len(response_b)}\n"
            f"{response_b}")
    else:
        if path == '/':
            filename = 'index.html'
        else:
            filename = path[1:]
        try:
            file = open(filename)
            content= file.read()
            file.close()

            response = 'HTTP/1.0 200 OK\n\n' + content
        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\n\n File not found\n\nPlease access a Valid file'

    
    client_connection.sendall(response.encode())

    client_connection.close()

server_socket.close()

