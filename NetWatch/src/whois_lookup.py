import whois
import dns.resolver
from ipwhois import IPWhois
from .helpers import is_ip

class WhoisLookup:
    def _format(self, domain_info: dict) -> dict:
        result = {}
        for k, v in domain_info.items():
            if not v:
                continue
            if isinstance(v, list):
                result[k] = [str(i) for i in v]
            else:
                result[k] = str(v)
        return result

    def lookup(self, domain_name: str) -> dict:
        try:
            if is_ip(domain_name):
                domain_info = IPWhois(domain_name).lookup_rdap()
            
            else:
                domain_info = whois.whois(domain_name)

            return self._format(domain_info)

        except Exception as e:
            return {"Error": str(e)}

class DNSLookup:
    def _query(self, domain: str, record_type: str) -> list:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            return [str(r) for r in answers]
    
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def lookup(self, domain: str) -> dict:
        return {
            "A": self._query(domain, "A"),
            "MX": self._query(domain, "MX"),
            "TXT": self._query(domain, "TXT")
        }