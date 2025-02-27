import time
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
        
    def get_optimal_scan_rate(self, scan_type):
        """
        Determine the optimal scan rate based on the network information and scan type.
        
        Args:
            scan_type (str): Type of scan ('syn', 'connect', 'udp', etc.)
            
        Returns:
            int: Optimal scan rate (packets per second)
        """
        # Base rate from scan strategy
        base_rate = self.scan_strategy["max_scan_rate"]
        
        # If IDS/IPS is present, reduce scan rate
        if self.security_status["ids_present"]:
            base_rate = min(base_rate, 10)  # Reduce to 10 pps if IDS is present
            
        # If stealth mode is required, reduce scan rate further
        if self.scan_strategy["stealth_required"]:
            base_rate = min(base_rate, 5)  # Reduce to 5 pps if stealth is required
            
        # Adjust based on scan type
        if scan_type == 'syn':
            # SYN scans are less noisy
            return base_rate
        elif scan_type == 'connect':
            # Connect scans are more noisy
            return max(1, base_rate // 2)
        elif scan_type == 'udp':
            # UDP scans are very noisy
            return max(1, base_rate // 3)
        else:
            return base_rate
    
    def get_scan_delay(self, scan_type):
        """
        Determine the optimal delay between scan packets.
        
        Args:
            scan_type (str): Type of scan ('syn', 'connect', 'udp', etc.)
            
        Returns:
            float: Delay in seconds between packets
        """
        # Get optimal scan rate
        rate = self.get_optimal_scan_rate(scan_type)
        
        # Convert rate to delay (seconds)
        delay = 1.0 / rate if rate > 0 else 1.0
        
        # Add recommended interval
        delay += self.scan_strategy["recommended_interval"]
        
        return delay
    
    def get_optimal_ports(self, scan_type):
        """
        Determine the optimal ports to scan based on the network information.
        
        Args:
            scan_type (str): Type of scan ('tcp', 'udp')
            
        Returns:
            list: List of ports to scan
        """
        if scan_type == 'tcp':
            return self.common_protocols["tcp_ports"]
        elif scan_type == 'udp':
            return self.common_protocols["udp_ports"]
        else:
            return []
    
    def is_safe_to_scan(self):
        """
        Determine if it's safe to scan based on the network information.
        
        Returns:
            bool: True if safe to scan, False otherwise
        """
        # If no IDS/IPS, WAF, or active monitoring, it's safe to scan
        if not self.security_status["ids_present"] and \
           not self.security_status["waf_present"] and \
           not self.monitoring["active_monitoring"]:
            return True
            
        # If firewall policy is ACCEPT, it's safer to scan
        if self.security_status["firewall_policy"] == "ACCEPT":
            return True
            
        # If safe scan window is 'any', it's safe to scan
        if self.scan_strategy["safe_scan_window"] == "any":
            return True
            
        # Otherwise, it's not safe to scan
        return False
    
    def optimize_command(self, command, command_type):
        """
        Optimize a command based on the network information.
        
        Args:
            command (str): Command to optimize
            command_type (str): Type of command ('syn', 'connect', 'udp', etc.)
            
        Returns:
            str: Optimized command
        """
        # If it's not safe to scan, add appropriate flags
        if not self.is_safe_to_scan():
            if "nmap" in command:
                # Add timing template for slower scanning
                if "-T" not in command:
                    command += " -T2"  # Use timing template 2 (slower)
                
                # Add fragmentation for stealth
                if "-f" not in command:
                    command += " -f"
                    
                # Add decoy for stealth
                if "-D" not in command:
                    command += f" -D {self.network_config['gateway']}"
            
            elif "masscan" in command:
                # Reduce rate for masscan
                rate = self.get_optimal_scan_rate(command_type)
                command = command.replace("--rate=1000", f"--rate={rate}")
        
        # If no IDS/IPS, we can be more aggressive
        elif not self.security_status["ids_present"]:
            if "nmap" in command:
                # Use faster timing template
                if "-T" not in command:
                    command += " -T4"  # Use timing template 4 (faster)
            
            elif "masscan" in command:
                # Increase rate for masscan
                rate = min(self.scan_strategy["max_scan_rate"], 10000)
                command = command.replace("--rate=1000", f"--rate={rate}")
        
        return command
    
    def get_command_execution_strategy(self, command, command_type):
        """
        Get a strategy for executing a command based on the network information.
        
        Args:
            command (str): Command to execute
            command_type (str): Type of command ('syn', 'connect', 'udp', etc.)
            
        Returns:
            dict: Strategy for executing the command
        """
        # Optimize the command
        optimized_command = self.optimize_command(command, command_type)
        
        # Get scan delay
        delay = self.get_scan_delay(command_type)
        
        # Determine if we need to split the scan
        split_scan = False
        if self.security_status["ids_present"] or self.scan_strategy["stealth_required"]:
            split_scan = True
        
        return {
            "command": optimized_command,
            "delay": delay,
            "split_scan": split_scan,
            "safe_to_scan": self.is_safe_to_scan()
        }
    
    def execute_with_strategy(self, command, command_type, executor_func):
        """
        Execute a command with the optimal strategy.
        
        Args:
            command (str): Command to execute
            command_type (str): Type of command ('syn', 'connect', 'udp', etc.)
            executor_func (function): Function to execute the command
            
        Returns:
            tuple: (output, error)
        """
        # Get execution strategy
        strategy = self.get_command_execution_strategy(command, command_type)
        
        # If not safe to scan, warn the user
        if not strategy["safe_to_scan"]:
            print("WARNING: Scanning may trigger IDS/IPS alerts. Proceeding with caution.")
        
        # If we need to split the scan, do it
        if strategy["split_scan"]:
            print(f"Splitting scan for stealth. Using delay of {strategy['delay']} seconds between packets.")
            # Execute with delay between packets
            # This would require a custom executor that supports delays
            # For now, we'll just add a delay before execution
            time.sleep(strategy["delay"])
        
        # Execute the command
        return executor_func(strategy["command"])
