import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

console = Console()

class Grader:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')

    def grade_interview(self, transcript: str, interview_type: str):
        prompt = f"""
        You are a Senior Hiring Manager evaluating a candidate's mock interview.
        
        Interview Type: {interview_type}
        
        Transcript:
        {transcript}
        
        Please provide a structured evaluation:
        1. **Strengths**: What did the candidate do well?
        2. **Areas for Improvement**: Specific actionable advice.
        3. **Technical/Role Fit**: How well did they demonstrate the required skills for a '{interview_type}' role?
        4. **Communication**: Clarity and pacing.
        5. **Overall Score**: 1-10.
        
        Format the output in Markdown.
        """
        
        try:
            console.print("[bold yellow]Generating Feedback...[/bold yellow]")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating grade: {e}"
