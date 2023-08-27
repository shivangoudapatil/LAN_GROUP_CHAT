import socket

def server(obj):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', obj.port)
        server_socket.bind(server_address)

        print("Server is listening for broadcasts... ", obj.port)

        while True:

            data, client_address = server_socket.recvfrom(1024)
            sig = data.decode()[0]
            msg = data.decode()[1:]

            if sig == '*':
                obj.queue.put(obj.users[client_address[0]] + " : " + msg)
                send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                send_sock.sendto('+'.encode(), (client_address[0], obj.port))
                send_sock.close()

            elif sig == '#':
                obj.users[client_address[0]] = msg
                obj.msgs[client_address[0]] = obj.tm
                obj.queue.put(msg + " Connected")
                print(client_address)
                send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                send_sock.sendto(obj.name.encode(), (client_address[0], obj.port))
                send_sock.close()
                print("sent")

            elif sig == '+':
                obj.msgs[client_address[0]] += 1

            elif sig == '!':
                obj.queue.put(obj.users[msg] + " disconnected")
                obj.users.pop(msg)
                obj.msgs.pop(msg)

            else:
                print(f"unknown msg from {client_address}")