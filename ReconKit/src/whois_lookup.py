import whois

class WhoisLookup:
    def format(self, domain_info: dict) -> dict:
        return {k: v for k, v in domain_info.items() if v}

    def lookup(self, domain_name: str) -> dict | str:
        try:
            domain_info = whois.whois(domain_name)

            return self.format(domain_info)

        except Exception as e:
            return "Error grabbing WHOIS information."