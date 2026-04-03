from src import ping_sweep, start_ping, PortScanner, WhoisLookup, DNSLookup, ServiceBanner, get_config

config = get_config()
ps = PortScanner()
wl = WhoisLookup()
dns = DNSLookup()
sb = ServiceBanner()

# Ping
def sweep_host(target: str) -> list[str]:
    hosts = ping_sweep(target, config["max_workers"])
    return hosts

def ping_host(target: str) -> bool:
    return start_ping(target, config["timeout"])

# Scan
def scan_host(
        target: str,
        fast: bool,
        ports: list[int] | None = None
    ):
    scan_results = ps.start_scan(
        host = target,
        full_mode = fast,
        timeout = config["timeout"],
        max_workers = config["max_workers"],
        selective_ports = ports
    )
    return scan_results

# Whois
def whois_info(target: str) -> tuple[dict, dict]:
    info = wl.lookup(target)
    dns_info = dns.lookup(target)
    return (info, dns_info)

# Banner
def banner_info(
    target: str,
    ports: int | list[int]
) -> str | list[str]:
    if isinstance(ports, int):
        return sb.grab_banner(
            ip = target,
            port = ports,
            timeout = config["timeout"]
        )
    else:
        return sb.grab_banners(
            ip = target,
            ports = ports,
            timeout = config["timeout"],
            max_workers = config["max_workers"]
        )
    