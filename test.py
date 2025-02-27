from openai import OpenAI
from logger import Logger
from config import OPENAI_API_KEY, COMMAND_TEMPLATES
from agents import CommandProcessor
from lab_parser import LabInstructionParser, LabStrategy, EvidenceCollector
import os
import time
import json

class TestLabAutomation:
    def __init__(self):
        self.logger = Logger()
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.command_processor = CommandProcessor(self.client)
        self.lab_parser = LabInstructionParser(self.client)
        self.lab_strategy = LabStrategy(self.client)
        self.evidence_collector = EvidenceCollector()
        
    def get_output_explanation(self, command, output):
        """Generate explanation for command output"""
        try:
            print("Generating output analysis...")
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert. Analyze and explain the output of this command in a clear, technical manner. Focus on what the output reveals and its security implications."},
                    {"role": "user", "content": f"Command: {command}\nOutput: {output}\nProvide a technical analysis of this output."}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting output explanation: {e}")
            return "Output analysis unavailable"

    def simulate_command_execution(self, command):
        """Simulate command execution with mock output"""
        print(f"Simulating execution of: {command}")
        
        # Mock outputs for different command types
        if "nmap" in command and "-sS" in command:
            return """
Starting Nmap 7.93 ( https://nmap.org ) at 2025-02-26 19:18 CST
Nmap scan report for 192.168.1.1
Host is up (0.0023s latency).
Not shown: 995 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3389/tcp open  ms-wbt-server
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 0.25 seconds
            """, None
        elif "nmap" in command and "-sV" in command:
            return """
Starting Nmap 7.93 ( https://nmap.org ) at 2025-02-26 19:18 CST
Nmap scan report for 192.168.1.1
Host is up (0.0023s latency).
Not shown: 995 closed ports
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.5
80/tcp   open  http          Apache httpd 2.4.41
443/tcp  open  https         Apache httpd 2.4.41
3389/tcp open  ms-wbt-server xrdp 0.9.12
8080/tcp open  http-proxy    Squid http proxy 4.10

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds
            """, None
        elif "nmap" in command and "-sn" in command:
            return """
Starting Nmap 7.93 ( https://nmap.org ) at 2025-02-26 19:18 CST
Nmap scan report for 192.168.1.1
Host is up (0.0023s latency).
Nmap scan report for 192.168.1.100
Host is up (0.0045s latency).
Nmap scan report for 192.168.1.101
Host is up (0.0032s latency).
Nmap scan report for 192.168.1.102
Host is up (0.0028s latency).
Nmap done: 256 IP addresses (4 hosts up) scanned in 2.45 seconds
            """, None
        elif "tshark" in command and "dns" in command:
            return """
google.com    192.168.1.100
example.com   192.168.1.101
mail.com      192.168.1.102
dns.google    192.168.1.100
api.example.com 192.168.1.101
lumon.com     192.168.1.101
intranet.lumon.com 192.168.1.101
hr.lumon.com  192.168.1.101
            """, None
        elif "tshark" in command and "http" in command:
            return """
192.168.1.100    example.com    /index.html
192.168.1.101    lumon.com     /index.html
192.168.1.101    intranet.lumon.com     /login
192.168.1.101    hr.lumon.com    /employee-portal
192.168.1.101    lumon.com     /products
192.168.1.101    lumon.com     /about
            """, None
        elif "arp-scan" in command:
            return """
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.1.1	00:50:56:c0:00:08	VMware, Inc.
192.168.1.100	00:0c:29:8d:5a:b1	VMware, Inc.
192.168.1.101	00:0c:29:f4:1e:6c	VMware, Inc.
192.168.1.102	00:0c:29:2d:3f:1b	VMware, Inc.

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.7: 256 hosts scanned in 2.323 seconds (110.20 hosts/sec). 4 responded
            """, None
        else:
            return "Command executed successfully", None

    def process_instruction(self, instruction):
        """Process a lab instruction using the multi-agent system"""
        print(f"\nProcessing instruction: {instruction}")
        
        # Use the command processor to generate a customized command and explanation
        command, command_type, selection_explanation = self.command_processor.process_instruction(instruction)
        
        if not command:
            print(f"Could not determine appropriate command for: {instruction}")
            return
            
        print(f"Generated command: {command}")
        print(f"Command type: {command_type}")
        print(f"Selection explanation: {selection_explanation[:100]}...")
        
        # Simulate execution
        output, error = self.simulate_command_execution(command)
        
        # Process output for evidence collection
        if output and not error:
            self._process_output_for_evidence(command, command_type, output)
        
        # Generate explanation for the output
        if output:
            output_explanation = self.get_output_explanation(command, output)
            # Combine the selection explanation and output explanation
            full_explanation = f"{selection_explanation}\n\nOutput Analysis:\n{output_explanation}"
            print(f"Output analysis: {output_explanation[:100]}...")
        else:
            full_explanation = selection_explanation
        
        # Log the step
        self.logger.log_step(command, output, error, full_explanation)
        print(f"Step logged with screenshot at: {self.logger.screenshot_dir}")
        
        # Small delay to see output
        time.sleep(1)
    
    def _process_output_for_evidence(self, command, command_type, output):
        """Process command output to collect evidence"""
        try:
            # Process DNS analysis output
            if command_type == "dns_analysis" and "dns" in command:
                lines = output.strip().split('\n')
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        query = parts[0]
                        source = parts[1]
                        self.evidence_collector.add_dns_query(query, source)
            
            # Process HTTP traffic output
            elif command_type == "http_traffic" and ("http" in command or "https" in command):
                lines = output.strip().split('\n')
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        source = parts[0]
                        host = parts[1]
                        uri = parts[2]
                        self.evidence_collector.add_http_request(source, host, uri)
            
            # Process general network traffic
            elif "nmap" in command:
                # Extract hosts from nmap output
                hosts = []
                current_host = None
                
                lines = output.strip().split('\n')
                for line in lines:
                    if "Nmap scan report for" in line:
                        host_match = line.split("for")[1].strip()
                        current_host = host_match
                        hosts.append(current_host)
                    elif current_host and "open" in line and "tcp" in line:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            port = parts[0].split('/')[0]
                            protocol = parts[0].split('/')[1]
                            state = parts[1]
                            service = parts[2]
                            self.evidence_collector.add_network_traffic(
                                "scanner", current_host, protocol, 
                                f"Port {port} is {state}, running {service}"
                            )
        except Exception as e:
            print(f"Error processing output for evidence: {e}")

    def test_lab_document_parsing(self):
        """Test parsing a full lab document"""
        print("\nTesting lab document parsing...")
        
        # Sample lab document
        lab_document = """
# **Lab 2: Identifying a Target Host on the Lumon Industries Network**

## **Welcome, Lumon Industries Employees**  

Employees of the **Macrodata Refinement Division**, you have recently noticed suspicious behavior from one of your colleagues. To ensure **data integrity and security**, you must determine which computer belongs to this individual by analyzing network activity.  

The suspected employee's activity will be displayed on the **projector** during the lab as they browse different **Lumon Industries websites in a specific order**.  

### **Your Task**  
Your objective is to **passively observe network traffic** to identify this colleague's **computer IP address** based on their browsing behavior.

---

## **Learning Objectives**  

By the end of this lab, you will:  

1. Understand **passive reconnaissance techniques** using network traffic analysis.  
2. Use **DNS query observation** to profile a host's activity.  
3. Analyze **HTTP/S communications** to correlate user behavior.  
4. Identify a host based on observed traffic **without active interaction**.  

---

## **Lab Setup**  

- Use your **virtual machine (VM)** provided by **Lumon Industries**.  
- The **network environment** contains multiple hosts, including the **target computer**.  
- Your goal is to **identify the specific host** based on **passive analysis** of network traffic.  

---

## **Lab Goals**  

- Observe and analyze **DNS queries** to track host activity.  
- Identify **HTTP/S communications** to correlate user behavior.  
- Determine the **host generating specific network traffic patterns**.  

---

## **Lab Report**  

Submit the report **before the deadline**, including:  

- **Screenshots** detailing each step towards identifying the target host.  
- A **list of DNS queries** (domains queried).  
- Answers to **additional questions** about the network.  
- The report must be submitted using the **provided template** with all required sections filled in.  

---

### **Good luck, Lumon employees.**  
Your department's **security depends on your skills!**
        """
        
        # Parse the lab document
        lab_components = self.lab_parser.parse_lab_document(lab_document)
        
        print("\nExtracted Lab Components:")
        print(json.dumps(lab_components, indent=2))
        
        # Determine strategy
        strategy = self.lab_strategy.determine_approach(lab_components)
        
        print("\nDetermined Strategy:")
        print(json.dumps(strategy, indent=2))
        
        return lab_components, strategy

    def test_evidence_collection(self):
        """Test evidence collection and analysis"""
        print("\nTesting evidence collection and analysis...")
        
        # Process some instructions to collect evidence
        instructions = [
            "Observe and analyze DNS queries to track host activity",
            "Identify HTTP/S communications to correlate user behavior"
        ]
        
        for instruction in instructions:
            self.process_instruction(instruction)
        
        # Analyze the collected evidence
        print("\nAnalyzing collected evidence...")
        analysis = self.evidence_collector.analyze_patterns(self.client)
        
        print("\nEvidence Analysis:")
        print(json.dumps(analysis, indent=2))
        
        return analysis

    def run_test(self):
        """Run a comprehensive test of the system"""
        print("Starting comprehensive test of the lab automation system...")
        
        # Test 1: Lab document parsing
        lab_components, strategy = self.test_lab_document_parsing()
        
        # Test 2: Command processing
        print("\nTesting command processing...")
        if strategy and "sequence" in strategy:
            for i, step in enumerate(strategy.get('sequence', []), 1):
                print(f"\n[{i}/{len(strategy['sequence'])}] Executing: {step}")
                self.process_instruction(step)
        else:
            # Fallback to individual instructions
            instructions = [
                "Identify live hosts on the network",
                "Detect open ports and services on target systems",
                "Observe and analyze DNS queries to track host activity",
                "Identify HTTP/S communications to correlate user behavior"
            ]
            
            for i, instruction in enumerate(instructions, 1):
                print(f"\n[{i}/{len(instructions)}] Testing instruction: {instruction}")
                self.process_instruction(instruction)
        
        # Test 3: Evidence analysis
        analysis = self.test_evidence_collection()
        
        # Test 4: Report generation
        print("\nTesting report generation...")
        report = self.evidence_collector.generate_report(lab_components, self.client)
        
        # Save report to file
        report_path = f"{self.logger.log_dir}/test_lab_report.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\nTest lab report generated: {report_path}")
        
        print(f"\nTest completed. Log file: {self.logger.get_log_file()}")
        print(f"Screenshots saved in: {self.logger.screenshot_dir}")

if __name__ == "__main__":
    test = TestLabAutomation()
    test.run_test()
