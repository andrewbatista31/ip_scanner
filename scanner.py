# scanner.py
import ipaddress
from scapy.all import ARP, Ether, srp
import threading
from queue import Queue

class NetworkScanner:
    def __init__(self, network):
        self.network = ipaddress.ip_network(network)
        self.devices = []
        self.lock = threading.Lock()

    def scan_chunk(self, start_ip, end_ip):
        arp = ARP(pdst=f"{start_ip}-{end_ip}")
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        result = srp(packet, timeout=2, verbose=0)[0]
        
        for sent, received in result:
            with self.lock:
                self.devices.append({
                    'ip': received.psrc,
                    'status': 'Active',
                    'hostname': self.get_hostname(received.psrc),
                    'port': 'N/A'
                })

    def get_hostname(self, ip):
        import socket
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def scan_network(self):
        ip_list = list(self.network.hosts())
        chunk_size = 50
        threads = []

        for i in range(0, len(ip_list), chunk_size):
            chunk = ip_list[i:i + chunk_size]
            start_ip = str(chunk[0])
            end_ip = str(chunk[-1])
            t = threading.Thread(target=self.scan_chunk, args=(start_ip, end_ip))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return sorted(self.devices, key=lambda x: ipaddress.ip_address(x['ip']))