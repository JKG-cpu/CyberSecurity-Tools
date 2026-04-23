import argparse
from os.path import join
from dataclasses import asdict

from src import *

class Main:
    def __init__(self) -> None:
        self.fileHandler = FileHandler()
        self.config_settings = self.fileHandler.load_data(join("config", "config.json"))
        self.portScanner = PortScanner()
        self.whoisLookup = WhoisLookup()
        self.dnsLookup = DNSLookup()
        self.serviceBanner = ServiceBanner()
    
    def save(self, obj) -> None:
        data = self.fileHandler.load_data(self.config_settings["output_path"])
        data.append(obj)
        self.fileHandler.save(self.config_settings["output_path"], data)

    def get_open_ports(self, ip: str, full_mode: bool) -> None:
        scan_result = self.portScanner.start_scan(
            host = ip,
            full_mode = full_mode,
            timeout = self.config_settings["timeout"],
            max_workers = self.config_settings["max_workers"],
            selective_ports = None
        )

        open_ports = []

        for port in scan_result:
            match port.state:
                case "open":
                    open_ports.append(port)

        return open_ports

    def ping(self, ip: str) -> None:
        ip_addresses = ping_sweep(
            ip_addr = ip,
            max_workers = self.config_settings["max_workers"]
        )

        print(f"Amount of hosts up on {ip}: {len(ip_addresses)}")

        self.save({
            "ping": {
                "host": ip,
                "hosts_up": ip_addresses
            }
        })

    def scan(self, ip: str, full_mode: bool, selective_ports: list[int] | None = None) -> None:
        scan_result = self.portScanner.start_scan(
            host = ip,
            full_mode = full_mode,
            timeout = self.config_settings["timeout"],
            max_workers = self.config_settings["max_workers"],
            selective_ports = selective_ports
        )
        
        number_of_ports = len(scan_result)
        open_ports = []
        closed_ports = []
        filtered_ports = []

        for port in scan_result:
            match port.state:
                case "open":
                    open_ports.append(port)

                case "filtered":
                    filtered_ports.append(port)

                case "closed":
                    closed_ports.append(port)

        print(f"Number of ports on {ip}: {number_of_ports}")
        print(f"Open Ports: {len(open_ports)}")
        print(f"Filtered Ports: {len(filtered_ports)}")
        print(f"Closed Ports: {len(closed_ports)}")
        print(f"Look at the config path for more details...")

        self.save({
            "Scan": {
                "host": ip,
                "open_ports": [asdict(port) for port in open_ports],
                "filtered_ports": [asdict(port) for port in filtered_ports],
                "closed_ports": [asdict(port) for port in closed_ports],
                "ports_scanned": number_of_ports
            }
        })

    def whois(self, domain: str) -> None:
        info = self.whoisLookup.lookup(domain)
        dns = self.dnsLookup.lookup(domain)

        print("Scan complete, look in output folder")

        self.save({
            "Whois": {
                "domain": domain,
                "info": info,
                "dns": dns
            }
        })

    def grab_banners(self, ip: str, full_mode: bool, ports: list[int] | None) -> None:
        banners = self.serviceBanner.grab_banners(
            ip, 
            ports if ports else self.get_open_ports(ip, full_mode), 
            self.config_settings["timeout"], 
            self.config_settings["max_workers"]
        )
 
        if banners:
            print(f"Service banners given. Check output file ({self.config_settings["output_path"]})")
            self.save({
                "Service Banners": {
                    "ip": ip,
                    "banners recieved": banners
                }
            })

        else:
            print("No service banners given")

if __name__ == "__main__":
    m = Main()

    parser = argparse.ArgumentParser("NetWatch")

    config = parser.add_argument_group("Config")

    config.add_argument("--ports", type = str, help = "Specify ports to scan. Seperate port numbers with commas")
    config.add_argument("--full", action = "store_true", help = "Scan the full host.")

    ping = parser.add_argument_group("Ping")
    ping.add_argument("-ping", type = str, help = "Ping an ip address(es).")

    scanning = parser.add_argument_group("Scanning")
    scanning.add_argument("-scan", type = str, help = "Scan an ip address. Use --full for a full scan")

    whois = parser.add_argument_group("Whois")
    whois.add_argument("-whois", type = str, help = "Get whois info from a domain or ip")

    banner = parser.add_argument_group("Banner")
    banner.add_argument("-banner", type = str, help = "Get banners from a specific ip address")

    web = parser.add_argument_group("Website")
    web.add_argument("-web", action = "store_true", help = "Launch the web browser version of this!")

    args = parser.parse_args()
    
    if args.scan:
        m.scan(
            ip = args.scan,
            full_mode = args.full,
            selective_ports = [
                int(port) for port in args.ports.split(",")
            ] if args.ports else None
        )

    elif args.ping:
        m.ping(
            ip = args.ping
        )

    elif args.whois:
        m.whois(
            domain = args.whois
        )

    elif args.banner:
        m.grab_banners(
            ip = args.banner,
            full_mode = args.full,
            ports = [
                int(port) for port in args.ports.split(",")
            ] if args.ports else None
        )

    else:
        parser.print_help()