import asyncio
from socket import gethostbyname
import subprocess

class Scanner:
    def __init__(self, remote_host: str, start_port: int = 1, end_port: int = 1024) -> None:
        self.target_ip = remote_host
        self.start_port, self.end_port = start_port, end_port

    async def _scan_port(self, port: int, semaphore: asyncio.Semaphore):
        async with semaphore:
            try:
                _, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.target_ip, port),
                    timeout=1
                )
                print(f"Port {port} is open")
                writer.close()
                await writer.wait_closed()
                return port
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                pass

    async def start_scan(self, max_concurrent: int = 500) -> list[int]:
        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = [self._scan_port(port, semaphore) 
                 for port in range(self.start_port, self.end_port + 1)]
        ports = await asyncio.gather(*tasks)
        return [port for port in ports if port is not None]

class NmapScanner:
    def __init__(self, remote_host: str, start_port: int = 1, end_port: int = 1024):
        self.target_ip = gethostbyname(remote_host)
        self.scanner = Scanner(self.target_ip, start_port, end_port)
    
    def run_nmap_scan(self) -> str:
        open_ports = asyncio.run(self.scanner.start_scan())

        if not open_ports:
            return "All ports are closed or filtered."

        port_string = ",".join(str(p) for p in open_ports)
        result = subprocess.run(
            ["nmap", "-sV", "-T4", "--open", "-p", port_string, self.target_ip],
            capture_output = True,
            text = True
        )
        return result.stdout
