# Ollama Setup Guide

## What is Ollama?

Ollama allows you to run large language models (LLMs) locally on your computer. This is useful when:
- Gemini API credits run out
- You want to work offline
- You want full privacy (no data sent to cloud)
- You want to avoid API rate limits

## Installation

### macOS

```bash
# Download and install from website
# Visit: https://ollama.ai/download

# Or use Homebrew
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

Download the installer from: https://ollama.ai/download

## Setup Steps

### 1. Start Ollama Server

```bash
ollama serve
```

Leave this running in a terminal window.

### 2. Pull a Model

In a new terminal window:

```bash
# Recommended: Llama 3.1 (8B parameters, good balance)
ollama pull llama3.1

# Alternative options:
# ollama pull mistral       # Smaller, faster
# ollama pull llama3.1:70b  # Larger, smarter (requires more RAM)
# ollama pull qwen2.5:7b    # Good for function calling
```

### 3. Test the Model

```bash
ollama run llama3.1
```

Type a message and press Enter. Type `/bye` to exit.

### 4. Configure Your Portfolio Manager

Edit your `.env` file:

```bash
# Option 1: Use Ollama by default
AI_BACKEND=ollama
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434

# Option 2: Use Gemini but auto-fallback to Ollama when credits run out
AI_BACKEND=gemini
GEMINI_API_KEY=your_key_here
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```

## Model Recommendations

### For Low RAM (8-16 GB)
- `llama3.1` (8B) - Best balance
- `mistral` (7B) - Faster, lighter
- `phi3` (3.8B) - Smallest option

### For Medium RAM (16-32 GB)
- `llama3.1:13b` - Better reasoning
- `qwen2.5:14b` - Good for function calling

### For High RAM (32+ GB)
- `llama3.1:70b` - Most capable
- `mixtral:8x7b` - Excellent quality

## System Requirements

| Model Size | Minimum RAM | Recommended RAM | Speed |
|------------|-------------|-----------------|-------|
| 3B params  | 4 GB        | 8 GB           | Fast  |
| 7B params  | 8 GB        | 16 GB          | Good  |
| 13B params | 16 GB       | 32 GB          | Medium|
| 70B params | 64 GB       | 128 GB         | Slow  |

## Usage

### Normal Startup (Using Gemini)

```bash
python portfolio_manager.py
# Uses Gemini API
```

### When Gemini Credits Run Out

The app will **automatically switch** to Ollama when it detects:
- Quota exhausted errors
- 429 (rate limit) errors
- Resource exhausted errors

You'll see:
```
[yellow]Gemini API quota exhausted. Switching to Ollama...[/yellow]
```

### Force Ollama from Start

Set in `.env`:
```bash
AI_BACKEND=ollama
```

Then run normally:
```bash
python portfolio_manager.py
```

## Function Calling with Ollama

**Note**: Ollama models don't have native function calling like Gemini. The implementation uses a simplified approach:

1. The model outputs JSON function calls
2. The agent parses and executes them
3. Results are fed back to the model

**Performance Considerations**:
- Ollama may be slower than Gemini
- Local models may be less reliable at complex multi-step tasks
- Larger models (13B+) perform better with function calling
- May require more explicit prompting

## Troubleshooting

### "Error: Ollama is not running"

Solution:
```bash
ollama serve
```

### "Cannot connect to Ollama"

Check if Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

Should return list of installed models.

### "Model not found"

Pull the model:
```bash
ollama pull llama3.1
```

### Model is slow

Options:
1. Use a smaller model: `ollama pull mistral`
2. Reduce context length in the code
3. Use GPU acceleration (automatic if CUDA/Metal available)

### Model gives poor results

Try a larger model:
```bash
ollama pull llama3.1:13b
```

Or use a model specialized for function calling:
```bash
ollama pull qwen2.5:14b
```

## Checking Status

### List installed models
```bash
ollama list
```

### Check running models
```bash
ollama ps
```

### Remove a model
```bash
ollama rm llama3.1
```

### Update a model
```bash
ollama pull llama3.1
```

## Performance Tips

1. **Keep Ollama running**: Don't stop/start the server frequently
2. **Use SSD**: Models load faster from SSD
3. **Close other apps**: Free up RAM for the model
4. **Use GPU**: Ollama auto-detects CUDA (NVIDIA) or Metal (Apple Silicon)
5. **Smaller models**: For testing, use smaller models (mistral, phi3)

## Switching Back to Gemini

Edit `.env`:
```bash
AI_BACKEND=gemini
```

Restart the application.

## Advanced Configuration

### Custom Ollama Port

If Ollama runs on a different port:

```bash
OLLAMA_BASE_URL=http://localhost:8080
```

### Remote Ollama Server

Run Ollama on another machine:

```bash
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

### Multiple Models

You can switch models anytime by changing `.env`:

```bash
OLLAMA_MODEL=mistral
```

No need to restart the app - it uses the env var each time.

## Comparison: Gemini vs Ollama

| Feature | Gemini | Ollama |
|---------|--------|--------|
| Cost | Free tier, then paid | Free (local) |
| Speed | Fast (cloud) | Depends on hardware |
| Privacy | Data sent to Google | 100% local |
| Reliability | High | Depends on model |
| Function Calling | Native support | Simulated |
| Setup | API key only | Install + download models |
| Offline | No | Yes |
| Model Quality | Very high | Good to excellent |

## Recommended Workflow

1. **Default**: Use Gemini (fast, reliable)
2. **Fallback**: Auto-switch to Ollama when quota exceeded
3. **Development**: Use Ollama to save API credits
4. **Production**: Use Gemini for best results

## Resources

- Official Site: https://ollama.ai/
- Model Library: https://ollama.ai/library
- GitHub: https://github.com/ollama/ollama
- Discord: https://discord.gg/ollama
