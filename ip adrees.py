import json
import webbrowser
from datetime import datetime

class NetworkManager:
    def __init__(self, devices_file="network_devices.json"):
        self.devices = self.load_devices(devices_file)
        
    def load_devices(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def generate_router_config_guide(self):
        """Generate instructions for router configuration"""
        
        print("\n" + "=" * 80)
        print("ROUTER CONFIGURATION INSTRUCTIONS")
        print("=" * 80)
        
        for device in self.devices:
            print(f"\nDevice: {device.get('hostname', 'Unknown')}")
            print(f"  MAC Address: {device.get('mac', 'Unknown')}")
            print(f"  Current IP: {device.get('ip', 'Unknown')}")
            print(f"  Suggested Static IP: {self.suggest_static_ip(device)}")
            print(f"  Steps to configure in router:")
            print(f"    1. Login to router admin panel")
            print(f"    2. Find 'DHCP Reservation' or 'Static DHCP'")
            print(f"    3. Add new entry with MAC above")
            print(f"    4. Assign IP: {self.suggest_static_ip(device)}")
            print(f"    5. Save and reboot if required")
    
    def suggest_static_ip(self, device):
        """Suggest a static IP based on device type"""
        current_ip = device.get('ip', '192.168.1.100')
        base = '.'.join(current_ip.split('.')[:3])
        
        # IP allocation ranges
        device_type = device.get('type', '').lower()
        
        if 'router' in device_type:
            return f"{base}.1"
        elif 'server' in device_type or 'nas' in device_type:
            return f"{base}.10"
        elif 'printer' in device_type:
            return f"{base}.20"
        elif 'camera' in device_type:
            return f"{base}.30"
        elif 'iot' in device_type or 'smart' in device_type:
            return f"{base}.40"
        elif 'phone' in device_type:
            return f"{base}.50"
        elif 'pc' in device_type or 'laptop' in device_type:
            return f"{base}.100"
        else:
            return current_ip  # Keep current IP
    
    def generate_html_report(self):
        """Generate an HTML report of network devices"""
        html = """
        <html>
        <head>
            <title>Network Devices Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                .warning { color: #ff0000; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Network Devices Inventory</h1>
            <p>Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <table>
                <tr>
                    <th>IP Address</th>
                    <th>Hostname</th>
                    <th>MAC Address</th>
                    <th>Vendor</th>
                    <th>Type</th>
                    <th>Suggested Static IP</th>
                </tr>
        """
        
        for device in self.devices:
            html += f"""
                <tr>
                    <td>{device.get('ip', 'N/A')}</td>
                    <td>{device.get('hostname', 'Unknown')}</td>
                    <td>{device.get('mac', 'Unknown')}</td>
                    <td>{device.get('vendor', 'Unknown')}</td>
                    <td>{device.get('type', 'Unknown')}</td>
                    <td>{self.suggest_static_ip(device)}</td>
                </tr>
            """
        
        html += """
            </table>
            <p class="warning">Note: To change IP addresses, configure DHCP reservations in your router.</p>
            <p>Router Access: Usually http://192.168.1.1 or http://192.168.0.1</p>
        </body>
        </html>
        """
        
        with open("network_report.html", "w") as f:
            f.write(html)
        
        webbrowser.open("network_report.html")
        print("[+] HTML report generated: network_report.html")

# Usage
if __name__ == "__main__":
    manager = NetworkManager()
    manager.generate_router_config_guide()
    manager.generate_html_report()