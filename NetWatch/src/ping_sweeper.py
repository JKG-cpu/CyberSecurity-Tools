import subprocess
import ipaddress
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

def start_ping(ip_addr: str, timeout: int = 5) -> bool:
    system = platform.system()
    args = ["ping"]

    if system == "Windows":
        args += ["-n", "1", "-w", str(timeout * 1000), ip_addr]
    elif system == "Darwin":
        args += ["-c", "1", "-W", str(timeout * 1000), ip_addr]
    else:
        args += ["-c", "1", "-w", str(timeout), ip_addr]

    process = subprocess.run(
        args,
        capture_output = True
    )

    return process.returncode == 0

def ping_sweep(ip_addr: str, max_workers: int = 100) -> list[str]:
    hosts = ipaddress.ip_network(ip_addr, strict = False)
    results = []

    with ThreadPoolExecutor(max_workers = max_workers) as executor:
        futures = {executor.submit(start_ping, str(host)): str(host) for host in hosts.hosts()}

        for future in as_completed(futures):
            try:
                if future.result():
                    results.append(futures[future])
            
            except Exception as e:
                print(f"Exception: {e}")

    return results

if __name__ == "__main__":
    print(ping_sweep("127.0.0.0/24"))