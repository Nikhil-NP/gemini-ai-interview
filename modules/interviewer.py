import os
import warnings
import google.generativeai as genai
from rich.console import Console 

# Suppress the Warning from google.generativeai
warnings.simplefilter(action='ignore', category=FutureWarning)

console = Console()

class Interviewer:
    def __init__(self, api_key: str, interview_type: str):
        if not api_key:
            raise ValueError("API Key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.history = []
        self.interview_type = interview_type
        self.chat = self.model.start_chat(history=[])
        
        # Initialize the persona
        self._set_system_prompt()

    def _set_system_prompt(self):
        prompts = {
            "Default": "You are a professional mock interviewer.",
            "Product Design": """
            You are an expert Product Manager Interviewer at a top tech company.
            Conduct a 'Product Design' interview.
            
            Goal:
            - Ask a case study question (e.g., "Design X for Y").
            - DRILL DOWN. Do not let the candidate stay high level. Ask "Why?" and "How exactly?".
            - Be conversational. React to what they say.
            """,
            "Engineering": """
            You are a Supportive Engineering Interviewer.
            Conduct a technical 'Engineering' interview.
            
            Goal:
            - Focus STRICTLY on Algorithms and Data Structures (Arrays, Strings, HashMaps).
            - DO NOT ask System Design questions.
            - **VERBAL ONLY**: Never ask the candidate to write code. Ask for their "logic", "approach", or "pseudocode description".
            - START EASY. 
                1. Ice Breaker: "What is your favorite language?" or "Tell me about a project."
                2. Warm Up: A simple array/string manipulation question.
                3. Challenge: Only if they do well, move to optimization.
            - Be encouraging and helpful.
            """,
            "System Design": """
            You are a Principal Architect.
            Conduct a 'System Design' interview.
            
            Goal:
            - Ask a system design question.
            - Focus on scalability and bottlenecks.
            - Ask specific questions about components (e.g., "How would you shard the database?").
            """,
            "Behavioral": """
            You are a Hiring Manager.
            Conduct a 'Behavioral' interview.
            
            Goal:
            - Ask STAR method questions.
            - Dig into their specific contribution. "What did YOU do vs the team?".
            """,
            "Strategy": """
            You are a Strategy Lead.
            Conduct a 'Product Strategy' interview.
            
            Goal:
            - Ask a strategy question.
            - Focus on market analysis and competitive advantage.
            """
        }
        
        # Select prompt or fallback to a generic one constructed from the type
        base_prompt = prompts.get(self.interview_type, prompts["Default"])
        
        common_instructions = """
        CRITICAL RULES:
        1. **DIFFICULTY CURVE**:
           - **Start**: Ask a simple "Ice Breaker" technical/role-related question (e.g., "What's your favorite sorting algorithm?" or "Tell me about yourself").
           - **Middle**: Move to a standard conceptual question.
           - **End**: Ramp up to a challenging scenario or edge case.
        2. ASK ONLY ONE QUESTION AT A TIME. Never double-barrel questions.
        3. Keep responses SHORT (under 3 sentences). This is a spoken conversation.
        4. Do NOT provide lists of follow-ups. Wait for the user to answer.
        5. If the user is vague, ask for clarification before moving on.
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
