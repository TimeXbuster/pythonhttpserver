#Building a basic HTTP/1.0 Server using sockets

#Sockets are basically one of the endpoint of a 2 way communication link between two programs running on a network
#If a building has a street address(IP) and each resident(program) has an apartmet nuber(port) then the socket is the actual physical door through which people(data) enter and leave

import socket

#Defining Socket Host and Port
SERVER_HOST = '0.0.0.0' #This means All IP adresses are allowed
SERVER_PORT = 8000 #the computer is listening on port 8000

#Creating the Socket


#Creating the server_socket variable

#we have set it to AF_INET it is the Internet Protocol v4 (IPv4) address family
#AF_INET tells the socket what type of addresses to communicate with

'''SOCK_STREAM is a socket type that provides sequenced(no duplication or change in sequence of transmissioned data),
it is basically like a phone call it establishes two way connection between two sockets before any data is sent or recieved
in case of IPv4 as defined earlier due to AF_INET it uses TCP by default'''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#setsockopt is basically like opening the settings menu in the mobile it basically takes four arguments
#what phone/socket are we adjusting server_socket here
#what level are we adjusting a general level (sol_socket) or any specific protocol setting
#which specific setting we are changing(so_reuseaddr)
#what are we setting it to 1 for ON, 0 for off

'''
SO_REUSEADDR is the specific rule which means reuse address it tells the socket to reconnect in case there is a time_wait basically a designated delay by us before a new connection is made after the older one closes 
this is helpful in case i accidentally lost my connection or i made some change and restarted the socket now instead of wiating minutes for the socket to clean the older connection and build a new one for the same address 
it just reuses the older one this helps in reducing waiting time 
it also helps clear errors like OSError: [Errno 48] Address already in use
which basically means that the old connection has not been cleared so wait but i want to connect using the same adress anyway so instead of building a new one from scratch it helps me hop onto the existing one'''

'''sol_socket is a constant that specifies the level at which a socket option should be applied 
It basically tells the code to look in general Socket rules Category instead of the category for a specific protocol like TCP
Basically it says that if i change a rule it should apply to the entire socket not just a specific protocol like TCP or IP
Going by Real life example
the Socket is a Building and the plumbing within it is TCP level 
sol_socket tells to the Code to basically affect the entire building on rule changes not just the plumbing
'''
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind ties the Socket to a specific IP address and Port number so that it doesnt recieve requests from any port or ip address
#ifnot specified the os picks a random one for you which makes it hard for the clients to know where to send it
server_socket.bind((SERVER_HOST, SERVER_PORT))

#listen opens the socket to incoming requests basically like waiting for a knock on a door after opening a shop
#the 1 tells the number of connections that can wait in line while the socket is talking ti the current one if a 2nd one tries to enter the wait line at exact milisecond they get a connection refused error
server_socket.listen(1)

print('Listening on Port %s ....' % SERVER_PORT)

while True:			#this is a loop that tells to continue to keep the socket open otherwise it would be closed after just one connection but this keeps it going (one connection connects it does its work disconnects then next one can connect)

	client_connection,client_address = server_socket.accept()
	#accept tells the server to wait ustil someone tries to connect
	#the code is paused here until somebody connects
	#when somebody does connect it gives two things a connection basically like a private phone line and the id/address (ip and port) of the person who tried to connect

	request = client_connection.recv(1024).decode()
	print(request)
	#the recv(1024) tells socket to hold a bucket that can catch upto 1024 bytes of data from the connection
	#decode translates the binary to human readable text

	#This is just a test to open an html file and send its contents to the browser when it asks for the root of the server
	#this is a predefined test but we can make it dynamic too
	# file=open('index.html')
	# content = file.read()
	# file.close()

	#This is a dynamic implementation of the above feature
	#Bascially we are parsing/extracting the filename from the request string sent by the browser and opening the file it is requesting '/' (root) by default
	headers = request.split('\n')
	filename = headers[0].split()[1]
	if filename == '/':
		filename='index.html'
	try:
		file = open(filename)
		content= file.read()
		file.close()

		response = 'HTTP/1.0 200 OK\n\n' + content
	except FileNotFoundError:
		response = 'HTTP/1.0 404 NOT FOUND\n\n File not found\n\nPlease access a Valid file'
	#This is an error exception catching in case somebody tries to access a file not present
	#this prevents the server from straight up crashing and exiting when it encounters this error and instead returns this error message

	
	client_connection.sendall(response.encode())
	#sendall sends the defined response back through the same connection
	#encode converts the text to binary for transfer

	client_connection.close()
	#The connection with this customer is closed and the loop starts looking for a new customer again

server_socket.close()

#This program sends Hello world string as a response to http://localhost:8000/

#For AF_INET there is also AF_INET6 which uses IPv6 address family
#Sock_STREAM is an alternative to SOCK_DGRAM(datagram sockets) which uses UDP by default but the problem is that it is connctionless and unreliable(data packets may be lost in case there was an error in connection since there was no beforehand connection established before data transfer)
#there is advantages to using it too as they can be capped to have a maximum length but SOCK_STREAM cannot




#This is what the terminal shows on running
#python3 http.py
#The GET here is te browser asking for the root of the server

'''Listening on Port 8000 ....
GET / HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i'''
