# display.py
from tabulate import tabulate

class Display:
    def show_results(self, devices):
        if not devices:
            print("\nNo devices found on the network.")
            return

        print(f"\nFound {len(devices)} active devices:")
        
        table_data = []
        for device in devices:
            table_data.append([
                device['ip'],
                device['status'],
                device['hostname'],
                device['port']
            ])

        headers = ['IP Address', 'Status', 'Hostname', 'Open Port']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))