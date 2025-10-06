# Ollama Setup Guide

Complete guide to install and configure Ollama for local AI summarization.

## 📥 Install Ollama

### macOS
```bash
# Download and install from official site
curl -fsSL https://ollama.com/install.sh | sh

# Or use Homebrew
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download installer from: https://ollama.com/download/windows

## 🚀 Start Ollama

```bash
# Start the Ollama service
ollama serve
```

**Note:** Keep this terminal open - Ollama needs to run in the background.

Alternatively, Ollama may auto-start as a background service after installation.

## 📦 Download a Model

Open a **new terminal** and run:

```bash
# Download Llama 3.2 (recommended - 2GB, fast and good quality)
ollama pull llama3.2

# OR other options:
ollama pull mistral       # 4GB - Very good quality
ollama pull phi3          # 2GB - Faster, lighter
ollama pull llama3.1      # 4.7GB - Best quality, slower
```

**Recommended:** Start with `llama3.2` - it's fast and works well for this use case.

## ✅ Test Ollama

```bash
# Test the model
ollama run llama3.2 "Hello, how are you?"
```

You should see a response from the AI. Press `Ctrl+D` or type `/bye` to exit.

## 🔧 Configure the App

The app is already configured to use Ollama! Settings in `config.py`:

```python
USE_AI_SUMMARIZATION = True
OLLAMA_MODEL = "llama3.2"  # Change if you downloaded a different model
OLLAMA_API_URL = "http://localhost:11434"
```

## 🎯 Usage

Once Ollama is running:

```bash
# Start the activity tracker
python scheduler.py
```

The app will automatically use Ollama to generate intelligent summaries!

## 🔍 Verify Ollama is Running

```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags
```

Should return a JSON list of installed models.

## 📊 Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama3.2 | 2GB | Fast | Good | **Recommended - balanced** |
| phi3 | 2GB | Very Fast | Decent | Low-end hardware |
| mistral | 4GB | Medium | Very Good | Better quality |
| llama3.1 | 5GB | Slow | Excellent | Best results |

## 🆘 Troubleshooting

**"Could not connect to Ollama"**
- Make sure `ollama serve` is running
- Check http://localhost:11434 in browser

**Model not found**
- Run `ollama pull llama3.2`
- Update `OLLAMA_MODEL` in config.py to match

**Too slow**
- Try a smaller model like `phi3`
- Reduce screenshot count

**Out of memory**
- Use a smaller model
- Close other applications
- Reduce the number of screenshots being analyzed

## 💰 Cost

**FREE!** Ollama runs 100% locally on your machine. No API costs.

## 🔒 Privacy

All AI processing happens on your local machine. No data is sent to external services.
