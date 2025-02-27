from openai import OpenAI
from config import COMMAND_TEMPLATES, DEFAULT_PARAMS
import json

class ContextAnalyzer:
    """Agent responsible for analyzing lab instructions and extracting context"""
    
    def __init__(self, client):
        self.client = client
    
    def analyze(self, instruction):
        """Extract key parameters and context from the instruction"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a cybersecurity expert. 
                    Analyze the lab instruction and extract key parameters needed for command generation:
                    - target: IP addresses or ranges to scan (e.g., "192.168.1.100" or "192.168.1.0/24")
                    - ports: specific ports or port ranges to examine
                    - protocols: specific protocols mentioned (e.g., DNS, HTTP)
                    - techniques: specific techniques or approaches mentioned
                    - tools: specific tools mentioned (e.g., nmap, tshark)
                    
                    Return a JSON object with these parameters. If a parameter is not specified in the instruction,
                    use null as the value. Be specific and extract only what's explicitly mentioned or strongly implied.
                    """},
                    {"role": "user", "content": f"Instruction: {instruction}"}
                ]
            )
            
            context_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            try:
                # Find JSON content if it's embedded in text
                if '{' in context_text and '}' in context_text:
                    start = context_text.find('{')
                    end = context_text.rfind('}') + 1
                    json_str = context_text[start:end]
                    context = json.loads(json_str)
                else:
                    context = json.loads(context_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                context = {
                    "target": None,
                    "ports": None,
                    "protocols": None,
                    "techniques": None,
                    "tools": None
                }
            
            return context
            
        except Exception as e:
            print(f"Error in context analysis: {e}")
            return {
                "target": None,
                "ports": None,
                "protocols": None,
                "techniques": None,
                "tools": None
            }


class CommandGenerator:
    """Agent responsible for selecting and customizing commands"""
    
    def __init__(self, client):
        self.client = client
    
    def select_command_type(self, instruction, context):
        """Select the most appropriate command type from available templates"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are a cybersecurity expert. 
                    Given a lab instruction and context, select the most appropriate command type from the available templates.
                    Available command types: {list(COMMAND_TEMPLATES.keys())}
                    
                    Return only the command type name, nothing else. Do not include quotes or any other characters."""},
                    {"role": "user", "content": f"Instruction: {instruction}\nContext: {context}"}
                ]
            )
            
            command_type = response.choices[0].message.content.strip()
            
            # Remove any quotes or extra characters that might be in the response
            command_type = command_type.replace("'", "").replace('"', "").strip()
            
            # Verify the command type exists in templates
            if command_type not in COMMAND_TEMPLATES:
                print(f"Warning: Selected command type '{command_type}' not found in templates.")
                # Try to find a close match
                for template_key in COMMAND_TEMPLATES.keys():
                    if command_type.lower() in template_key.lower():
                        print(f"Using similar command type: {template_key}")
                        return template_key
                return None
            
            return command_type
            
        except Exception as e:
            print(f"Error in command type selection: {e}")
            return None
    
    def customize_command(self, command_type, context):
        """Customize the selected command template with context-specific parameters"""
        if command_type not in COMMAND_TEMPLATES:
            return None
            
        template = COMMAND_TEMPLATES[command_type]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are a command customization expert.
                    Given a command template and context parameters, customize the command by filling in the placeholders.
                    
                    Command template: {template}
                    Default parameters: {DEFAULT_PARAMS}
                    
                    For each placeholder in the template, determine the appropriate value based on the context.
                    If the context doesn't specify a value, use the default.
                    
                    Return a JSON object where keys are parameter names and values are the customized values.
                    Include only parameters that are in the template."""},
                    {"role": "user", "content": f"Context: {context}"}
                ]
            )
            
            params_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            try:
                # Find JSON content if it's embedded in text
                if '{' in params_text and '}' in params_text:
                    start = params_text.find('{')
                    end = params_text.rfind('}') + 1
                    json_str = params_text[start:end]
                    params = json.loads(json_str)
                else:
                    params = json.loads(params_text)
            except json.JSONDecodeError:
                # Fallback to default parameters
                params = {}
            
            # Fill in any missing parameters with defaults
            for key in DEFAULT_PARAMS:
                if key not in params:
                    params[key] = DEFAULT_PARAMS[key]
            
            # Format the command with the parameters
            try:
                command = template.format(**params)
                return command, params
            except KeyError as e:
                print(f"Missing parameter in template: {e}")
                return None, None
                
        except Exception as e:
            print(f"Error in command customization: {e}")
            return None, None


class ExplanationGenerator:
    """Agent responsible for generating explanations for command selection and customization"""
    
    def __init__(self, client):
        self.client = client
    
    def explain_command_selection(self, instruction, command_type, command, context, params):
        """Explain why this command was selected and how it was customized"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a cybersecurity strategy expert.
                    Explain why this specific command was chosen for the given instruction and how it was customized.
                    
                    Your explanation should include:
                    1. Why this command type was selected for the specific lab instruction
                    2. How the command parameters were customized based on the context
                    3. What specific aspects of the lab task this command addresses
                    
                    Focus on the strategic decision-making process and how this command helps accomplish the lab objective.
                    Start with "I chose to use this command because..." and be specific about the reasoning."""},
                    {"role": "user", "content": f"Instruction: {instruction}\nCommand Type: {command_type}\nCommand: {command}\nContext: {context}\nParameters: {params}"}
                ]
            )
            
            explanation = response.choices[0].message.content.strip()
            return explanation
            
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return "Explanation unavailable due to an error."


class CommandProcessor:
    """Main class that coordinates the agents to process lab instructions"""
    
    def __init__(self, openai_client):
        self.client = openai_client
        self.context_analyzer = ContextAnalyzer(self.client)
        self.command_generator = CommandGenerator(self.client)
        self.explanation_generator = ExplanationGenerator(self.client)
    
    def process_instruction(self, instruction):
        """Process a lab instruction and generate an appropriate command with explanation"""
        # Step 1: Analyze the instruction to extract context
        context = self.context_analyzer.analyze(instruction)
        print(f"Extracted context: {context}")
        
        # Step 2: Select the appropriate command type
        command_type = self.command_generator.select_command_type(instruction, context)
        if not command_type:
            return None, None, "Could not determine appropriate command type."
        print(f"Selected command type: {command_type}")
        
        # Step 3: Customize the command with context-specific parameters
        command, params = self.command_generator.customize_command(command_type, context)
        if not command:
            return None, None, "Could not customize command with provided context."
        print(f"Customized command: {command}")
        
        # Step 4: Generate an explanation for the command selection and customization
        explanation = self.explanation_generator.explain_command_selection(
            instruction, command_type, command, context, params
        )
        
        return command, command_type, explanation
