import socket
import threading
from network_utils import get_local_ip
from network_utils import calculate_broadcast_address
from server_thread import server

def scan_network(obj, input_text):
    my_ip = get_local_ip()
    obj.name = input_text
    message = "#" + input_text
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ser_sock_add = ('0.0.0.0', obj.port)
    ser_sock.bind(ser_sock_add)
    client_socket.sendto(message.encode(), (str(calculate_broadcast_address()), obj.port))
    client_socket.close()

    ser_sock.settimeout(1)
    while True:

        try:
            reply, server_address = ser_sock.recvfrom(1024)
            print(server_address)
            if server_address[0] != my_ip: 
                print("name is : ", reply.decode())
                obj.users[server_address[0]] = reply.decode()
                obj.msgs[server_address[0]] = obj.tm

        except socket.timeout:
            break

    ser_sock.close()
    print(obj.users)
    obj.queue.put(obj.name + " Connected")
    server_t = threading.Thread(target=server, args = (obj,))
    server_t.start()