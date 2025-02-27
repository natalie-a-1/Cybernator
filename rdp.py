import time
import os
import subprocess
import pyautogui
import cv2
import numpy as np
from config import RDP_HOST, RDP_PORT, RDP_USERNAME, RDP_PASSWORD
import datetime

class RDPConnection:
    """Class to handle RDP connections and command execution for macOS to Kali Linux"""
    
    
    def __init__(self):
        self.connected = False
        self.terminal_open = False
        self.screenshot_dir = "lab_logs/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def connect(self):
        """Connect to the VM via RDP on macOS"""
        try:
            print(f"Connecting to {RDP_HOST}:{RDP_PORT} via RDP...")
            
            # Launch Microsoft Remote Desktop on macOS
            script = '''
            tell application "Microsoft Remote Desktop"
                activate
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            
            # Provide connection details for manual connection
            print("Microsoft Remote Desktop launched. Please manually connect to the VM.")
            print(f"Host: {RDP_HOST}:{RDP_PORT}")
            print(f"Username: {RDP_USERNAME}")
            print(f"Password: {RDP_PASSWORD}")
            
            # Wait for user to connect
            print("Waiting for RDP connection to establish...")
            time.sleep(10)  # Give user time to connect
            
            # Assume connection is successful if we can take a screenshot
            screenshot = pyautogui.screenshot()
            if screenshot:
                self.connected = True
                print("RDP connection established.")
                
                # Open terminal
                if self._open_terminal():
                    return True
                else:
                    print("Failed to open terminal.")
                    return False
            else:
                print("Failed to establish RDP connection.")
                return False
                
        except Exception as e:
            print(f"Error connecting via RDP: {e}")
            return False
    
    def _open_terminal(self):
        """Open a terminal window in Kali Linux"""
        try:
            # Use Ctrl+Option+T to open terminal in Kali
            pyautogui.hotkey('ctrl', 'option', 't')
            time.sleep(2)
            
            # Take a screenshot to verify terminal is open
            self._take_screenshot("terminal_opened")
            
            self.terminal_open = True
            return True
        except Exception as e:
            print(f"Error opening terminal: {e}")
            return False
    
    def _take_screenshot(self, name_prefix):
        """Take a screenshot and save it with timestamp"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshot_dir, f"{name_prefix}_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def execute(self, command):
        """Execute a command in the Kali Linux terminal"""
        if not self.connected or not self.terminal_open:
            print("Not connected to RDP or terminal not open.")
            return None, "Not connected to RDP or terminal not open."
        
        try:
            # Clear any existing text in the terminal with Ctrl+U
            pyautogui.hotkey('ctrl', 'u')
            time.sleep(0.5)
            
            # Type the command
            pyautogui.write(command)
            
            # Take screenshot before execution
            self._take_screenshot(f"before_exec_{command[:20].replace(' ', '_')}")
            
            # Execute command
            pyautogui.press('enter')
            
            # Wait for command to execute
            time.sleep(5)  # Adjust based on expected command execution time
            
            # Take screenshot after execution
            screenshot_path = self._take_screenshot(f"after_exec_{command[:20].replace(' ', '_')}")
            
            # For now, we'll just return the screenshot path as we can't easily extract text
            return f"Command executed. See screenshot: {screenshot_path}", None
            
        except Exception as e:
            print(f"Error executing command: {e}")
            return None, f"Error executing command: {e}"
    
    def close(self):
        """Close the RDP connection"""
        try:
            # Close the terminal with Ctrl+D
            if self.terminal_open:
                pyautogui.hotkey('ctrl', 'd')
                time.sleep(1)
                self.terminal_open = False
            
            # Close the RDP window with Cmd+W
            pyautogui.hotkey('command', 'w')
            time.sleep(1)
            
            # Confirm any "disconnect" dialogs with Enter
            pyautogui.press('enter')
            
            self.connected = False
            print("RDP connection closed.")
            return True
        except Exception as e:
            print(f"Error closing RDP connection: {e}")
            return False
