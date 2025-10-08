# Loggerheads

Automatically track your work and get AI-generated daily summaries focused on Solana ecosystem activities. Perfect for Solana developers, researchers, and professionals who want intelligent work logging that understands your role and filters out personal activities.

## ✨ Features

- 🤖 **AI-Powered Summarization** - Uses local Ollama LLM to analyze your workday
- 🎯 **Context-Aware Filtering** - Configurable work categorization based on your role
- ⏸️ **Pause/Resume Controls** - Easy break management
- 🔄 **Auto-Start on Boot** - Set it and forget it
- 🔒 **Privacy First** - 100% local processing, auto-cleanup after summary
- 💬 **Discord Integration** - Daily summaries posted to your preferred discord channel

## 🚀 Installation

### 1. Install Dependencies

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# Install Tesseract OCR
brew install tesseract
```

### 2. Clone and Install

```bash
git clone https://github.com/stElmitchay/loggerheads
cd loggerheads
pip3 install -e .
```

### 3. Configure Discord (Optional)

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

**Note:** The Discord webhook sends your daily log directly to your team's daily logs chat. You can change `SEND_TO_DISCORD=false` if you don't want logs to be sent directly.

### 4. First-Time Setup

Configure what counts as "work" for you:

```bash
loggerheads setup
```

This interactive wizard will ask about:
- Your role (e.g., "Solana Developer", "Web3 Designer")
- Your industry
- Custom app categorization (e.g., WhatsApp = work for social media managers)
- Work-related keywords

## ▶️ Usage

### Basic Commands

```bash
# Start tracking
loggerheads start

# Configure work context
loggerheads setup

# View current configuration
loggerheads config

# Install auto-start on boot
loggerheads install

# Remove auto-start
loggerheads uninstall

# Check auto-start status
loggerheads status

# Show version
loggerheads version

# Show help
loggerheads help
```

### How It Works

The app will:
- ✅ Start tracking at **9:30 AM** (Mon-Fri)
- 🤖 Generate AI summary at **4:30 PM**
- 💬 Post summary to Discord
- 🗑️ Delete all data automatically
- 🔄 Repeat next workday

### ⌨️ Controls

While the tracker is running:
- **Press `P`** - Pause tracking (for breaks, personal time, etc.)
- **Press `R`** - Resume tracking
- **Press `Ctrl+C`** - Stop and generate summary immediately

When paused, no screenshots are captured and no activity is tracked. Perfect for lunch breaks or watching movies!

## 🎯 Context-Aware Work Filtering

Loggerheads intelligently categorizes activities based on your configuration:

**Example: Solana Developer**
- ✅ VSCode, Terminal → Always work
- ✅ Chrome on docs.solana.com → Work
- ✅ Twitter with Solana content → Captured as news
- ❌ WhatsApp messages → Filtered out
- ❌ Netflix → Ignored

**Example: Social Media Manager**
- ✅ Instagram, WhatsApp → Work (configurable)
- ✅ Twitter, Discord → Work
- ❌ Personal browsing → Filtered out

Configuration file: `~/.loggerheads_context.json`

## 🔧 Auto-Start on Boot

Enable automatic startup on macOS:

```bash
loggerheads install
```

This creates a LaunchAgent that:
- Starts on system boot
- Runs silently in the background
- Only tracks during work hours (9:30 AM - 4:30 PM)
- Generates summaries automatically

**Check if running:**
```bash
loggerheads status
# or
launchctl list | grep loggerheads
```

**View logs:**
```bash
tail -f ~/.loggerheads_logs/loggerheads.log
```

**Important:** You'll need to grant **Screen Recording** permission:
1. System Settings → Privacy & Security → Screen Recording
2. Enable for `loggerheads` or `Terminal`

## 📊 Daily Summary Format

Your AI-generated summary includes:

- ✅ **What I Worked on Today** - Detailed tasks and activities
- 🏁 **What I Completed** - Finished work items
- 📰 **What's the latest in the Solana Ecosystem** - News captured from browsing
- ⚠️ **Issues / Blockers** - Problems encountered
- 🔜 **Focus for Tomorrow** - Intelligent recommendations (except Fridays)

## 🔧 Configuration

### Tracking Settings

Edit `loggerheads/config.py`:

```python
# Work hours
WORK_START_TIME = "09:30"  # Start time
WORK_END_TIME = "16:30"    # End time (4:30 PM)
WORK_DAYS = [0, 1, 2, 3, 4]  # Mon-Fri

# Screenshot interval
SCREENSHOT_INTERVAL = 10  # seconds

# AI model
OLLAMA_MODEL = "llama3.2"  # or "mistral", "phi3", etc.
```

### Work Context

Edit `~/.loggerheads_context.json` or run:

```bash
loggerheads setup
```

## 🔒 Privacy & Security

- **100% Local Processing** - Ollama runs offline on your machine
- **Auto-Cleanup** - All screenshots deleted after summary generation
- **Database Wiped Daily** - No persistent activity logs
- **Only Summary Shared** - Only the AI summary goes to Discord
- **No Cloud Dependencies** - Everything stays on your computer

## 🆘 Troubleshooting

### Screenshots Failing

**Issue:** "Screenshot capture failed: could not create image from display"

**Solution:** Grant Screen Recording permission
- macOS: System Settings → Privacy & Security → Screen Recording
- Enable for Terminal or loggerheads

### AI Summary Not Working

**Issue:** Ollama connection errors

**Solution:**
```bash
# Check if Ollama is running
ollama serve

# Test the model
ollama run llama3.2
```

### Summary Quality Issues

- Try different model: Edit `config.py` and set `OLLAMA_MODEL = "mistral"`
- Increase screenshot interval if too much data
- Run `loggerheads setup` to refine work context

### Auto-Start Not Working

```bash
# Check status
loggerheads status

# Reinstall
loggerheads uninstall
loggerheads install

# Check LaunchAgent
launchctl list | grep loggerheads
```

## 🔄 Updates

```bash
# Update to latest version
cd loggerheads
git pull
pip3 install -e .
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or PR on GitHub.

---

**Built for Solana ecosystem professionals who want intelligent work tracking without the manual effort.**
