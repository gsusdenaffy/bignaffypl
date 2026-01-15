import socket
import time
import threading
import struct
import sys

class LocalNetworkSpeedTest:
    def __init__(self, port=5555):
        self.port = port
        self.results = {}
    
    def start_server(self):
        """Start a speed test server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(1)
        
        print(f"Speed test server listening on port {self.port}")
        print("Waiting for client to connect...")
        
        client_socket, client_address = server.accept()
        print(f"Client connected from {client_address}")
        
        # Receive test
        start_time = time.time()
        total_received = 0
        
        # Receive 10MB of data
        target_size = 10 * 1024 * 1024  # 10MB
        data = b'0' * 1024  # 1KB chunk
        
        while total_received < target_size:
            received = client_socket.recv(1024)
            if not received:
                break
            total_received += len(received)
        
        end_time = time.time()
        
        # Calculate speed
        duration = end_time - start_time
        speed_mbps = (total_received * 8) / (duration * 1_000_000)
        
        print(f"\nLocal Network Speed Test Results:")
        print(f"  Data transferred: {total_received / 1_000_000:.2f} MB")
        print(f"  Time: {duration:.2f} seconds")
        print(f"  Speed: {speed_mbps:.2f} Mbps")
        print(f"  From: {client_address[0]}")
        
        client_socket.close()
        server.close()
        
        return speed_mbps
    
    def start_client(self, server_ip):
        """Connect to speed test server"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client.connect((server_ip, self.port))
            print(f"Connected to server at {server_ip}:{self.port}")
            
            # Send test data
            data = b'X' * 1024  # 1KB chunk
            total_sent = 0
            target_size = 10 * 1024 * 1024  # 10MB
            
            start_time = time.time()
            
            while total_sent < target_size:
                sent = client.send(data)
                if sent == 0:
                    break
                total_sent += sent
            
            end_time = time.time()
            
            duration = end_time - start_time
            speed_mbps = (total_sent * 8) / (duration * 1_000_000)
            
            print(f"\nSpeed test complete:")
            print(f"  Data sent: {total_sent / 1_000_000:.2f} MB")
            print(f"  Time: {duration:.2f} seconds")
            print(f"  Speed: {speed_mbps:.2f} Mbps")
            print(f"  To: {server_ip}")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()
        
        return speed_mbps

def main_menu():
    print("=" * 60)
    print("LOCAL NETWORK SPEED TEST")
    print("=" * 60)
    print("\n1. Run internet speed test (requires internet)")
    print("2. Monitor real-time bandwidth usage")
    print("3. Test speed between local devices")
    print("4. Check device latencies")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ")
    return choice

if __name__ == "__main__":
    print("Network Speed Tools")
    print("=" * 50)
    
    # Check requirements
    print("Checking requirements...")
    
    required_packages = ['speedtest-cli', 'psutil']
    
    for package in required_packages:
        try:
            if package == 'speedtest-cli':
                import speedtest
            elif package == 'psutil':
                import psutil
        except ImportError:
            install = input(f"\n{package} is not installed. Install now? (y/n): ")
            if install.lower() == 'y':
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} installed successfully!")
    
    print("\n" + "=" * 50)
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            # Run the first script
            exec(open(__file__).read())
        elif choice == '2':
            # Run real-time monitor
            monitor = RealTimeBandwidthMonitor()
            monitor.monitor()
        elif choice == '3':
            print("\nLocal device speed test")
            print("1. Start as SERVER (wait for connection)")
            print("2. Start as CLIENT (connect to server)")
            sub_choice = input("\nSelect: ")
            
            tester = LocalNetworkSpeedTest()
            
            if sub_choice == '1':
                tester.start_server()
            elif sub_choice == '2':
                server_ip = input("Enter server IP address: ")
                tester.start_client(server_ip)
        elif choice == '4':
            # Get local IP range
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            network_prefix = '.'.join(local_ip.split('.')[:3])
            
            print(f"\nTesting latency in network {network_prefix}.0/24")
            
            # Test common IPs
            common_ips = [f"{network_prefix}.{i}" for i in [1, 254, 100, 101, 102]]
            
            for ip in common_ips:
                print(f"\nTesting {ip}...")
                os.system(f"ping -n 2 {ip}" if os.name == 'nt' else f"ping -c 2 {ip}")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")
