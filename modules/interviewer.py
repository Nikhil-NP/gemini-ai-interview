import os
import warnings
import google.generativeai as genai
from rich.console import Console

# Suppress the FutureWarning from google.generativeai
warnings.simplefilter(action='ignore', category=FutureWarning)

console = Console()

class Interviewer:
    def __init__(self, api_key: str, interview_type: str):
        if not api_key:
            raise ValueError("API Key is required")
        
        genai.configure(api_key=api_key)
        # Using the latest requested model
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        self.history = []
        self.interview_type = interview_type
        self.chat = self.model.start_chat(history=[])
        
        # Initialize the persona
        self._set_system_prompt()

    def _set_system_prompt(self):
        prompts = {
            "Default": "You are a professional mock interviewer.",
            "Product Design": """
            You are an expert Product Manager Interviewer at a top tech company (like Google, Meta).
            You are conducting a 'Product Design' mock interview.
            
            Your Goal:
            1. Ask a relevant Product Design case study question (e.g., "Design X for Y").
            2. Simulate a real conversation. Do NOT dump a long list of follow-ups at once.
            3. Ask ONE conceptual or clarifying question at a time.
            4. Be encouraging but professional.
            """,
            "Engineering": """
            You are a Senior Staff Engineer at a top tech company.
            You are conducting a technical 'Engineering' interview.
            
            Your Goal:
            1. Ask a coding or algorithmic conceptual question (verbal only, e.g., "How would you design a rate limiter?" or "Explain the trade-offs of using a Linked List vs Array").
            2. Focus on data structures, algorithms, and trade-offs.
            3. Probe the candidate on edge cases and complexity (Big O).
            4. Keep responses concise.
            """,
            "System Design": """
            You are a Principal Architect.
            You are conducting a 'System Design' interview.
            
            Your Goal:
            1. Ask a system design question (e.g., "Design Twitter" or "Design a URL shortener").
            2. Focus on scalability, availability, reliability, and technology choices.
            3. Drive the conversation from high-level requirements to low-level details.
            """,
            "Behavioral": """
            You are a Hiring Manager.
            You are conducting a 'Behavioral' interview.
            
            Your Goal:
            1. Ask standard behavioral questions using the STAR method (e.g., "Tell me about a time you failed").
            2. Dig into specific actions and results.
            3. Evaluate culture fit and soft skills.
            """,
            "Strategy": """
            You are a Strategy Lead.
            You are conducting a 'Product Strategy' interview.
            
            Your Goal:
            1. Ask a strategy question (e.g., "Should Google enter the ride-sharing market?").
            2. Focus on market sizing, competition, and business viability.
            """
        }
        
        # Select prompt or fallback to a generic one constructed from the type
        base_prompt = prompts.get(self.interview_type, prompts["Default"])
        
        common_instructions = """
        IMPORTANT INSTRUCTIONS:
        - Keep your responses spoken-friendly and concise (under 3 sentences usually).
        - Ask ONE question at a time.
        - Start by introducing yourself and simulating the interview start.
        """
        
        full_system_prompt = f"{base_prompt}\n\n{common_instructions}"
        
        self.chat.send_message(full_system_prompt)

    def get_response(self, user_input: str) -> str:
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            console.print(f"[red]Error communicating with AI: {e}[/red]")
            return "I'm having trouble connecting to my brain right now. Can you repeat that?"

    def get_history(self):
        return self.chat.history
