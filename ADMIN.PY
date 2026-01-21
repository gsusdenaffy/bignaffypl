import requests
from bs4 import BeautifulSoup
import base64
import hashlib

class RouterController:
    def __init__(self, router_ip, username, password):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def login_to_router(self):
        """Login to router admin panel (generic method)"""
        try:
            # Try common login endpoints
            login_endpoints = [
                f"http://{self.router_ip}/login.cgi",
                f"http://{self.router_ip}/admin/login.asp",
                f"http://{self.router_ip}/",
                f"http://{self.router_ip}/login.html"
            ]
            
            for endpoint in login_endpoints:
                try:
                    # Get login page to find form
                    response = self.session.get(endpoint, timeout=5)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for login form
                        login_form = soup.find('form', {'method': 'post'})
                        if login_form:
                            # Extract form data
                            form_data = {}
                            for input_tag in login_form.find_all('input'):
                                name = input_tag.get('name')
                                value = input_tag.get('value', '')
                                if name:
                                    if 'user' in name.lower() or 'login' in name.lower():
                                        form_data[name] = self.username
                                    elif 'pass' in name.lower():
                                        form_data[name] = self.password
                                    else:
                                        form_data[name] = value
                            
                            # Submit login
                            action = login_form.get('action', endpoint)
                            if not action.startswith('http'):
                                action = f"http://{self.router_ip}/{action.lstrip('/')}"
                            
                            login_response = self.session.post(action, data=form_data, timeout=5)
                            
                            if login_response.status_code == 200:
                                print(f"[+] Successfully logged into router at {self.router_ip}")
                                return True
                except:
                    continue
            
            print("[-] Could not login to router. Check credentials and router IP.")
            return False
            
        except Exception as e:
            print(f"[-] Login error: {e}")
            return False
    
    def get_connected_devices(self):
        """Get list of connected devices from router"""
        try:
            # Common endpoints for device lists
            device_endpoints = [
                f"http://{self.router_ip}/dhcpclients.htm",
                f"http://{self.router_ip}/connected_devices.asp",
                f"http://{self.router_ip}/lan_dhcp.html",
                f"http://{self.router_ip}/cgi-bin/lanDHCP.cgi"
            ]
            
            for endpoint in device_endpoints:
                try:
                    response = self.session.get(endpoint, timeout=5)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for device table
                        devices = []
                        tables = soup.find_all('table')
                        
                        for table in tables:
                            rows = table.find_all('tr')
                            for row in rows[1:]:  # Skip header
                                cols = row.find_all('td')
                                if len(cols) >= 3:
                                    device_info = {
                                        'ip': cols[0].text.strip(),
                                        'mac': cols[1].text.strip(),
                                        'hostname': cols[2].text.strip() if len(cols) > 2 else 'Unknown',
                                        'status': 'Connected'
                                    }
                                    devices.append(device_info)
                        
                        if devices:
                            return devices
                except:
                    continue
            
            print("[-] Could not retrieve device list from router")
            return []
            
        except Exception as e:
            print(f"[-] Error getting devices: {e}")
            return []
    
    def reboot_router(self):
        """Reboot the router"""
        print("[!] This will reboot your router!")
        confirm = input("Are you sure? (yes/no): ")
        
        if confirm.lower() == 'yes':
            try:
                reboot_endpoints = [
                    f"http://{self.router_ip}/rebootinfo.cgi",
                    f"http://{self.router_ip}/reboot.cgi",
                    f"http://{self.router_ip}/apply.cgi"
                ]
                
                for endpoint in reboot_endpoints:
                    try:
                        response = self.session.get(endpoint, timeout=10)
                        if response.status_code == 200:
                            print("[+] Router reboot initiated")
                            return True
                    except:
                        continue
                
                print("[-] Could not reboot router")
                return False
                
            except Exception as e:
                print(f"[-] Reboot error: {e}")
                return False
        else:
            print("[-] Reboot cancelled")
            return False

# Example usage for specific router brands
def detect_router_type(ip):
    """Try to detect router type/brand"""
    common_routers = {
        '192.168.0.1': 'TP-Link/Default',
        '192.168.1.1': 'Linksys/Default',
        '192.168.1.254': 'AT&T',
        '192.168.1.10': 'Xfinity',
        '192.168.1.100': 'Netgear',
        '10.0.0.1': 'Xfinity/Comcast',
        '10.0.1.1': 'Apple'
    }
    
    return common_routers.get(ip, 'Unknown')

# Quick network info script
def get_network_info():
    """Get basic network information"""
    import netifaces
    
    print("\n[+] Network Interfaces:")
    print("-" * 50)
    
    for interface in netifaces.interfaces():
        try:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                ip_info = addrs[netifaces.AF_INET][0]
                print(f"Interface: {interface}")
                print(f"  IP: {ip_info['addr']}")
                print(f"  Netmask: {ip_info['netmask']}")
                
                # Get gateway
                if netifaces.AF_INET in netifaces.gateways().get('default', {}):
                    gateway = netifaces.gateways()['default'][netifaces.AF_INET]
                    print(f"  Gateway: {gateway[0]}")
                print("-" * 30)
        except:
            pass

if __name__ == "__main__":
    print("="*60)
    print("ROUTER MANAGEMENT TOOL")
    print("="*60)
    print("\nIMPORTANT LEGAL NOTICE:")
    print("-" * 60)
    print("1. ONLY use on networks YOU OWN or have PERMISSION to manage")
    print("2. Unauthorized access to networks is ILLEGAL")
    print("3. This tool is for EDUCATIONAL purposes only")
    print("4. Always get explicit permission before scanning/controlling")
    print("="*60)
    
    # Get router details
    router_ip = input("\nEnter router IP (default: 192.168.1.1): ") or "192.168.1.1"
    username = input("Enter admin username (default: admin): ") or "admin"
    password = input("Enter admin password: ")
    
    if not password:
        print("[-] Password required")
        exit(1)
    
    router_type = detect_router_type(router_ip)
    print(f"\n[+] Detected router type: {router_type}")
    
    # Try to connect
    controller = RouterController(router_ip, username, password)
    
    if controller.login_to_router():
        print("\n[+] Router Control Options:")
        print("1. List connected devices")
        print("2. Reboot router")
        print("3. Get router info")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            devices = controller.get_connected_devices()
            if devices:
                print("\nConnected Devices:")
                print("-" * 60)
                for device in devices:
                    print(f"IP: {device['ip']}")
                    print(f"MAC: {device['mac']}")
                    print(f"Hostname: {device['hostname']}")
                    print(f"Status: {device['status']}")
                    print("-" * 30)
        elif choice == '2':
            controller.reboot_router()
        elif choice == '3':
            get_network_info()
    else:
        print("\n[!] Could not access router. Trying alternative methods...")
        
        # Use the first script for network scanning
        print("\n[+] Using network scanner instead...")
        from scapy_network_controller import NetworkController
        nc = NetworkController()
        devices = nc.scan_network()
        nc.display_devices(devices)