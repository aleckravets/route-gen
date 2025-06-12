const dns = require('dns').promises;
const fs = require('fs');
const ip = require('ip');

const DOMAINS = [
  'figma.com',
  'api.figma.com',
  'cdn.figma.com',
  'fonts.gstatic.com',
];

const GATEWAY = '0.0.0.0';
const SUBNET_MASK = '255.255.255.0'; // /24
const OUTPUT_FILE = 'add-routes.bat';

function getSubnet(ipAddr, maskBits = 24) {
  const subnet = ip.subnet(ipAddr, ip.fromPrefixLen(maskBits));
  return subnet.networkAddress;
}

async function resolveDomain(domain) {
  try {
    const addresses = await dns.resolve4(domain);
    console.log(`🔍 ${domain}:`, addresses);
    return addresses;
  } catch (err) {
    console.error(`failed to resolve domain ${domain}:`, err.message);
    return [];
  }
}

(async () => {
  const allIPs = new Set();

  for (const domain of DOMAINS) {
    const ips = await resolveDomain(domain);
    ips.forEach(ip => allIPs.add(ip));
  }

  // Группируем по подсетям /24
  const subnets = new Set();
  allIPs.forEach(ipAddr => {
    const subnet = getSubnet(ipAddr);
    subnets.add(subnet);
  });

  const lines = [];
  for (const subnet of Array.from(subnets).sort()) {
    lines.push(`route add ${subnet} mask ${SUBNET_MASK} ${GATEWAY}`);
  }

  fs.writeFileSync(OUTPUT_FILE, lines.join('\n'), 'utf8');

})();
