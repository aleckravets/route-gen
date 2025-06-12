import socket
import ipaddress

DOMAINS = [
    "figma.com",
    "api.figma.com",
    "cdn.figma.com",
    "fonts.gstatic.com"
]

GATEWAY = "0.0.0.0"
SUBNET_MASK_BITS = 24
OUTPUT_FILE = "add-routes.bat"

def resolve_domain(domain):
    try:
        return list({res[4][0] for res in socket.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP) if '.' in res[4][0]})
    except socket.gaierror:
        return []

def ip_to_subnet(ip_str, mask_bits):
    return ipaddress.IPv4Network(f"{ip_str}/{mask_bits}", strict=False)

def main():
    all_ips = set()

    for domain in DOMAINS:
        ips = resolve_domain(domain)
        print(f"{domain}:")
        for ip in ips:
            print(f"  {ip}")
        all_ips.update(ips)

    subnets = set()
    for ip in all_ips:
        try:
            subnet = ip_to_subnet(ip, SUBNET_MASK_BITS)
            subnets.add(subnet)
        except ValueError:
            continue

    print("\nGenerated routes:")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for subnet in sorted(subnets, key=lambda net: str(net.network_address)):
            net_ip = subnet.network_address
            net_mask = subnet.netmask
            line = f"route add {net_ip} mask {net_mask} {GATEWAY}"
            print(line)
            f.write(line + "\n")

if __name__ == "__main__":
    main()
