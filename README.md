# AI Mock Interview CLI

A  CLI-based AI Mock Interview Platform for AI Mock Interview . Integrated with Google Gemini for AI logic, gTTS for voice output, and SpeechRecognition for voice input.

## Features
- **AI Interviewer**: Simulates a real interviewer using Gemini 1.5 Flash.
- **Voice Interaction**: Talk to the AI and hear it speak back.
- **Grading**: Automtaic feedback and scoring after the interview.
- **Feedback Storage**: Detailed feedback is saved to `feedback/` folder.
- **Transcripts**: Saves full interview logs for review.

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- A Google Cloud Gemini API Key ([Get one here](https://aistudio.google.com/))

### 2. OS-Specific Setup

#### 🐧 Linux (Ubuntu/Debian)
You need system-level audio libraries for the microphone and speakers.
```bash
sudo apt-get update
sudo apt-get install mpg123 portaudio19-dev python3-venv
```

#### 🪟 Windows
Windows users need specific audio wheels.
1. Install [Python](https://www.python.org/downloads/).
2. Open PowerShell or Command Prompt.
3. You might need C++ Build Tools if `pyaudio` fails to compile, but usually the pre-built wheels work.

### 3. Project Setup (All Platforms)

**Create Virtual Environment**:
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

**Install Python Dependencies**:
```bash
pip install -r requirements.txt
```

**Configure API Key**:
1. Copy the example env file:
   ```bash
   # Linux
   cp .env.example .env
   
   # Windows
   copy .env.example .env
   ```
2. Open `.env` and paste your `GEMINI_API_KEY`.

---

## 🚀 Usage

### Interactive Mode (Recommended)
Simply run the app, and use the arrow keys to choose your settings.
```bash
python main.py
```

### Command Line Flags
For power users who want to skip the menu:
```bash
# Standard Product Design Interview (20 mins)
python main.py --interview-type "Product Design" --duration 20

# Quick System Design Check
python main.py --interview-type "System Design" --duration 10 --text-only
```

**Available Types**: `Product Design`, `Engineering`, `System Design`, `Behavioral`, `Strategy`.

---

## 🔧 Troubleshooting

### Common Issues
| Issue | Platform | Solution |
|-------|----------|----------|
| **No Audio Output** | Linux | Install `mpg123`: `sudo apt install mpg123` |
| **Microphone Error** | Linux | Install `portaudio19-dev`. Ensure mic is not muted in Settings. |
| **"Wheel failed to build"** | Windows | Try installing specific binaries: `pip install pipwin` then `pipwin install pyaudio`. |
| **"Quota Exceeded"** | All | The free Gemini API has rate limits. Wait a minute and try again. |

