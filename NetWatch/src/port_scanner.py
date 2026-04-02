import socket
from nmap import PortScanner as NmapScanner
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

@dataclass(frozen = True)
class PortResult:
    port: int
    state: str
    service: str
    protocol: str

class PortScanner:
    def _check_port(self, host: str, port: int, timeout: int) -> PortResult:
        addr = (socket.gethostbyname(host), port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect(addr)
            state = "open"
        except socket.timeout:
            state = "filtered"
        except Exception:
            state = "closed"
        finally:
            s.close()

        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "unknown"

        return PortResult(port=port, state=state, service=service, protocol="tcp")

    def _nmap_scan_range(self, host: str, port_range: tuple[int, int], timeout: int) -> list[PortResult]:
        nm = NmapScanner()
        start, end = port_range
        nm.scan(
            host,
            f"{start}-{end}",
            arguments=f"--host-timeout {timeout}s -sV"
        )

        results = []
        host_ip = socket.gethostbyname(host)

        if host_ip not in nm.all_hosts():
            return results

        for proto in nm[host_ip].all_protocols():
            for port, data in nm[host_ip][proto].items():
                results.append(PortResult(
                    port=port,
                    state=data["state"],
                    service=data.get("name", "unknown"),
                    protocol=proto,
                ))
        return results

    def scan_selective(self, host: str, ports: list[int], timeout: int, max_workers: int = 100) -> list[PortResult]:
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._check_port, host, p, timeout): p for p in ports}
            for future in as_completed(futures):
                results.append(future.result())
        return sorted(results, key=lambda r: r.port)

    def scan_range(self, host: str, port_range: tuple[int, int], timeout: int) -> list[PortResult]:
        return sorted(self._nmap_scan_range(host, port_range, timeout), key=lambda r: r.port)

    def start_scan(
        self,
        host: str,
        full_mode: bool = False,
        timeout: int = 5,
        max_workers: int = 100,
        selective_ports: list[int] | None = None,
    ) -> list[PortResult]:

        if full_mode:
            return self.scan_range(host, (1, 65535), timeout)

        elif selective_ports:
            return self.scan_selective(host, selective_ports, timeout, max_workers)

        else:
            return self.scan_range(host, (1, 1024), timeout)