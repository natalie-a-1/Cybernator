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

# Default parameter values
DEFAULT_PARAMS = {
    "interface": "eth0",
    "verbosity": "-v",
    "target": "192.168.1.0/24",
    "top_ports": "--top-ports 20",
    "additional_flags": "",
    "additional_filters": "",
    "port_list": "21,22,23,25,80,443,3389",
    "port_range": "1-1000",
    "initial_port": "80",
    "target_network": "--localnet",
    "rate": "1000"
}
