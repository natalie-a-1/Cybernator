
# Cybernator

Cybernator is a Python-based AI system designed to automate cybersecurity lab tasks on a Kali Linux virtual machine (VM). It interprets lab instructions, executes appropriate commands, captures outputs and screenshots, and generates structured logs to help with lab reports.

## Features

- **Instruction Interpretation**: Accepts lab instructions as text input and determines the best tools and actions.
- **Command Execution**: Dynamically generates and executes commands on the Kali VM via SSH or RDP.
- **Screenshot Capture**: Takes screenshots of the VM window after each command execution.
- **Explanation Generation**: Provides explanations for each command and its output.
- **Log Generation**: Creates structured logs with commands, outputs, explanations, and screenshot references.
- **Network-Aware Scanning**: Optimizes scanning strategies based on network information to avoid triggering IDS/IPS alerts.

## Setup

### Prerequisites

- Python 3.8 or higher
- Kali Linux VM (accessible via SSH or RDP)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cybernator.git
   cd cybernator
   ```

2. Run the setup script to create a virtual environment and install dependencies:
   ```bash
   ./setup_env.sh
   ```

3. Create a `.env` file with your configuration:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file with your VM and OpenAI API credentials.

## Usage

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run the Cybernator:
   ```bash
   python main.py
   ```

3. When prompted, enter your lab instructions. You can paste a complete lab document or enter instructions one by one.

4. The system will analyze the instructions, determine the best approach, and execute the appropriate commands on the VM.

5. After execution, you'll find logs and screenshots in the `lab_logs` directory.

## Network Information Enhancement

Cybernator includes a network information enhancement that allows it to make intelligent decisions about command execution based on network information. This helps avoid triggering IDS/IPS alerts while optimizing scanning strategies.

For more information, see [NETWORK_INFO.md](NETWORK_INFO.md).

## Troubleshooting

If you encounter issues with the RDP connection, make sure:
- The VM is running and accessible
- RDP service is running on the VM
- IP address and port are correct
- Username and password are correct

If you see deprecation warnings related to TripleDES, you can ignore them or update the cryptography package to a newer version.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
