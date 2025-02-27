import re
from openai import OpenAI
from config import OPENAI_API_KEY

class LabInstructionParser:
    """Parser for full lab instructions to extract goals, tasks, and requirements"""
    
    def __init__(self, openai_client=None):
        self.client = openai_client or OpenAI(api_key=OPENAI_API_KEY)
    
    def parse_lab_document(self, text):
        """Parse full lab document to extract key components"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a cybersecurity lab assistant. 
                    Analyze the provided lab instructions and extract the following components:
                    
                    1. title: The lab title
                    2. objective: The main goal or objective of the lab
                    3. tasks: List of specific tasks to complete
                    4. target: What needs to be identified or found (e.g., specific host, vulnerability)
                    5. approach: The required approach (e.g., passive observation, active scanning)
                    6. deliverables: What needs to be submitted or documented
                    
                    Return the results as a JSON object with these keys. Be concise but comprehensive.
                    """},
                    {"role": "user", "content": f"Lab Instructions:\n\n{text}"}
                ]
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content.strip()
            
            # Simple regex-based JSON extraction (more robust than eval)
            json_match = re.search(r'({[\s\S]*})', content)
            if json_match:
                import json
                try:
                    parsed_data = json.loads(json_match.group(1))
                    return parsed_data
                except json.JSONDecodeError:
                    print("Error parsing JSON from response")
            
            # Fallback to manual extraction if JSON parsing fails
            return self._extract_components_manually(text)
            
        except Exception as e:
            print(f"Error parsing lab document: {e}")
            return self._extract_components_manually(text)
    
    def _extract_components_manually(self, text):
        """Fallback method to extract components using regex patterns"""
        components = {
            "title": "",
            "objective": "",
            "tasks": [],
            "target": "",
            "approach": "",
            "deliverables": []
        }
        
        # Extract title (usually at the beginning, preceded by # or similar)
        title_match = re.search(r'#\s*(.+?)(?=\n|$)', text)
        if title_match:
            components["title"] = title_match.group(1).strip()
        else:
            # Try to find the first line as title
            first_line = text.strip().split('\n')[0]
            if first_line and len(first_line) < 100:  # Reasonable title length
                components["title"] = first_line.strip()
        
        # Extract objective (often contains words like "objective", "goal", "task")
        objective_patterns = [
            r'objective[^\n.]*is to\s+(.+?)(?=\n\n|\.\s|\.$)',
            r'your task[^\n.]*is to\s+(.+?)(?=\n\n|\.\s|\.$)',
            r'goal[^\n.]*is to\s+(.+?)(?=\n\n|\.\s|\.$)'
        ]
        for pattern in objective_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                components["objective"] = match.group(1).strip()
                break
        
        # Extract tasks (often in bullet points or numbered lists)
        task_matches = re.findall(r'[-*•]\s*(.+?)(?=\n|$)', text)
        if task_matches:
            components["tasks"] = [task.strip() for task in task_matches]
        
        # First, try to extract IP addresses directly
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
        ip_matches = re.findall(ip_pattern, text)
        
        # If we found IP addresses, look for target indicators
        if ip_matches:
            # Look for specific target indicators
            target_indicators = ["target", "host", "machine", "server", "computer"]
            for indicator in target_indicators:
                # Look for patterns like "target: 192.168.1.1" or "target host 192.168.1.1"
                indicator_pattern = rf'{indicator}[:\s]+([0-9]{{1,3}}(?:\.[0-9]{{1,3}}){{3}})'
                indicator_match = re.search(indicator_pattern, text, re.IGNORECASE)
                if indicator_match:
                    components["target"] = indicator_match.group(1)
                    break
            
            # If no specific indicator, use the first IP found
            if not components["target"] and ip_matches:
                components["target"] = ip_matches[0]
        
        # If no IP found, try other target patterns
        if not components["target"]:
            target_patterns = [
                r'identify\s+(.+?)(?=\n|\.|,)',
                r'find\s+(.+?)(?=\n|\.|,)',
                r'determine\s+(.+?)(?=\n|\.|,)'
            ]
            for pattern in target_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    components["target"] = match.group(1).strip()
                    break
        
        # Extract approach
        if "passive" in text.lower():
            components["approach"] = "passive"
        elif "active" in text.lower():
            components["approach"] = "active"
        
        # Extract deliverables
        deliverable_section = re.search(r'report|submit|deliverable', text, re.IGNORECASE)
        if deliverable_section:
            section_start = deliverable_section.start()
            section_text = text[section_start:section_start + 500]  # Look at next 500 chars
            deliverable_matches = re.findall(r'[-*•]\s*(.+?)(?=\n|$)', section_text)
            if deliverable_matches:
                components["deliverables"] = [d.strip() for d in deliverable_matches]
        
        return components

class LabStrategy:
    """Determines the strategic approach to completing the lab based on parsed instructions"""
    
    def __init__(self, openai_client=None):
        self.client = openai_client or OpenAI(api_key=OPENAI_API_KEY)
    
    def determine_approach(self, lab_components):
        """Determine the best approach to complete the lab"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a cybersecurity lab strategist.
                    Based on the provided lab components, determine the best approach to complete the lab.
                    
                    Consider:
                    1. What tools and commands would be most appropriate
                    2. The sequence of steps to follow
                    3. What evidence needs to be collected
                    4. How to identify the target
                    
                    Return a JSON object with the following keys:
                    - tools: List of tools that should be used
                    - commands: List of command types that would be useful
                    - sequence: Ordered list of steps to follow
                    - evidence: What evidence should be collected
                    - analysis: How to analyze the evidence to reach the objective
                    """},
                    {"role": "user", "content": f"Lab Components: {lab_components}"}
                ]
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content.strip()
            
            # Simple regex-based JSON extraction
            json_match = re.search(r'({[\s\S]*})', content)
            if json_match:
                import json
                try:
                    strategy = json.loads(json_match.group(1))
                    return strategy
                except json.JSONDecodeError:
                    print("Error parsing JSON from strategy response")
            
            # Return the raw content if JSON parsing fails
            return {"raw_strategy": content}
            
        except Exception as e:
            print(f"Error determining lab strategy: {e}")
            return {
                "tools": [],
                "commands": [],
                "sequence": [],
                "evidence": [],
                "analysis": "Error generating strategy"
            }

class EvidenceCollector:
    """Collects and analyzes evidence during lab execution"""
    
    def __init__(self):
        self.dns_queries = []
        self.http_requests = []
        self.network_traffic = []
        self.patterns = []
        self.findings = {}
    
    def add_dns_query(self, query, source):
        """Add a DNS query to the evidence"""
        self.dns_queries.append({"query": query, "source": source, "timestamp": self._get_timestamp()})
    
    def add_http_request(self, source, host, uri):
        """Add an HTTP request to the evidence"""
        self.http_requests.append({
            "source": source,
            "host": host,
            "uri": uri,
            "timestamp": self._get_timestamp()
        })
    
    def add_network_traffic(self, source, destination, protocol, info):
        """Add general network traffic to the evidence"""
        self.network_traffic.append({
            "source": source,
            "destination": destination,
            "protocol": protocol,
            "info": info,
            "timestamp": self._get_timestamp()
        })
    
    def analyze_patterns(self, openai_client):
        """Analyze collected evidence for patterns"""
        if not (self.dns_queries or self.http_requests or self.network_traffic):
            return "No evidence collected yet"
        
        try:
            # Prepare evidence summary
            evidence_summary = {
                "dns_queries": self.dns_queries,
                "http_requests": self.http_requests,
                "network_traffic": self.network_traffic
            }
            
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a cybersecurity evidence analyst.
                    Analyze the provided network evidence and identify:
                    
                    1. Patterns in the traffic
                    2. Suspicious or unusual activity
                    3. Correlations between different types of traffic
                    4. Potential targets based on the evidence
                    
                    Return your analysis as a JSON object with these keys:
                    - patterns: List of identified patterns
                    - suspicious_activity: List of suspicious activities
                    - correlations: List of correlations between different traffic types
                    - potential_targets: List of potential targets with reasoning
                    """},
                    {"role": "user", "content": f"Network Evidence: {evidence_summary}"}
                ]
            )
            
            # Extract analysis from response
            content = response.choices[0].message.content.strip()
            
            # Simple regex-based JSON extraction
            json_match = re.search(r'({[\s\S]*})', content)
            if json_match:
                import json
                try:
                    analysis = json.loads(json_match.group(1))
                    self.patterns = analysis.get("patterns", [])
                    self.findings = analysis
                    return analysis
                except json.JSONDecodeError:
                    print("Error parsing JSON from analysis response")
            
            # Return the raw content if JSON parsing fails
            return {"raw_analysis": content}
            
        except Exception as e:
            print(f"Error analyzing evidence: {e}")
            return {"error": str(e)}
    
    def generate_report(self, lab_components, openai_client):
        """Generate a report based on collected evidence and lab requirements"""
        if not self.findings:
            return "No analysis performed yet"
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a cybersecurity report writer.
                    Based on the provided lab components and evidence analysis, generate a comprehensive lab report.
                    
                    The report should include:
                    1. Executive summary
                    2. Methodology
                    3. Findings
                    4. Evidence
                    5. Conclusion
                    
                    Format the report in Markdown.
                    """},
                    {"role": "user", "content": f"Lab Components: {lab_components}\nEvidence Analysis: {self.findings}"}
                ]
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return f"Error generating report: {e}"
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
