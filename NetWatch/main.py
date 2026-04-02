import argparse
import json
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
    
    def ping(self, ip: str) -> None:
        ip_addresses = ping_sweep(
            ip_addr = ip,
            max_workers = self.config_settings["max_workers"]
        )

        print(f"Amount of hosts up on {ip}: {len(ip_addresses)}")

        data = self.fileHandler.load_data(self.config_settings["output_path"])
        data.append({
            "ping": {
                "host": ip,
                "hosts_up": ip_addresses
            }
        })
        self.fileHandler.save(self.config_settings["output_path"], data)

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

        data = self.fileHandler.load_data(self.config_settings["output_path"])
        data.append({
            "Scan": {
                "host": ip,
                "open_ports": [asdict(port) for port in open_ports],
                "filtered_ports": [asdict(port) for port in filtered_ports],
                "closed_ports": [asdict(port) for port in closed_ports],
                "ports_scanned": number_of_ports
            }
        })
        self.fileHandler.save(self.config_settings["output_path"], data)

    def whois(self, domain: str) -> None:
        info = self.whoisLookup.lookup(domain)
        dns = self.dnsLookup.lookup(domain)

        print("Scan complete, look in output folder")

        data = self.fileHandler.load_data(self.config_settings["output_path"])
        data.append({
            "Whois": {
                "domain": domain,
                "info": info,
                "dns": dns
            }
        })
        self.fileHandler.save(self.config_settings["output_path"], data)

if __name__ == "__main__":
    m = Main()

    parser = argparse.ArgumentParser("NetWatch")

    config = parser.add_argument_group("Config", "Set your config settings.")

    ping = parser.add_argument_group("Ping")
    ping.add_argument("-ping", type = str, help = "Ping an ip address(es).")

    scanning = parser.add_argument_group("Scanning")
    scanning.add_argument("-scan", type = str, help = "Scan an ip address. Use --full for a full scan")
    scanning.add_argument("-ports", type = str, help = "Scan specific ports on the target ip address. Seperate port numbers with commas")
    scanning.add_argument("--full", action = "store_true", help = "Scan the full host.")

    whois = parser.add_argument_group("Whois")
    whois.add_argument("-whois", type = str, help = "Get whois info from a domain or ip")

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
        m.whois(args.whois)

    else:
        parser.print_help()