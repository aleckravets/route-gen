import socket
import ipaddress

DOMAINS = [
    "figma.com",
    "api.figma.com",
    "cdn.figma.com",
    "fonts.gstatic.com"
]

GATEWAY = "0.0.0.0"

OUTPUT_FILE = "add_routes.bat"

def resolve_domain(domain):
    try:
        addresses = socket.getaddrinfo(domain, None)
        ip_list = {result[4][0] for result in addresses}
        return list(ip_list)
    except socket.gaierror:
        print(f"failed to resolve domain {domain}")
        return []

def generate_routes(ip_list):
    commands = []
    for ip in ip_list:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if isinstance(ip_obj, ipaddress.IPv4Address):
                # route add <IP> mask 255.255.255.255 <GATEWAY>
                cmd = f"route add {ip} mask 255.255.255.255 {GATEWAY}"
                commands.append(cmd)
        except ValueError:
            continue
    return commands

def main():
    all_ips = []
    for domain in DOMAINS:
        print(f"{domain}")
        ips = resolve_domain(domain)
        for ip in ips:
            print(f"{ip}")
        all_ips.extend(ips)

    commands = generate_routes(all_ips)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for cmd in commands:
            f.write(cmd + "\n")

if __name__ == "__main__":
    main()
