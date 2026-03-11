import asyncio

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
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                pass

    async def start_scan(self, max_concurrent: int = 500):
        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = [self._scan_port(port, semaphore) 
                 for port in range(self.start_port, self.end_port + 1)]
        await asyncio.gather(*tasks)