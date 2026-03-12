import whois

# Specify the domain name you want to look up
domain_name = 'google.com'

try:
    # Perform the WHOIS lookup
    domain_info = whois.whois(domain_name)

    # Print all retrieved information (as a dictionary)
    print(domain_info)

except Exception as e:
    print(f"Error retrieving WHOIS information: {e}")
