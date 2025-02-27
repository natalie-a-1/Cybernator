# Network Information Enhancement

This document describes the network information enhancement added to the Cybernator system. This enhancement allows the system to make intelligent decisions about command execution based on network information, helping to avoid triggering IDS/IPS alerts.

## Overview

The network information enhancement consists of:

1. **Environment Variables**: Network information is stored in the `.env` file.
2. **Configuration**: The network information is loaded into the `config.py` file.
3. **Network Analyzer**: A new `NetworkAnalyzer` class analyzes the network information and optimizes command execution.
4. **Main Integration**: The `main.py` file has been updated to use the `NetworkAnalyzer` class.

## Environment Variables

The following environment variables have been added to the `.env` file:

```
# Network Configuration
NETWORK_SUBNET=192.168.13.0/24
NETWORK_GATEWAY=192.168.13.1
NETWORK_INTERFACE=eth0

# Traffic Baselines
BASELINE_RX_PPS=10.9
BASELINE_TX_PPS=16.5

# Common Protocols and Ports
COMMON_TCP_PORTS=22,3389
COMMON_UDP_PORTS=67,68

# Timeouts
TCP_FIN_TIMEOUT=60
APACHE_TIMEOUT=300
KEEPALIVE_TIMEOUT=5

# Security Status
IDS_PRESENT=false
WAF_PRESENT=false
FIREWALL_DEFAULT_POLICY=ACCEPT

# Monitoring Tools
AVAILABLE_TOOLS=tcpdump,nmap,wireshark
ACTIVE_MONITORING=false
SCHEDULED_MONITORING=false

# Rate Limiting Status
API_RATE_LIMITS=false
DNS_RATE_LIMITS=false
SCAN_RATE_LIMITS=false

# Scan Strategy Optimization
MAX_SCAN_RATE=50
RECOMMENDED_SCAN_INTERVAL=0
STEALTH_MODE_REQUIRED=false
SAFE_SCAN_WINDOW=any
```

## Configuration

The `config.py` file has been updated to load the network information from the `.env` file:

```python
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
```

## Network Analyzer

A new `NetworkAnalyzer` class has been created in `network_analyzer.py` to analyze the network information and optimize command execution:

```python
class NetworkAnalyzer:
    """
    Analyzes network information to optimize scanning strategies and avoid triggering IDS/IPS alerts.
    Uses the network information from the .env file to make intelligent decisions.
    """
    
    def __init__(self):
        self.network_config = NETWORK_CONFIG
        self.traffic_baselines = TRAFFIC_BASELINES
        self.common_protocols = COMMON_PROTOCOLS
        self.timeouts = TIMEOUTS
        self.security_status = SECURITY_STATUS
        self.monitoring = MONITORING
        self.rate_limits = RATE_LIMITS
        self.scan_strategy = SCAN_STRATEGY
```

The `NetworkAnalyzer` class provides the following methods:

- `get_optimal_scan_rate(scan_type)`: Determines the optimal scan rate based on the network information and scan type.
- `get_scan_delay(scan_type)`: Determines the optimal delay between scan packets.
- `get_optimal_ports(scan_type)`: Determines the optimal ports to scan based on the network information.
- `is_safe_to_scan()`: Determines if it's safe to scan based on the network information.
- `optimize_command(command, command_type)`: Optimizes a command based on the network information.
- `get_command_execution_strategy(command, command_type)`: Gets a strategy for executing a command based on the network information.
- `execute_with_strategy(command, command_type, executor_func)`: Executes a command with the optimal strategy.

## Main Integration

The `main.py` file has been updated to use the `NetworkAnalyzer` class:

```python
def execute_lab_instruction(self, instruction):
    """Process a single lab instruction using the multi-agent system"""
    print(f"\nProcessing instruction: {instruction}")
    
    # Use the command processor to generate a customized command and explanation
    command, command_type, selection_explanation = self.command_processor.process_instruction(instruction)
    
    if not command:
        print(f"Could not determine appropriate command for: {instruction}")
        return None, None
        
    print(f"Generated command: {command}")
    print(f"Command type: {command_type}")
    
    # Use network analyzer to optimize command execution
    print("Optimizing command based on network information...")
    strategy = self.network_analyzer.get_command_execution_strategy(command, command_type)
    optimized_command = strategy["command"]
    
    if optimized_command != command:
        print(f"Optimized command: {optimized_command}")
        
    if not strategy["safe_to_scan"]:
        print("WARNING: Scanning may trigger IDS/IPS alerts. Proceeding with caution.")
        
    if strategy["split_scan"]:
        print(f"Using split scan strategy with delay of {strategy['delay']} seconds between operations.")
        
    # Execute optimized command on VM
    def execute_func(cmd):
        return self.vm.execute(cmd)
        
    output, error = self.network_analyzer.execute_with_strategy(command, command_type, execute_func)
```

## Benefits

The network information enhancement provides the following benefits:

1. **Intelligent Command Optimization**: Commands are optimized based on the network information, helping to avoid triggering IDS/IPS alerts.
2. **Adaptive Scan Rates**: Scan rates are adjusted based on the network information and scan type.
3. **Optimal Port Selection**: Ports to scan are selected based on the network information.
4. **Safe Scanning**: The system determines if it's safe to scan based on the network information.
5. **Split Scanning**: The system can split scans to avoid triggering IDS/IPS alerts.
6. **Delay Calculation**: The system calculates optimal delays between scan packets.

## Testing

A test script `test_network_analyzer.py` has been created to verify that the network information is being loaded correctly and that the `NetworkAnalyzer` class is working as expected.

```bash
python test_network_analyzer.py
```

The test script verifies:

1. Network information is loaded correctly from the `.env` file.
2. The `NetworkAnalyzer` class is working as expected.
3. Commands are optimized based on the network information.
4. Scan rates are adjusted based on the network information and scan type.
5. Ports to scan are selected based on the network information.
6. The system determines if it's safe to scan based on the network information.
7. The system calculates optimal delays between scan packets.
