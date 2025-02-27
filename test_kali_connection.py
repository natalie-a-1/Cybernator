#!/usr/bin/env python3
"""
Simple script to test connection to Kali Linux VM
"""

import subprocess
import time
import os
from config import VM_HOST, VM_PORT, VM_USERNAME, VM_PASSWORD
import paramiko

def test_ssh_connection():
    """Test SSH connection to Kali VM"""
    print(f"Testing SSH connection to {VM_HOST}:{VM_PORT}...")
    
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect with timeout
        client.connect(
            VM_HOST,
            port=VM_PORT,
            username=VM_USERNAME,
            password=VM_PASSWORD,
            timeout=10
        )
        
        print("✅ SSH connection successful!")
        
        # Run basic commands to verify Kali Linux
        commands = [
            "whoami",
            "uname -a",
            "pwd",
            "ls /usr/share/wordlists",
            "which nmap"
        ]
        
        for cmd in commands:
            print(f"\nExecuting: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                print(f"Error: {error}")
            else:
                print(f"Output: {output}")
                
                # Check for Kali-specific indicators
                if cmd == "uname -a" and "kali" in output.lower():
                    print("✅ Confirmed Kali Linux system")
                elif cmd == "ls /usr/share/wordlists" and output:
                    print("✅ Kali wordlists directory exists")
                elif cmd == "which nmap" and "/nmap" in output:
                    print("✅ Nmap is installed")
        
        # Close connection
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ SSH connection failed: {e}")
        return False

if __name__ == "__main__":
    test_ssh_connection()
