import paramiko
from config import VM_HOST, VM_PORT, VM_USERNAME, VM_PASSWORD

class VMConnection:
    def __init__(self):
        self.client = None
        self.connected = False

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
            return True
        except Exception as e:
            print(f"Failed to connect to VM: {e}")
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
