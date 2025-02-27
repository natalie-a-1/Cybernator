from openai import OpenAI
from vm import VMConnection
from rdp import RDPConnection
from logger import Logger
from config import OPENAI_API_KEY
from agents import CommandProcessor
from lab_parser import LabInstructionParser, LabStrategy, EvidenceCollector
import textwrap
import json
import os

class LabAutomation:
    def __init__(self, use_rdp=True):
        self.use_rdp = use_rdp
        self.vm = VMConnection() if not use_rdp else RDPConnection()
        self.logger = Logger()
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.command_processor = CommandProcessor(self.client)
        self.lab_parser = LabInstructionParser(self.client)
        self.lab_strategy = LabStrategy(self.client)
        self.evidence_collector = EvidenceCollector()
        self.lab_components = None
        self.strategy = None

    def get_output_explanation(self, command, output):
        """Generate explanation for command output"""
        try:
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

    def process_lab_document(self, lab_text):
        """Process a full lab document to extract components and determine strategy"""
        print("\nAnalyzing lab document...")
        self.lab_components = self.lab_parser.parse_lab_document(lab_text)
        
        print("\nLab Components:")
        print(f"Title: {self.lab_components.get('title', 'Unknown')}")
        print(f"Objective: {self.lab_components.get('objective', 'Unknown')}")
        print(f"Target: {self.lab_components.get('target', 'Unknown')}")
        print(f"Approach: {self.lab_components.get('approach', 'Unknown')}")
        
        print("\nDetermining lab strategy...")
        self.strategy = self.lab_strategy.determine_approach(self.lab_components)
        
        print("\nRecommended Strategy:")
        if "tools" in self.strategy:
            print(f"Tools: {', '.join(self.strategy.get('tools', []))}")
        if "commands" in self.strategy:
            print(f"Commands: {', '.join(self.strategy.get('commands', []))}")
        if "sequence" in self.strategy:
            print("\nRecommended Sequence:")
            for i, step in enumerate(self.strategy.get('sequence', []), 1):
                print(f"{i}. {step}")
        
        return self.lab_components, self.strategy

    def execute_lab_instruction(self, instruction):
        """Process a single lab instruction using the multi-agent system"""
        print(f"\nProcessing instruction: {instruction}")
        
        # Use the command processor to generate a customized command and explanation
        command, command_type, selection_explanation = self.command_processor.process_instruction(instruction)
        
        if not command:
            print(f"Could not determine appropriate command for: {instruction}")
            return None, None
            
        print(f"Generated command: {command}")
        print(f"Command type: {command_type}")
        
        # Execute command on VM
        output, error = self.vm.execute(command)
        
        # Process output for evidence collection
        if output and not error:
            self._process_output_for_evidence(command, command_type, output)
        
        # Generate explanation for the output
        if output:
            output_explanation = self.get_output_explanation(command, output)
            # Combine the selection explanation and output explanation
            full_explanation = f"{selection_explanation}\n\nOutput Analysis:\n{output_explanation}"
        else:
            full_explanation = selection_explanation
        
        # Log the step
        self.logger.log_step(command, output, error, full_explanation)
        
        return output, error
    
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

    def analyze_evidence(self):
        """Analyze collected evidence"""
        print("\nAnalyzing collected evidence...")
        analysis = self.evidence_collector.analyze_patterns(self.client)
        
        print("\nEvidence Analysis:")
        if isinstance(analysis, dict):
            if "patterns" in analysis:
                print("\nIdentified Patterns:")
                for pattern in analysis.get("patterns", []):
                    print(f"- {pattern}")
            
            if "potential_targets" in analysis:
                print("\nPotential Targets:")
                for target in analysis.get("potential_targets", []):
                    print(f"- {target}")
        else:
            print(analysis)
        
        return analysis

    def generate_report(self):
        """Generate a report based on lab components and evidence analysis"""
        if not self.lab_components:
            return "No lab components available. Please process a lab document first."
        
        print("\nGenerating lab report...")
        report = self.evidence_collector.generate_report(self.lab_components, self.client)
        
        # Save report to file
        report_path = f"{self.logger.log_dir}/lab_report.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\nLab report generated: {report_path}")
        return report

    def run_lab(self):
        """Main lab execution flow"""
        try:
            print("Connecting to Kali VM...")
            # Connect to VM with timeout
            if not self.vm.connect():
                print("Failed to connect to VM. Please check:")
                print("- VM is running and accessible")
                print("- SSH service is running on the VM")
                print("- IP address and port are correct")
                print("- Username and password are correct")
                return

            print("Connected to VM successfully.")
            print("\nEnter lab instructions (full lab document or individual instructions)")
            print("You can paste a complete lab document or enter instructions one by one.")
            print("Type 'done' on a new line when finished:")
            
            lines = []
            while True:
                try:
                    line = input("> ").strip()
                    if line.lower() == 'done':
                        break
                    lines.append(line)
                except KeyboardInterrupt:
                    print("\nInput interrupted. Finishing input collection.")
                    break
            
            if not lines:
                print("No instructions provided. Exiting.")
                return

            # Join all lines into a single text
            full_text = "\n".join(lines)
            
            # Check if this is a full lab document or individual instructions
            if len(lines) > 5 and ("lab" in full_text.lower() or "#" in full_text):
                # Process as a full lab document
                self.process_lab_document(full_text)
                
                if self.strategy and "sequence" in self.strategy:
                    # Execute the recommended sequence of steps
                    for i, step in enumerate(self.strategy.get('sequence', []), 1):
                        print(f"\n[{i}/{len(self.strategy['sequence'])}] Executing: {step}")
                        
                        # Convert the step into a command instruction
                        output, error = self.execute_lab_instruction(step)
                        
                        if error:
                            print(f"Error occurred: {error}")
                        elif output:
                            print("Command executed successfully.")
                            print("Screenshot captured.")
                        else:
                            print("Command executed but returned no output.")
                    
                    # Analyze the collected evidence
                    self.analyze_evidence()
                    
                    # Generate a report
                    self.generate_report()
                else:
                    print("No strategy sequence available. Processing as individual instructions.")
                    # Process each line as an individual instruction
                    for i, instruction in enumerate(lines, 1):
                        if instruction.strip():
                            print(f"\n[{i}/{len(lines)}] Processing: {instruction}")
                            output, error = self.execute_lab_instruction(instruction)
                            
                            if error:
                                print(f"Error occurred: {error}")
                            elif output:
                                print("Command executed successfully.")
                                print("Screenshot captured.")
                            else:
                                print("Command executed but returned no output.")
            else:
                # Process as individual instructions
                for i, instruction in enumerate(lines, 1):
                    if instruction.strip():
                        print(f"\n[{i}/{len(lines)}] Processing: {instruction}")
                        output, error = self.execute_lab_instruction(instruction)
                        
                        if error:
                            print(f"Error occurred: {error}")
                        elif output:
                            print("Command executed successfully.")
                            print("Screenshot captured.")
                        else:
                            print("Command executed but returned no output.")

            print(f"\nLab execution completed!")
            print(f"Log file: {self.logger.get_log_file()}")
            print(f"Screenshots saved in: {self.logger.screenshot_dir}")

        except KeyboardInterrupt:
            print("\nLab execution interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("Closing VM connection...")
            self.vm.close()

