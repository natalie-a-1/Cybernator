import paramiko
from config import VM_HOST, VM_PORT, VM_USERNAME, VM_PASSWORD

class VMConnection:
    def __init__(self):
        self.client = None
        self.connected = False
        self.is_kali = False

    def connect(self):
        """Establish SSH connection to the Kali VM"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                VM_HOST,
                port=VM_PORT,
                username=VM_USERNAME,
                password=VM_PASSWORD,
                timeout=10  # Add 10-second timeout
            )
            self.connected = True
            
            # Verify we're connected to a Kali Linux system
            if self.verify_kali_system():
                print("✅ Verified connection to Kali Linux system")
                return True
            else:
                print("⚠️ Connected to a system, but it doesn't appear to be Kali Linux")
                # Continue anyway since we have a connection
                return True
        except Exception as e:
            print(f"Failed to connect to VM: {e}")
            return False
            
    def verify_kali_system(self):
        """Verify that we're connected to a Kali Linux system"""
        if not self.connected:
            return False
            
        try:
            # Check for Kali-specific indicators
            stdin, stdout, stderr = self.client.exec_command("uname -a")
            uname_output = stdout.read().decode().strip()
            
            # Check if "kali" is in the uname output
            if "kali" in uname_output.lower():
                self.is_kali = True
                
            # Check for Kali wordlists directory
            stdin, stdout, stderr = self.client.exec_command("ls /usr/share/wordlists")
            wordlists_output = stdout.read().decode().strip()
            
            # Check if common Kali tools are installed
            stdin, stdout, stderr = self.client.exec_command("which nmap metasploit-framework")
            tools_output = stdout.read().decode().strip()
            
            # If any of these checks pass, it's likely Kali
            return self.is_kali or wordlists_output or tools_output
        except Exception as e:
            print(f"Error verifying Kali system: {e}")
            return False

    def execute(self, command):
        """Execute a command on the VM and return output"""
        if not self.connected:
            if not self.connect():
                return None, None

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            print(f"Command execution failed: {e}")
            return None, None

    def close(self):
        """Close the SSH connection"""
        if self.client:
            self.client.close()
            self.connected = False
