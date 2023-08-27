import socket
import ipaddress
import subprocess

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_subnet_mask(ip):
    proc = subprocess.Popen('ipconfig',stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if ip.encode() in line:
            break
    mask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',b'').decode()
    return mask

def calculate_broadcast_address():
    ip_address = get_local_ip()
    subnet_mask = get_subnet_mask(ip_address)
    ip = ipaddress.IPv4Interface(f"{ip_address}/{subnet_mask}")
    return ip.network.network_address + (ip.network.num_addresses - 1)