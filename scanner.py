# scanner.py
import ipaddress
import socket
import threading
from queue import Queue
import os

class NetworkScanner:
    def __init__(self, network):
        self.network = ipaddress.ip_network(network)
        self.devices = []
        self.queue = Queue()
        self.lock = threading.Lock()
        self.ports = [22, 80, 443, 3389]  # SSH, HTTP, HTTPS, RDP

    def check_host(self, ip):
        ip_str = str(ip)
        for port in self.ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip_str, port))
                if result == 0:
                    with self.lock:
                        self.devices.append({
                            'ip': ip_str,
                            'status': 'Active',
                            'hostname': self.get_hostname(ip_str),
                            'port': port
                        })
                    sock.close()
                    return
                sock.close()
            except Exception:
                pass
        
        if self.ping_host(ip_str):
            with self.lock:
                self.devices.append({
                    'ip': ip_str,
                    'status': 'Active (ping)',
                    'hostname': self.get_hostname(ip_str),
                    'port': 'N/A'
                })

    def ping_host(self, ip):
        param = '-n' if os.name == 'nt' else '-c'
        command = f"ping {param} 1 -w 100 {ip} >nul 2>&1"  # Windows: suppress output
        return os.system(command) == 0

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def thread_worker(self):
        while True:
            try:
                ip = self.queue.get_nowait()
                self.check_host(ip)
                self.queue.task_done()
            except:
                break

    def scan_network(self):
        for ip in self.network.hosts():
            self.queue.put(ip)

        thread_count = min(50, self.network.num_addresses)
        threads = []
        
        for _ in range(thread_count):
            t = threading.Thread(target=self.thread_worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return sorted(self.devices, key=lambda x: ipaddress.ip_address(x['ip']))