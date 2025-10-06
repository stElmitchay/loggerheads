# Daily Activity Tracker

Automatically track your work and get AI-generated daily summaries. Built for macOS.

## 🚀 Installation

### 1. Install Dependencies

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# Install Tesseract OCR
brew install tesseract
```

### 2. Clone and Install Package

```bash
git clone https://github.com/yourcompany/daily-tracker.git
cd daily-tracker
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

**Note:** The `.env` file is gitignored, so your webhook stays private!

## ▶️ Usage

```bash
# Start the tracker
daily-tracker

# Or explicitly
daily-tracker start

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

Press `Ctrl+C` to stop and generate summary immediately.

## 🔧 Updates

```bash
# Update to latest version
pip install --upgrade git+https://github.com/yourcompany/daily-tracker.git
```

## 📊 Summary Format

Daily summary posted to Discord:

```
✅ What I Worked on Today:
  • AI-analyzed tasks from your screenshots

🏁 What I Completed:
  • Tasks marked as finished/deployed

📰 What's the latest in the Solana Ecosystem:
  • Solana news (if captured from Twitter)

⚠️ Issues / Blockers:
  • Problems encountered

🔜 Focus for Tomorrow:
  • AI recommendations (skipped Fridays)
```

## 🔒 Privacy

- 100% local processing (Ollama runs offline)
- All screenshots deleted after summary
- Database wiped clean daily
- Only summary sent to Discord

## 🆘 Troubleshooting

**"Could not connect to Ollama"**
```bash
ollama serve
curl http://localhost:11434/api/tags
```

**"Tesseract not found"**
```bash
brew install tesseract
tesseract --version
```

**Screen recording permissions**
- macOS: System Preferences → Privacy → Screen Recording
- Enable for Terminal or your app

**Summary quality issues**
- Try different model: `OLLAMA_MODEL = "mistral"`
- Increase screenshot interval if too much data
