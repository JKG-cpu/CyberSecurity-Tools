import subprocess
import ipaddress

def start_ping(ip_addr: str, timeout: int = 5) -> bool:
    process = subprocess.run(
        ["ping", "-c", "1", "-w", str(timeout), ip_addr],
        capture_output = True
    )

    return process.returncode == 0

def ping_sweep(ip_addr: str) -> None:
    hosts = ipaddress.ip_network(ip_addr).hosts()
    print(hosts)

if __name__ == "__main__":
    ping_sweep("192.168.1.0/24")