# Cybernator: AI-Powered Cybersecurity Lab Automation

Cybernator is a Python-based AI system designed to automate cybersecurity lab tasks on a Kali Linux virtual machine. It interprets lab instructions, executes appropriate commands, captures outputs and screenshots, and generates structured logs to help with lab reports.

## Features

- **Intelligent Lab Instruction Parsing**: Analyzes lab documents to extract objectives, targets, and approaches
- **Automated Command Generation**: Determines the most appropriate commands based on lab instructions
- **Kali Linux VM Integration**: Connects to Kali Linux VM via SSH or RDP
- **Screenshot Capture**: Takes screenshots of command execution for documentation
- **Structured Logging**: Generates comprehensive logs with commands, outputs, and explanations
- **Report Generation**: Creates markdown reports summarizing findings and evidence

## Prerequisites

- Python 3.8+
- Kali Linux VM (accessible via SSH or RDP)
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cybernator.git
   cd cybernator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure connection settings in `.env` file:
   ```
   # SSH Connection (for direct VM access)
   VM_HOST=your-kali-vm-ip
   VM_PORT=22
   VM_USERNAME=kali
   VM_PASSWORD=your-password

   # RDP Connection (for GUI access)
   RDP_HOST=your-kali-vm-ip
   RDP_PORT=3389
   RDP_USERNAME=kali
   RDP_PASSWORD=your-password

   # OpenAI API Key
   OPENAI_API_KEY=your-openai-api-key
   ```

## Usage

### Running the Main Application

```
python main.py
```

The application will:
1. Connect to your Kali VM
2. Prompt you to enter lab instructions
3. Analyze the instructions and determine the best approach
4. Execute commands on the VM
5. Capture screenshots and outputs
6. Generate a structured log and report

### Testing VM Connection

To verify your connection to the Kali VM:

```
# Test SSH connection
python test_kali_connection.py

# Test RDP connection
python test_rdp_connection.py
```

These scripts will:
1. Attempt to connect to your Kali VM
2. Verify it's actually a Kali Linux system
3. Run basic commands to test functionality
4. Report the results

## Configuration

### Command Templates

Command templates are defined in `config.py` and can be customized to add new command types or modify existing ones.

### Network Analysis

The `network_analyzer.py` module optimizes command execution based on network conditions and security considerations.

## Troubleshooting

### Connection Issues

If you're having trouble connecting to your Kali VM:

1. Verify your VM is running and accessible
2. Check your connection settings in the `.env` file
3. Run the connection test scripts to diagnose issues:
   ```
   python test_kali_connection.py  # For SSH
   python test_rdp_connection.py   # For RDP
   ```

### Command Execution Issues

If commands aren't executing properly:

1. Check if your VM is actually running Kali Linux
2. Verify the required tools are installed on your Kali VM
3. Check the logs for error messages

## License

[MIT License](LICENSE)
