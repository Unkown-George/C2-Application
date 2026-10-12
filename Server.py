
import socket
import threading #multithreading 
import os #local os functions
from colorama import Fore, Style #colorama for colored text
import ctypes #communicate with windows api
from datetime import datetime #get current time

client = {}

def logo():
    red = Fore.RED + Style.BRIGHT
    dark = Fore.BLACK + Style.BRIGHT
    reset = Style.RESET_ALL

    print(red + r"""
   ╔══════════════════════════════════════════════╗
   ║  [!]  W T // 0xDEAD  //  ACCESS RESTRICTED    ║
   ╚══════════════════════════════════════════════╝

   ██╗    ██╗██╗  ██╗██╗████████╗███████╗
   ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝
   ██║ █╗ ██║███████║██║   ██║   █████╗
   ██║███╗██║██╔══██║██║   ██║   ██╔══╝
   ╚███╔███╔╝██║  ██║██║   ██║   ███████╗
    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

   ████████╗██████╗  █████╗ ███████╗██╗  ██╗
   ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║  ██║
      ██║   ██████╔╝███████║███████╗███████║
      ██║   ██╔══██╗██╔══██║╚════██║██╔══██║
      ██║   ██║  ██║██║  ██║███████║██║  ██║
      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
""" + reset)

    print(dark + "   ──[ SYSTEM // UNKNOWN ENTITY ]──────────────" + reset)
    print(red + "   > IDENTITY  : W.T_0x01")
    print(red + "   > PROTOCOL  : ENCRYPTED")
    print(red + "   > STATUS    : ONLINE")
    print(dark + "   ─────────────────────────────────────────────" + reset)

logo()

# ━━━━━━━━━ ADVANCED CLIENT MANAGEMENT ━━━━━━━━━

clients = {}
clients_lock = threading.RLock()


def handle_client(client_socket, addr):
    client_id = f"{addr[0]}:{addr[1]}"
    start_time = datetime.now()
    bytes_received = 0
    packets_received = 0

    # Colored logging with timestamps
    def log(status, message, color=Fore.RED):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(
            f"{color}[{timestamp}] [{status}] "
            f"{message}{Fore.RESET}",
            flush=True
        )

    # Register new connection
    with clients_lock:
        clients[addr] = client_socket
        active = len(clients)

    log("CONNECTED", client_id, Fore.GREEN)
    log("CLIENT COUNT", f"{active} active")

    try:
        client_socket.settimeout(120)

        while True:
            try:
                data = client_socket.recv(4096)

                # Detect graceful disconnection
                if not data:
                    log("CONNECTION CLOSED", client_id)
                    break

                bytes_received += len(data)
                packets_received += 1

                message = data.decode(
                    "utf-8",
                    errors="replace"
                )

                log(
                    "MESSAGE",
                    f"{client_id} | {message}",
                    Fore.WHITE
                )

            except socket.timeout:
                log("TIMEOUT", client_id, Fore.YELLOW)
                break

            except ConnectionResetError:
                log("CONNECTION RESET", client_id)
                break

            except BrokenPipeError:
                log("BROKEN PIPE", client_id)
                break

            except OSError as error:
                log("NETWORK ERROR", str(error))
                break

    except Exception as error:
        log("UNEXPECTED ERROR", str(error))

    finally:
        # Always clean up the client
        with clients_lock:
            clients.pop(addr, None)
            active = len(clients)

        try:
            client_socket.close()
        except OSError:
            pass

        duration = (
            datetime.now() - start_time
        ).total_seconds()

        log("DISCONNECTED", client_id)
        log("SESSION TIME", f"{duration:.2f} seconds")
        log("DATA RECEIVED", f"{bytes_received} bytes")
        log("RECEIVE CALLS", str(packets_received))
        log("ACTIVE CLIENTS", str(active))

# ━━━━━━━━━ ACCEPTING NEW CLIENTS ━━━━━━━━━

MAX_CLIENTS = 25
BACKLOG = 50

# Limits the number of active client handlers
client_slots = threading.BoundedSemaphore(MAX_CLIENTS)


def accept_clients(server):
    print(Fore.RED + "[SYSTEM] Waiting for incoming connections..."
          + Style.RESET_ALL)

    while True:
        client_socket = None
        slot_acquired = False

        try:
            # Reserve capacity before accepting
            client_slots.acquire()
            slot_acquired = True

            client_socket, addr = server.accept()

            client_id = f"{addr[0]}:{addr[1]}"

            print(
                Fore.GREEN +
                f"[+] CONNECTION ACCEPTED | {client_id}" +
                Style.RESET_ALL
            )

            # Run each client in a separate thread
            def client_worker(sock, address):
                try:
                    handle_client(sock, address)
                finally:
                    client_slots.release()

            client_thread = threading.Thread(
                target=client_worker,
                args=(client_socket, addr),
                daemon=True,
                name=f"Client-{client_id}"
            )

            client_thread.start()

            # Worker now owns the socket and capacity slot
            client_socket = None
            slot_acquired = False

        except (OSError, RuntimeError) as error:
            print(
                Fore.RED +
                f"[ACCEPT ERROR] {error}" +
                Style.RESET_ALL
            )
            break

        finally:
            if client_socket is not None:
                client_socket.close()

            if slot_acquired:
                client_slots.release()


# ━━━━━━━━━ SERVER INITIALIZATION ━━━━━━━━━

def start_server(host="127.0.0.1", port=5555):

    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as server:

            # Allow quick restart after shutdown
            server.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            # Assign server address
            server.bind((host, port))

            # Start listening
            server.listen(BACKLOG)

            print(Fore.RED + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(Fore.GREEN + "[+] SERVER INITIALIZED")
            print(Fore.WHITE + f"[HOST] {host}")
            print(Fore.WHITE + f"[PORT] {port}")
            print(Fore.WHITE + f"[MAX CLIENTS] {MAX_CLIENTS}")
            print(Fore.GREEN + "[STATUS] ONLINE")
            print(Fore.RED + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(Style.RESET_ALL)

            # Accept incoming clients
            accept_clients(server)

    except KeyboardInterrupt:
        print(
            Fore.YELLOW +
            "\n[!] SERVER SHUTDOWN REQUESTED" +
            Style.RESET_ALL
        )

    except OSError as error:
        print(
            Fore.RED +
            f"[SERVER ERROR] {error}" +
            Style.RESET_ALL
        )

    finally:
        print(
            Fore.RED +
            "[SYSTEM] Server listener stopped." +
            Style.RESET_ALL
        )


if __name__ == "__main__":
    start_server()
    
# ━━━━━━━━━ SENDING COMMANDS TO CLIENTS ━━━━━━━━━

import json

ALLOWED_COMMANDS = {"PING", "STATUS", "DISCONNECT"}

def send_command(client_id, command):
    command = command.upper()

    if command not in ALLOWED_COMMANDS:
        print(Fore.RED + f"[BLOCKED] Unknown command: {command}")
        return False

    # Find the requested client
    with clients_lock:
        client_socket = clients.get(client_id)

    if client_socket is None:
        print(Fore.RED + "[ERROR] Client not connected")
        return False

    # Create a structured command
    payload = {
        "type": "command",
        "action": command,
        "timestamp": datetime.now().isoformat()
    }

    try:
        message = json.dumps(payload) + "\n"
        client_socket.sendall(message.encode("utf-8"))

        print(
            Fore.GREEN +
            f"[COMMAND SENT] {client_id} | {command}" +
            Style.RESET_ALL
        )
        return True

    except OSError as error:
        print(Fore.RED + f"[SEND ERROR] {error}")
        return False