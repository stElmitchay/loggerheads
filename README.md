# Daily Activity Tracker

Automatically track your work and get AI-generated daily summaries at the end of the work day.

## 🚀 Installation

### 1. Install Dependencies

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# Install Tesseract OCR
brew install tesseract
```

### 2. Clone the repo and Install Package

```bash
git clone https://github.com/stElmitchay/loggerheads
cd loggerheads
pip install -e .
```

### 3. Configure

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Discord webhook
nano .env
```

Your `.env` file should contain:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url-here
SEND_TO_DISCORD=true
```

**Note:** The discord webhook is to get your daily log sent directly to the daily logs chat on discord.

## ▶️ Usage

```bash
# Or explicitly
daily-tracker start 
- To start tracking

# Show version
daily-tracker version

# Show help
daily-tracker help
```

The app will:
- Start tracking at 9:30am (Mon-Fri)
- Take screenshots every 10 seconds
- Generate AI summary at 4:30pm
- Post summary to Discord
- Delete all data automatically

### ⌨️ Controls

While the tracker is running:
- **Press `P`** - Pause tracking (for breaks, personal time, etc.)
- **Press `R`** - Resume tracking
- **Press `Ctrl+C`** - Stop and generate summary immediately

When paused, no screenshots are captured and no activity is tracked. Perfect for lunch breaks or watching movies!

## 🔧 Updates

```bash
# Update to latest version
pip install --upgrade git+https://github.com/yourcompany/daily-tracker.git
```

## 🔒 Privacy

- 100% local processing (Ollama runs offline)
- All screenshots deleted after summary
- Database wiped clean daily
- Only summary sent to Discord


**Screen recording permissions**
- macOS: System Preferences → Privacy → Screen Recording
- Enable for Terminal or your app

**Summary quality issues**
- Try different model: `OLLAMA_MODEL = "mistral"`
- Increase screenshot interval if too much data
