# Cybersecurity Lab Automation

An advanced Python-based system for automating cybersecurity lab tasks on a Kali Linux VM, featuring a multi-agent architecture for intelligent command selection, explanation, and lab goal analysis.

## Architecture

The system uses a sophisticated multi-agent approach to process lab instructions:

1. **Lab Instruction Parser**: Analyzes full lab documents to extract goals, tasks, and requirements
2. **Lab Strategy Planner**: Determines the optimal approach to complete the lab
3. **Context Analyzer**: Extracts key parameters from instructions (targets, ports, protocols)
4. **Command Generator**: Selects and customizes commands based on context
5. **Explanation Generator**: Provides detailed reasoning for command selection
6. **Output Analyzer**: Interprets command outputs from a security perspective
7. **Evidence Collector**: Gathers and analyzes evidence from command outputs
8. **Report Generator**: Creates comprehensive lab reports based on collected evidence

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For RDP functionality on macOS, you'll need Microsoft Remote Desktop:
```
brew install --cask microsoft-remote-desktop
```

3. Configuration is already set in `config.py` with:
- VM connection details (SSH and RDP)
- OpenAI API key
- Flexible command templates with customizable parameters

## Usage

1. Run the automation script:
```bash
python main.py
```

2. Enter your lab instructions:
   - You can paste a complete lab document (recommended)
   - Or enter instructions one at a time

3. The system will:
   - Connect to your Kali VM
   - Analyze the lab document to extract goals and requirements
   - Determine the optimal strategy to complete the lab
   - Execute a sequence of commands based on the strategy
   - Collect and analyze evidence from command outputs
   - Generate a comprehensive lab report
   - Take screenshots throughout the process
   - Create detailed log files

4. Find your lab documentation in the `lab_logs` directory:
   - Text logs with commands, outputs, and explanations
   - Screenshots in the `screenshots` subdirectory
   - A comprehensive lab report in Markdown format

## Features

- **Full Lab Document Analysis**: Extracts goals, tasks, and requirements from complete lab instructions
- **Strategic Lab Planning**: Determines the optimal approach to complete the lab
- **Intelligent Context Analysis**: Extracts key parameters from natural language instructions
- **Dynamic Command Customization**: Adapts commands to specific lab requirements
- **Strategic Explanation Generation**: Explains why each command was chosen for the task
- **Technical Output Analysis**: Interprets command results from a security perspective
- **Evidence Collection and Analysis**: Gathers and analyzes evidence from command outputs
- **Automated Report Generation**: Creates comprehensive lab reports based on collected evidence
- **Flexible Command Templates**: Customizable templates with placeholders for parameters
- **SSH Connection Management**: Reliable connection to Kali VM with error handling
- **Structured Documentation**: Comprehensive logs with commands, outputs, and explanations

## Example Lab Document

The system can process complete lab documents like this:

```markdown
# Lab 2: Identifying a Target Host on the Lumon Industries Network

## Welcome, Lumon Industries Employees

Employees of the Macrodata Refinement Division, you have recently noticed suspicious behavior from one of your colleagues. To ensure data integrity and security, you must determine which computer belongs to this individual by analyzing network activity.

The suspected employee's activity will be displayed on the projector during the lab as they browse different Lumon Industries websites in a specific order.

### Your Task
Your objective is to passively observe network traffic to identify this colleague's computer IP address based on their browsing behavior.

## Learning Objectives
1. Understand passive reconnaissance techniques using network traffic analysis.
2. Use DNS query observation to profile a host's activity.
3. Analyze HTTP/S communications to correlate user behavior.
4. Identify a host based on observed traffic without active interaction.

## Lab Goals
- Observe and analyze DNS queries to track host activity.
- Identify HTTP/S communications to correlate user behavior.
- Determine the host generating specific network traffic patterns.
```

## Testing

You can test the system without connecting to a VM:
```bash
python test.py
```

This will simulate command execution, lab document parsing, evidence collection, and report generation.
