import os
import platform
import speech_recognition as sr
from gtts import gTTS
from rich.console import Console
import tempfile
import time
from modules.alsa_error import no_alsa_err

console = Console()

class AudioManager:
    def __init__(self):
        with no_alsa_err():
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        
        # Adjust for ambient noise once at startup
        with self.microphone as source:
            console.print("[dim]Calibrating microphone...[/dim]")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def speak(self, text: str):
        """Converts text to speech and plays it."""
        if not text:
            return
            
        try:
            tts = gTTS(text=text, lang='en')
            # Create a localized temp file
            fd, path = tempfile.mkstemp(suffix=".mp3")
            try:
                os.close(fd)
                tts.save(path)
                
                if platform.system() == "Windows":
                    from playsound import playsound
                    playsound(path)
                else:
                    ret = os.system(f"mpg123 -q {path}")
                    if ret != 0:
                        console.print("[red]Error playing audio. Is mpg123 installed?[/red]")
            finally:
                if os.path.exists(path):
                    os.remove(path)
        except Exception as e:
            console.print(f"[red]TTS Error: {e}[/red]")

    def listen(self) -> str:
        """Listens to microphone input and converts to text."""
        with self.microphone as source:
            console.print("[green]Listening...[/green]")
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                console.print("[dim]Processing...[/dim]")
                text = self.recognizer.recognize_google(audio)
                console.print(f"[cyan]You said: {text}[/cyan]")
                return text
            except sr.WaitTimeoutError:
                console.print("[yellow]No speech detected.[/yellow]")
                return ""
            except sr.UnknownValueError:
                console.print("[red]Could not understand audio.[/red]")
                return ""
            except sr.RequestError as e:
                console.print(f"[red]STT Service Error: {e}[/red]")
                return ""
