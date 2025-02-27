from rdp import RDPConnection
import time

def test_rdp_connection():
    """Test the RDP connection functionality for macOS to Kali Linux"""
    print("Testing RDP connection to Kali Linux...")
    
    # Create RDP connection
    rdp = RDPConnection()
    
    try:
        # Connect to VM
        print("Connecting to VM via RDP...")
        if not rdp.connect():
            print("Failed to connect to VM via RDP.")
            return
        
        print("Connected to VM via RDP.")
        
        # Test command execution
        print("\nTesting command execution...")
        print("Executing 'ls -la' command...")
        output, error = rdp.execute("ls -la")
        
        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")
        
        # Test another command
        print("\nExecuting 'whoami' command...")
        output, error = rdp.execute("whoami")
        
        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")
        
        # Wait for user to interact with the RDP session
        print("\nRDP session is now active.")
        print("You can interact with the VM through the RDP window.")
        print("Press Ctrl+C in this terminal when you're done to close the connection.")
        
        # Keep the script running until user interrupts
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nUser interrupted. Closing RDP connection...")
        
    finally:
        # Close RDP connection
        rdp.close()
        print("RDP connection closed.")

if __name__ == "__main__":
    test_rdp_connection()
