import typer
import os
import time
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv

from modules.interviewer import Interviewer
from modules.audio import AudioManager
from modules.grader import Grader
from modules.utils import save_transcript, format_transcript_string

# Load env variables
load_dotenv()

app = typer.Typer()
console = Console()

@app.command()
def start(
    interview_type: Optional[str] = typer.Option(None, help="Type of interview"),
    duration: Optional[int] = typer.Option(None, help="Duration in minutes"),
    text_only: bool = typer.Option(False, help="Disable voice mode (text only)")
):
    """
    Start the AI Mock Interview.
    """
    # Interactive Mode if args are missing
    if interview_type is None:
        import questionary
        interview_type = questionary.select(
            "What type of interview would you like to practice?",
            choices=[
                "Product Design",
                "Engineering",
                "System Design",
                "Behavioral",
                "Strategy"
            ]
        ).ask()
        
    if duration is None:
        import questionary
        duration = int(questionary.text("Duration in minutes?", default="20").ask())

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]Error: GEMINI_API_KEY not found in environment variables.[/red]")
        console.print("Please create a .env file with your API key.")
        return

    console.print(Panel(f"[bold green]Starting {interview_type} Interview[/bold green]\nDuration: {duration} mins", title="AI Mock Interview"))

    # Initialize Modules
    try:
        interviewer = Interviewer(api_key, interview_type)
        audio_manager = AudioManager() if not text_only else None
    except Exception as e:
        console.print(f"[red]Initialization Error: {e}[/red]")
        return

    console.print("[bold]Interview Started. Press Ctrl+C to stop.[/bold]\n")

    greeting = "Hello! I'm your interviewer today. Are you ready to begin the case study?"
    console.print(f"[bold blue]AI:[/bold blue] {greeting}")
    
    if audio_manager:
        audio_manager.speak(greeting)

    start_time = time.time()

    try:
        while True:
            elapsed = (time.time() - start_time) / 60
            remaining = duration - elapsed
            
            if remaining <= 0:
                console.print("\n[bold red]Time is up![/bold red]")
                break

            mins = int(remaining)
            secs = int((remaining - mins) * 60)
            
            time_color = "green"
            if remaining < 5: time_color = "yellow"
            if remaining < 2: time_color = "red"
            
            console.rule(f"[{time_color}]Time Remaining: {mins:02d}:{secs:02d}[/{time_color}]", style=time_color)

            if audio_manager:
                user_input = audio_manager.listen()
                if not user_input:
                     continue
            else:
                user_input = console.input("[bold yellow]You:[/bold yellow] ")

            if user_input.lower() in ["exit", "quit", "stop"]:
                break
            
            # AI Turn
            if not text_only:
                 # Re-print user input for log visibility if it came from STT
                 # (Already printed in audio.listen but consistency helps)
                 pass

            ai_response = interviewer.get_response(user_input)
            console.print(f"[bold blue]AI:[/bold blue] {ai_response}")
            
            if audio_manager:
                audio_manager.speak(ai_response)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interview Stopped User.[/yellow]")

    # Grading Phase
    console.print("\n[bold magenta]Interview Complete. Generating Feedback...[/bold magenta]")
    
    history = interviewer.get_history()
    transcript_str = format_transcript_string(history)
    save_path = save_transcript(history, interview_type)
    
    grader = Grader(api_key)
    result = grader.grade_interview(transcript_str, interview_type)
    
    console.print(Panel(Markdown(result), title="Interview Feedback"))
    console.print(f"Transcript saved to: {save_path}")

if __name__ == "__main__":
    app()
