import os
import json
from datetime import datetime

def save_transcript(transcript: list, interview_type: str):
    """Saves the conversation history to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transcripts/{interview_type}_{timestamp}.json"
    
    os.makedirs("transcripts", exist_ok=True)
    
    serialized_transcript = []
    for msg in transcript:
        role = msg.role
        try:
            content = msg.parts[0].text
        except:
            content = "[Non-text content]"
        serialized_transcript.append({"role": role, "content": content})
    
    data = {
        "timestamp": timestamp,
        "type": interview_type,
        "transcript": serialized_transcript
    }
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    return filename

def format_transcript_string(history):
    """Formats the chat history into a string for grading."""
    text = ""
    for msg in history:
        role = msg.role  # 'user' or 'model'
        content = msg.parts[0].text
        text += f"{role.upper()}: {content}\n"
    return text
