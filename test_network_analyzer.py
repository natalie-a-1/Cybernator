import os
from dotenv import load_dotenv
from config import (
    NETWORK_CONFIG, 
    TRAFFIC_BASELINES, 
    COMMON_PROTOCOLS, 
    TIMEOUTS, 
    SECURITY_STATUS, 
    MONITORING, 
    RATE_LIMITS, 
    SCAN_STRATEGY
)
from network_analyzer import NetworkAnalyzer

def test_network_config():
    """Test that network configuration is loaded correctly from .env"""
    print("Testing network configuration...")
    
    # Check that network configuration is loaded
    print(f"Network subnet: {NETWORK_CONFIG['subnet']}")
    print(f"Network gateway: {NETWORK_CONFIG['gateway']}")
    print(f"Network interface: {NETWORK_CONFIG['interface']}")
    
    # Check that traffic baselines are loaded
    print(f"Baseline RX PPS: {TRAFFIC_BASELINES['rx_pps']}")
    print(f"Baseline TX PPS: {TRAFFIC_BASELINES['tx_pps']}")
    
    # Check that common protocols are loaded
    print(f"Common TCP ports: {COMMON_PROTOCOLS['tcp_ports']}")
    print(f"Common UDP ports: {COMMON_PROTOCOLS['udp_ports']}")
    
    # Check that timeouts are loaded
    print(f"TCP FIN timeout: {TIMEOUTS['tcp_fin']}")
    print(f"Apache timeout: {TIMEOUTS['apache']}")
    print(f"Keepalive timeout: {TIMEOUTS['keepalive']}")
    
    # Check that security status is loaded
    print(f"IDS present: {SECURITY_STATUS['ids_present']}")
    print(f"WAF present: {SECURITY_STATUS['waf_present']}")
    print(f"Firewall policy: {SECURITY_STATUS['firewall_policy']}")
    
    # Check that monitoring is loaded
    print(f"Available tools: {MONITORING['available_tools']}")
    print(f"Active monitoring: {MONITORING['active_monitoring']}")
    print(f"Scheduled monitoring: {MONITORING['scheduled_monitoring']}")
    
    # Check that rate limits are loaded
    print(f"API rate limits: {RATE_LIMITS['api']}")
    print(f"DNS rate limits: {RATE_LIMITS['dns']}")
    print(f"Scan rate limits: {RATE_LIMITS['scan']}")
    
    # Check that scan strategy is loaded
    print(f"Max scan rate: {SCAN_STRATEGY['max_scan_rate']}")
    print(f"Recommended interval: {SCAN_STRATEGY['recommended_interval']}")
    print(f"Stealth required: {SCAN_STRATEGY['stealth_required']}")
    print(f"Safe scan window: {SCAN_STRATEGY['safe_scan_window']}")

def test_network_analyzer():
    """Test the NetworkAnalyzer class"""
    print("\nTesting NetworkAnalyzer class...")
    
    # Create a NetworkAnalyzer instance
    analyzer = NetworkAnalyzer()
    
    # Test get_optimal_scan_rate
    print("\nTesting get_optimal_scan_rate...")
    print(f"Optimal scan rate for SYN scan: {analyzer.get_optimal_scan_rate('syn')}")
    print(f"Optimal scan rate for Connect scan: {analyzer.get_optimal_scan_rate('connect')}")
    print(f"Optimal scan rate for UDP scan: {analyzer.get_optimal_scan_rate('udp')}")
    
    # Test get_scan_delay
    print("\nTesting get_scan_delay...")
    print(f"Scan delay for SYN scan: {analyzer.get_scan_delay('syn')}")
    print(f"Scan delay for Connect scan: {analyzer.get_scan_delay('connect')}")
    print(f"Scan delay for UDP scan: {analyzer.get_scan_delay('udp')}")
    
    # Test get_optimal_ports
    print("\nTesting get_optimal_ports...")
    print(f"Optimal ports for TCP scan: {analyzer.get_optimal_ports('tcp')}")
    print(f"Optimal ports for UDP scan: {analyzer.get_optimal_ports('udp')}")
    
    # Test is_safe_to_scan
    print("\nTesting is_safe_to_scan...")
    print(f"Is safe to scan: {analyzer.is_safe_to_scan()}")
    
    # Test optimize_command
    print("\nTesting optimize_command...")
    nmap_command = "nmap -sS 192.168.13.0/24"
    optimized_nmap = analyzer.optimize_command(nmap_command, 'syn')
    print(f"Original nmap command: {nmap_command}")
    print(f"Optimized nmap command: {optimized_nmap}")
    
    masscan_command = "masscan -p 1-1000 192.168.13.0/24 --rate=1000"
    optimized_masscan = analyzer.optimize_command(masscan_command, 'syn')
    print(f"Original masscan command: {masscan_command}")
    print(f"Optimized masscan command: {optimized_masscan}")
    
    # Test get_command_execution_strategy
    print("\nTesting get_command_execution_strategy...")
    strategy = analyzer.get_command_execution_strategy(nmap_command, 'syn')
    print(f"Command execution strategy for nmap: {strategy}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run tests
    test_network_config()
    test_network_analyzer()
    
    print("\nAll tests completed successfully!")
