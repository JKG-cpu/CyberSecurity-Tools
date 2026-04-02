import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

class ServiceBanner:
    def grab_banner(self, ip: str, port: int, timeout: int) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((ip, port))

            s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode("utf-8") + b"\r\n\r\n")
            banner = s.recv(1024).decode().strip()
            return banner

        except socket.timeout:
            return "Timed out"

        finally:
            s.close()
        
    def grab_banners(self, ip: str, ports: list[int], timeout: int, max_workers: int = 100) -> list[tuple[int, str]]:
        banners = []

        with ThreadPoolExecutor(max_workers = max_workers) as executor:
            futures = {executor.submit(self.grab_banner, ip, p, timeout): p for p in ports}
            for future in as_completed(futures):
                p = futures[future]
                result = future.result()
                banners.append((p, result))

        return banners

