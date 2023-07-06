import dns.query
import dns.zone
import argparse

# DNS Zone Transfer
def dns_zone_transfer(target_domain, nameserver):
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(nameserver, target_domain))
        return zone.nodes.keys()
    except dns.exception.FormError:
        pass
    except dns.exception.Timeout:
        pass
    return []

def main():
    parser = argparse.ArgumentParser(description="DNS Zone Transfer Tool")
    parser.add_argument("target_domain", help="Target domain for DNS zone transfer")
    parser.add_argument("nameserver", help="Nameserver to perform zone transfer")
    args = parser.parse_args()

    transferred_zones = dns_zone_transfer(args.target_domain, args.nameserver)

    if transferred_zones:
        print("Transferred Zones:")
        for zone in transferred_zones:
            print(zone)
    else:
        print("No transferred zones found.")

if __name__ == "__main__":
    main()
