import socket
import time

def new_message_handler(obj, input_text):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    input_text = '*' + input_text
    obj.tm += 1
    for user_ip in obj.users:
        client_socket.sendto(input_text.encode(), (user_ip, obj.port))

    time.sleep(1)
    obj.queue.put("You: " + input_text[1:])

    dead_nodes = []

    for user_ip in obj.msgs:
        if obj.msgs[user_ip] != obj.tm:
            dead_nodes.append(user_ip)

    for user_ip in dead_nodes:
        obj.queue.put(obj.users[user_ip] + " Disconnected !")
        obj.users.pop(user_ip)
        obj.msgs.pop(user_ip)

    for user_ip in obj.users:
        for dead_node in dead_nodes:
            client_socket.sendto(('!' + dead_node).encode(), (user_ip, obj.port))

    client_socket.close()