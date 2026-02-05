# AI Mock Interview CLI

A  CLI-based AI Mock Interview Platform for AI Mock Interview . Integrated with Google Gemini for AI logic, gTTS for voice output, and SpeechRecognition for voice input.

## Features
- **AI Interviewer**: Simulates a real PM interviewer using Gemini 1.5 Flash.
- **Voice Interaction**: Talk to the AI and hear it speak back.
- **Grading**: Automtaic feedback and scoring after the interview.
- **Transcripts**: Saves full interview logs for review.

## Setup

1. **Install System Dependencies** (Linux):
   You need `mpg123` for audio playback and `portaudio` for microphone access.
   ```bash
   sudo apt-get install mpg123 portaudio19-dev python3-venv
   ```

2. **Setup Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   pip install -r requirements.txt
   ```
   
   **Windows Users**:
   - `python -m pip install playsound==1.2.2` should handle audio.
   - If you get microphone errors, you may need to install standard PyAudio wheel for Windows: `pip install pipwin && pipwin install pyaudio`.

3. **API Key**:
   - Get a free API key from [Google AI Studio](https://aistudio.google.com/).
   - Copy `.env.example` to `.env` and paste your key.
   ```bash
   cp .env.example .env
   # Edit .env with your key
   ```

## Usage

**Start the Interview**:
```bash
# Make sure venv is active
python main.py
```

**Options**:
- `--interview-type`: Change the interview style. supported:
    - `"Product Design"` (Default)
    - `"Engineering"`
    - `"System Design"`
    - `"Behavioral"`
    - `"Strategy"`
- `--text-only`: Disable voice mode (useful if you have no mic setup).
- `--duration`: Set interview length.

Example:
```bash
python main.py --interview-type "Behavioral" --duration 10
```

## Troubleshooting
- **No Audio?**: Ensure `mpg123` is installed (`sudo apt install mpg123`).
- **Microphone Error?**: Ensure `portaudio19-dev` is installed and your mic is unmuted.
