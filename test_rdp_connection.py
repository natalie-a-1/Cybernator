
#!/usr/bin/env python3
"""
Simple script to test RDP connection to Kali Linux VM
"""

import time
import os
from rdp import RDPConnection

def test_rdp_connection():
    """Test RDP connection to Kali VM"""
    print("Testing RDP connection to Kali VM...")
    
    # Create RDP connection
    rdp = RDPConnection()
    
    # Connect to VM
    if rdp.connect():
        print("✅ RDP connection established")
        
        # Execute basic commands to verify Kali Linux
        commands = [
            "whoami",
            "uname -a",
            "pwd",
            "ls /usr/share/wordlists",
            "which nmap"
        ]
        
        for cmd in commands:
            print(f"\nExecuting: {cmd}")
            output, error = rdp.execute(cmd)
            
            if error:
                print(f"Error: {error}")
            else:
                print(f"Output: {output}")
        
        # Close connection
        rdp.close()
        print("\nRDP connection test completed")
        return True
    else:
        print("❌ Failed to establish RDP connection")
        return False

if __name__ == "__main__":
    test_rdp_connection()
