# IP Scanner

A Python-based tool to scan a local network and discover active devices. It uses port scanning (ports 22, 80, 443, 3389) and ICMP ping to detect devices, displaying their IP addresses, status, hostnames, and open ports (if any).

## Features
- Scans a specified IP range (e.g., `192.168.3.0/24`)
- Multi-threaded scanning for faster results
- Detects devices via common ports and ping
- Displays results in a formatted table

## Requirements
- Python 3.x
- `tabulate` library (`pip install tabulate`)
- Windows, Linux, or macOS
- Administrative privileges (recommended for best results)

## Installation
1. Clone or download this repository:
   ```bash
   git clone https://github.com/andrewbatista31/ip-scanner.git
   cd ip-scanner 
