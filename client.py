import socket          # Connect to your server
import threading       # Run multiple tasks simultaneously
import time            # Manage delays and timeouts
import platform        # Identify the operating system
import json            # Send and receive structured messages
import logging         # Record errors and activity
import uuid            # Generate unique client IDs

from datetime import datetime
from colorama import Fore, Style

# CLIENT-SERVER COMMUNICATION 

import socket
import json
from colorama import Fore, Style

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5555
BUFFER_SIZE = 4096


def connect_to_server():
    try:
        client = socket.create_connection(
            (SERVER_HOST, SERVER_PORT),
            timeout=10
        )

        print(Fore.GREEN + "[CONNECTED] Server connection established")
        return client

    except OSError as error:
        print(Fore.RED + f"[CONNECTION ERROR] {error}")
        return None


def send_message(client, message):
    try:
        payload = {
            "type": "message",
            "content": message
        }

        data = json.dumps(payload) + "\n"
        client.sendall(data.encode("utf-8"))

        print(Fore.GREEN + "[MESSAGE SENT]")
        return True

    except OSError as error:
        print(Fore.RED + f"[SEND ERROR] {error}")
        return False


def receive_message(client):
    try:
        data = client.recv(BUFFER_SIZE)

        if not data:
            print(Fore.YELLOW + "[SERVER DISCONNECTED]")
            return None

        message = data.decode("utf-8", errors="replace")

        print(Fore.CYAN + f"[SERVER RESPONSE] {message}")
        return message

    except OSError as error:
        print(Fore.RED + f"[RECEIVE ERROR] {error}")
        return None


def start_client():
    client = connect_to_server()

    if client is None:
        return

    try:
        while True:
            message = input("CLIENT > ")

            if message.lower() == "exit":
                break

            if not send_message(client, message):
                break

    except KeyboardInterrupt:
        print("\n[CLIENT STOPPED]")

    finally:
        client.close()
        print(Style.RESET_ALL + "[DISCONNECTED]")


if __name__ == "__main__":
    start_client()

# ━━━━━━━━━ TERMINAL COMMAND HANDLER ━━━━━━━━━

import platform
import time

def execute_command(command):
    command = command.strip().lower()

    if command == "help":
        return (
            "AVAILABLE COMMANDS:\n"
            "  help    - Show available commands\n"
            "  status  - Check client status\n"
            "  system  - Display operating system\n"
            "  ping    - Test communication\n"
            "  uptime  - Show client uptime\n"
            "  exit    - Disconnect client"
        )

    elif command == "status":
        return "[ONLINE] Client is running"

    elif command == "system":
        return f"[SYSTEM] {platform.system()} {platform.release()}"

    elif command == "ping":
        return "PONG"

    elif command == "uptime":
        return f"[UPTIME] {time.monotonic():.0f} seconds since system clock origin"

    elif command == "exit":
        return "[DISCONNECT] Client closing connection"

    else:
        return f"[ERROR] Unknown command: {command}"