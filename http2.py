
import socket
import json

SERVER_HOST = '0.0.0.0' 

SERVER_PORT = int(input("Enter port: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print('Listening on Port %s ....' % SERVER_PORT)

while True:

    client_connection,client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)



    headers = request.split('\n')
    parts = headers[0].split()
    if len(parts)<2:
        client_connection.close()
        continue
    method,path = parts[0],parts[1]

    if path == '/health':
        response_b = '{"Status": "Alive"}'
        response = ('HTTP/1.0 200 OK\r\n'
            'Content-Type:application/json\r\n'
            f"Content-Length: {len(response_b)}\r\n\r\n"
            f"{response_b}")
    elif path == '/info':
        response_b = '{"status": "alive"}'
        response = ("HTTP/1.0 200 OK\r\n"
            "Content-Type:application/json\r\n"
            f"Content-Length:{len(response_b)}\r\n\r\n"
            f"{response_b}")
    elif path == '/task' and method == 'POST':
        try:
            body = request.split('\r\n\r\n')[1]
            data = json.loads(body)
            task = data.get("task")
            value = data.get("value")
            match(task):
                case "square":
                    result = value*value
                case "double":
                    result = value*2
                case _:
                    result = "unknown task"
            response_b = json.dumps({"result":result})
            response = ("HTTP/1.0 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(response_b)}\r\n\r\n"
                f"{response_b}")
        except Exception as e:
            response_b = json.dumps({"error": str(e)})
            response = (
                "HTTP/1.0 400 Bad Request\r\n\r\n"
                f"{response_b}"
            )
    else:
        if path == '/':
            filename = 'index.html'
        else:
            filename = path[1:]
        try:
            file = open(filename)
            content= file.read()
            file.close()

            response = 'HTTP/1.0 200 OK\r\n\r\n' + content
        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n File not found\r\n\r\nPlease access a Valid file'

    
    client_connection.sendall(response.encode())

    client_connection.close()

server_socket.close()

