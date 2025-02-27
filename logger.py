import os
import time
import pyautogui
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_dir = "lab_logs"
        self.screenshot_dir = os.path.join(self.log_dir, "screenshots")
        self.log_file = None
        self.step_count = 0
        self._setup_directories()

    def _setup_directories(self):
        """Create necessary directories for logs and screenshots"""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Create new log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"lab_log_{timestamp}.txt")

    def take_screenshot(self):
        """Capture screenshot of the VM window"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
            # Wait briefly for command output to appear
            time.sleep(2)
            pyautogui.screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None

    def log_step(self, command, output, error=None, explanation=None):
        """Log a command execution step"""
        self.step_count += 1
        screenshot_path = self.take_screenshot()
        
        with open(self.log_file, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Step {self.step_count}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Command: {command}\n\n")
            
            if output:
                f.write("Output:\n")
                f.write(f"{output}\n")
            
            if error:
                f.write("Errors:\n")
                f.write(f"{error}\n")
            
            if explanation:
                f.write("\nExplanation:\n")
                f.write(f"{explanation}\n")
            
            if screenshot_path:
                f.write(f"\nScreenshot: {os.path.basename(screenshot_path)}\n")
            
            f.write(f"{'='*50}\n")

    def get_log_file(self):
        """Return path to current log file"""
        return self.log_file
