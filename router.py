import socket
import requests
import json
server_host = '0.0.0.0'
server_port = 8000
router_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
router_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
router_socket.bind((server_host,server_port))
router_socket.listen(5)
print("Listening on port %s....." %server_port)
nodes=[8001,8002]
current_index = 0
while True:
	client_connection,client_address = router_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)

    headers = request.split('\n')
    parts = headers[0].split()

    if len(parts) < 2:
        client_connection.close()
        continue

    method, path = parts[0], parts[1]
    
    start_index = current_index
    current_index = (current_index + 1) % len(nodes)
    if path == '/task' and method == 'POST':
    	body = request.split('\r\n\r\n')[-1]
    	success =  False
    	for i in range(len(nodes)):
    		port = nodes[(start_index + i) % len(nodes)]
    		try:
    			response_from_workerNode = requests.post(
    				f"http://localhost:{port}/task",
    				data=body,
    				headers={"Content-Type": "application/json"},
    				timeout=2
				)
    			if response_from_workerNode.status_code == 200:
    				response_body = response_from_workerNode.text

    				response = (
    					"HTTP/1.0 200 OK\n"
    					"Content-Type: application/json\r\n"
    					f"Content-Length: {len(response_body)}\r\n\r\n"
    					f"{response_body}"
    					)
					client_connection.sendall(response.encode())
					success = True
					break
			except requests.exceptions.RequestException:
				print(f"Node {port} failed")
				continue

		if not success:
			response_body = '{"error": "All nodes are down"}'
			response = (
				"HTTP/1.0 500 Internal Server Error\n"
				"Content-Type: application/json\r\n"
				f"Content-Length: {len(response_body)}\r\n\r\n"
				f"{response_body}"
			)
			client_connection.sendall(response.encode())
	client_connection.close()
	continue
