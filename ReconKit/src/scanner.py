import asyncio
import subprocess
from socket import gethostbyname
from datetime import datetime

from .helpers import FileHandler
from .lookups import WhoisLookup, DNSLookup

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
    def __init__(self, remote_host: str, start_port: int = 1, end_port: int = 1024, max_concurrent: int = 500):
        self.host = remote_host
        self.target_ip = gethostbyname(remote_host)
        self.max_concurrent = max_concurrent
        self.scanner = Scanner(self.target_ip, start_port, end_port)

        self.filehandler = FileHandler()
        self.whioslookup = WhoisLookup()
        self.dnslookup = DNSLookup()

    def get_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_details(self, nmap_result: str, open_ports: list[int]) -> dict:
        return {
            "target": self.target_ip,
            "scan_time": self.get_time(),
            "ports": {
                "open_ports": open_ports,
                "nmap_output": nmap_result
            },
            "whois": self.whioslookup.lookup(self.target_ip),
            "dns": self.dnslookup.lookup(self.host)
        }

    def _run_nmap_scan(self) -> tuple[str, list[int]]:
        open_ports = asyncio.run(self.scanner.start_scan(self.max_concurrent))

        if not open_ports:
            return ("All ports are closed or filtered.", open_ports)

        port_string = ",".join(str(p) for p in open_ports)
        result = subprocess.run(
            [
                "nmap",
                "-sV",
                "--version-intensity", "2",
                "-T4",
                "--open",
                "-p", port_string,
                "--host-timeout", "30s",
                "--script-timeout", "10s",
                self.target_ip
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        return (result.stdout, open_ports)

    def start_scan(self):
        nmap_result, open_ports = self._run_nmap_scan()

        data = self.get_details(nmap_result, open_ports)

        self.filehandler.save_data(data)

