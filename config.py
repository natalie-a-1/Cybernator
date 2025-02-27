import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kali VM Configuration
# SSH Configuration
VM_HOST = os.getenv('VM_HOST')
VM_PORT = int(os.getenv('VM_PORT'))
VM_USERNAME = os.getenv('VM_USERNAME')
VM_PASSWORD = os.getenv('VM_PASSWORD')

# RDP Configuration
RDP_HOST = os.getenv('RDP_HOST')
RDP_PORT = int(os.getenv('RDP_PORT'))
RDP_USERNAME = os.getenv('RDP_USERNAME')
RDP_PASSWORD = os.getenv('RDP_PASSWORD')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Network Configuration
NETWORK_CONFIG = {
    "subnet": os.getenv('NETWORK_SUBNET'),
    "gateway": os.getenv('NETWORK_GATEWAY'),
    "interface": os.getenv('NETWORK_INTERFACE')
}

# Traffic Baselines
TRAFFIC_BASELINES = {
    "rx_pps": float(os.getenv('BASELINE_RX_PPS')),
    "tx_pps": float(os.getenv('BASELINE_TX_PPS'))
}

# Common Protocols and Ports
COMMON_PROTOCOLS = {
    "tcp_ports": os.getenv('COMMON_TCP_PORTS').split(','),
    "udp_ports": os.getenv('COMMON_UDP_PORTS').split(',')
}

# Timeouts
TIMEOUTS = {
    "tcp_fin": int(os.getenv('TCP_FIN_TIMEOUT')),
    "apache": int(os.getenv('APACHE_TIMEOUT')),
    "keepalive": int(os.getenv('KEEPALIVE_TIMEOUT'))
}

# Security Status
SECURITY_STATUS = {
    "ids_present": os.getenv('IDS_PRESENT').lower() == 'true',
    "waf_present": os.getenv('WAF_PRESENT').lower() == 'true',
    "firewall_policy": os.getenv('FIREWALL_DEFAULT_POLICY')
}

# Monitoring Tools
MONITORING = {
    "available_tools": os.getenv('AVAILABLE_TOOLS').split(','),
    "active_monitoring": os.getenv('ACTIVE_MONITORING').lower() == 'true',
    "scheduled_monitoring": os.getenv('SCHEDULED_MONITORING').lower() == 'true'
}

# Rate Limiting Status
RATE_LIMITS = {
    "api": os.getenv('API_RATE_LIMITS').lower() == 'true',
    "dns": os.getenv('DNS_RATE_LIMITS').lower() == 'true',
    "scan": os.getenv('SCAN_RATE_LIMITS').lower() == 'true'
}

# Scan Strategy Optimization
SCAN_STRATEGY = {
    "max_scan_rate": int(os.getenv('MAX_SCAN_RATE')),
    "recommended_interval": int(os.getenv('RECOMMENDED_SCAN_INTERVAL')),
    "stealth_required": os.getenv('STEALTH_MODE_REQUIRED').lower() == 'true',
    "safe_scan_window": os.getenv('SAFE_SCAN_WINDOW')
}

# Command Templates with placeholders for customization
COMMAND_TEMPLATES = {
    # Network Reconnaissance
    "dns_analysis": "tshark -i {interface} -Y 'dns' -T fields -e dns.qry.name -e ip.src {additional_filters}",
    "http_traffic": "tshark -i {interface} -Y 'http || https' -T fields -e ip.src -e http.host -e http.request.uri {additional_filters}",
    
    # Port Scanning
    "tcp_syn_scan": "nmap -sS {verbosity} {target}",
    "tcp_connect_scan": "nmap -sT {verbosity} {target}",
    "udp_scan": "nmap -sU {verbosity} {top_ports} {target}",
    "service_scan": "nmap -sV {verbosity} {additional_flags} {target}",
    "os_detection": "nmap -O {verbosity} {target}",
    "all_ports_scan": "nmap -p- {verbosity} {target}",
    "aggressive_scan": "nmap -A {verbosity} {target}",
    
    # Custom Port Scanning
    "custom_port_scan": "nmap -p {port_list} {verbosity} {target}",
    "non_standard_ports": "nmap -p {port_list} {verbosity} {target}",
    
    # Host Discovery
    "ping_sweep": "nmap -sn {target}",
    "arp_scan": "arp-scan {target_network}",
    
    # Specific Tools
    "hping3_scan": "hping3 -S -p {initial_port} --scan {port_range} {target}",
    "masscan_quick": "masscan -p {port_range} {target} --rate={rate}",
    "netcat_scan": "nc -zv {target} {port_range}"
}

# Default parameter values - Updated based on network information
DEFAULT_PARAMS = {
    "interface": NETWORK_CONFIG["interface"],
    "verbosity": "-v",
    "target": NETWORK_CONFIG["subnet"],
    "top_ports": "--top-ports 20",
    "additional_flags": "",
    "additional_filters": "",
    "port_list": ",".join(COMMON_PROTOCOLS["tcp_ports"]),
    "port_range": "1-1000",
    "initial_port": COMMON_PROTOCOLS["tcp_ports"][0],
    "target_network": "--localnet",
    "rate": str(SCAN_STRATEGY["max_scan_rate"])
}
