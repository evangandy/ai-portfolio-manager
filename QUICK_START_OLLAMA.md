# Quick Start: Running with Ollama

## ✅ You're All Set!

Everything is already configured:
- ✅ Ollama installed
- ✅ llama3.1:8b model downloaded (4.9 GB)
- ✅ Ollama server running
- ✅ .env configured

## 🚀 To Run

Simply start the application:

```bash
cd "/Users/evangandy/Desktop/GitHub Projects/Portfolio Management Tool"
python3 portfolio_manager.py
```

You should see:
```
AI Portfolio Manager
Connected to Alpaca (Paper Trading)
[cyan]Using Ollama (local LLM) backend[/cyan]

💰 Portfolio Value: $X,XXX.XX
💵 Cash Available: $X,XXX.XX

You: _
```

## 📝 Try These Commands

### Simple Queries
```
What stocks do I own?
What's my portfolio value?
Show me my positions
```

### Getting Data
```
Get the latest quote for AAPL
Get news on AAPL
What's the current price of TSLA?
```

### Analysis
```
Show me my best performers
What are my worst performers?
Analyze my portfolio allocation
```

### Trading (be careful, this is real!)
```
Get a quote for AAPL
Buy 1 share of AAPL
Sell 1 share of AAPL
```

## ⚡ Performance Notes

**Ollama (Local) vs Gemini (Cloud)**

| Aspect | Ollama | Gemini |
|--------|--------|--------|
| Speed | 3-10 seconds per response | 1-2 seconds |
| Reliability | Good | Excellent |
| Cost | Free | Free tier, then paid |
| Internet | Not required | Required |
| Privacy | 100% local | Data sent to Google |

**Expected Behavior:**
- Ollama responses take **5-15 seconds** (depending on your Mac)
- May need more explicit prompts than Gemini
- Function calling is simulated (not native)

## 🔄 Switching Back to Gemini

Edit `.env`:
```bash
AI_BACKEND=gemini
```

Then restart the application.

## 🔧 Troubleshooting

### "Error: Ollama is not running"
```bash
# Start Ollama server
ollama serve
```

### "Cannot connect to Ollama"
Check if running:
```bash
curl http://localhost:11434/api/tags
```

### Ollama is slow
- Close other applications to free up RAM
- Use a smaller model: `OLLAMA_MODEL=gemma:2b` (you have this installed)
- Ensure you're on Apple Silicon (M1/M2/M3) for Metal acceleration

### Model not found
Pull it:
```bash
ollama pull llama3.1:8b
```

## 📊 Current Configuration

Your `.env` file:
```bash
AI_BACKEND=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

Your installed models:
```
llama3.1:8b  - 4.9 GB (RECOMMENDED - currently configured)
gemma:2b     - 1.7 GB (faster, less capable)
```

## 🎯 Best Practices

1. **Start Simple**: Test with basic queries first
2. **Be Explicit**: Ollama needs clearer instructions than Gemini
3. **One Step at a Time**: Complex multi-step tasks may be less reliable
4. **Check Results**: Verify trades before confirming
5. **Use Gemini for Complex Tasks**: Switch to Gemini for better results on hard queries

## 💡 Tips

### For Faster Responses
Switch to the smaller model:
```bash
# In .env
OLLAMA_MODEL=gemma:2b
```

### For Better Quality
Use Gemini for important decisions:
```bash
# In .env
AI_BACKEND=gemini
```

### Hybrid Approach (RECOMMENDED)
```bash
# In .env
AI_BACKEND=gemini
# Keep Ollama config for automatic fallback
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

This way:
- Uses Gemini normally (fast, reliable)
- Auto-switches to Ollama when credits run out
- Best of both worlds!

## 🆘 Need Help?

- Check [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed setup
- Check [IMPROVEMENTS_MADE.md](IMPROVEMENTS_MADE.md) for technical details
- Ollama docs: https://ollama.ai/
- Model library: https://ollama.ai/library

## 🎉 You're Ready!

Just run:
```bash
python3 portfolio_manager.py
```

And start chatting with your AI portfolio manager!
