import sys
from scanner import NetworkScanner
from display import Display

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <network_address>")
        print("Example: python main.py 192.168.1.0/24")
        sys.exit(1)

    network = sys.argv[1]
    scanner = NetworkScanner(network)
    display = Display()
    
    print(f"Scanning network: {network}")
    devices = scanner.scan_network()
    display.show_results(devices)

if __name__ == "__main__":
    main()