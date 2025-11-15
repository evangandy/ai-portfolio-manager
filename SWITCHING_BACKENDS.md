# Switching Between Gemini and Ollama

You have two AI backends available. Here's how to switch between them:

## Quick Switch (Easiest)

### Option 1: Use the Switch Script

```bash
# Switch to Gemini
./switch_ai.sh gemini

# Switch to Ollama
./switch_ai.sh ollama

# Check current setting
./switch_ai.sh
```

### Option 2: Edit .env Manually

Open `.env` and change this line:

```bash
# For Gemini (fast, reliable, uses API credits)
AI_BACKEND=gemini

# OR

# For Ollama (local, unlimited, slower)
AI_BACKEND=ollama
```

Then restart the app.

## Current Configuration

**Right now you're set to: OLLAMA** ✅

Your `.env` shows:
```bash
AI_BACKEND=ollama
```

## When to Use Each

### Use Gemini When:
- ✅ You need **fast responses** (1-2 seconds)
- ✅ You have **complex multi-step tasks**
- ✅ You want **maximum reliability**
- ✅ You have API credits available
- ✅ You're doing **important portfolio decisions**

**Example tasks:**
- Complex analysis and trading workflows
- Multi-step operations (get news → analyze → trade → report)
- Anything time-sensitive

### Use Ollama When:
- ✅ You **ran out of Gemini credits**
- ✅ You want to **save API costs**
- ✅ You're **testing/experimenting**
- ✅ You want **100% privacy** (no data sent to cloud)
- ✅ You're doing **simple queries**
- ✅ You're working **offline**

**Example tasks:**
- Checking positions
- Getting quotes
- Simple analysis
- Testing the app
- Learning how it works

## Performance Comparison

| Feature | Gemini | Ollama |
|---------|--------|--------|
| **Speed** | ⚡ 1-2 sec | 🐌 5-15 sec |
| **Reliability** | 🌟 Excellent | ⭐ Good |
| **Function Calling** | ✅ Native | ⚠️ Simulated |
| **Complex Tasks** | ✅ Excellent | ⚠️ Struggles |
| **Cost** | 💰 Free tier | 🆓 Unlimited |
| **Internet** | 📡 Required | ❌ Not needed |
| **Privacy** | ☁️ Cloud | 🔒 100% local |

## Hybrid Mode (RECOMMENDED)

Set your `.env` to:
```bash
AI_BACKEND=gemini
```

**Benefits:**
- Uses Gemini by default (fast, reliable)
- Auto-switches to Ollama when credits run out
- Best of both worlds!
- Never get stuck!

## Current Status Check

```bash
# What's currently set?
grep "AI_BACKEND=" .env

# Is Ollama running?
curl http://localhost:11434/api/tags

# What models do you have?
ollama list
```

## Examples

### Switching to Gemini
```bash
./switch_ai.sh gemini
python3 portfolio_manager.py
```

You'll see:
```
[cyan]Using Gemini API backend[/cyan]
```

### Switching to Ollama
```bash
./switch_ai.sh ollama
python3 portfolio_manager.py
```

You'll see:
```
[cyan]Using Ollama (local LLM) backend[/cyan]
```

## Troubleshooting

### "Ollama is not running"
```bash
ollama serve
```

### "Gemini quota exceeded"
The app will **automatically** switch to Ollama. You'll see:
```
[yellow]Gemini API quota exhausted. Switching to Ollama...[/yellow]
```

### Want to force a specific backend
```bash
# Force Ollama even if Gemini available
AI_BACKEND=ollama

# Force Gemini (will error if no credits)
AI_BACKEND=gemini
```

## Testing Both

### Test Gemini
```bash
./switch_ai.sh gemini
python3 portfolio_manager.py
# Try: "What stocks do I own?"
# Exit with Ctrl+C
```

### Test Ollama
```bash
./switch_ai.sh ollama
python3 portfolio_manager.py
# Try: "What stocks do I own?"
# Exit with Ctrl+C
```

### Compare Speed
Notice Ollama takes 5-15 seconds vs Gemini's 1-2 seconds.

## Your Current Setup

✅ **Ollama Backend Active**
```bash
AI_BACKEND=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

## Quick Commands Reference

```bash
# Switch to Gemini
./switch_ai.sh gemini

# Switch to Ollama
./switch_ai.sh ollama

# Check current
./switch_ai.sh

# Run app
python3 portfolio_manager.py

# Stop app
Ctrl+C (or type "exit")
```

---

**Note:** The app must be restarted after changing `AI_BACKEND` for the change to take effect.
