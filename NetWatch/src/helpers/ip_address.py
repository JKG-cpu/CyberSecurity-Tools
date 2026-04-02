import ipaddress

def is_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True

    except:
        return False