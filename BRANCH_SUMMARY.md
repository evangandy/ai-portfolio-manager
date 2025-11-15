# Experimental Branch Summary

## Branch: `experimental-gemini-improvements`

This experimental branch contains major improvements to fix Gemini function calling issues and adds Ollama support as a fallback.

## What's New

### 1. Fixed Gemini Function Calling Issues ✅

**Problems Solved:**
- ❌ AI printing code blocks instead of executing functions
- ❌ AI asking for data it can fetch itself
- ❌ AI not completing multi-step task chains

**Solutions Implemented:**
- Enhanced system prompt with explicit multi-step execution rules
- Added temperature=0 for deterministic behavior
- Switched to gemini-2.0-flash-exp model
- Explicit function_calling_config with AUTO mode
- Increased max iterations from 5→10
- Post-processing filter to strip code blocks

**Result:** AI should now execute complex workflows like "Get news on my stocks, sell any with bad news, buy SCHD and TLT" in one shot without stopping.

### 2. Added Ollama Support 🆕

**Why:**
- Gemini API has free tier limits (credits run out)
- Ollama runs models locally (100% free, unlimited)
- Works offline
- Complete privacy (no data sent to cloud)

**Features:**
- New `OllamaAgent` class with function calling
- Automatic fallback when Gemini quota exhausted
- Configurable via `AI_BACKEND` environment variable
- Supports popular models: llama3.1, mistral, qwen2.5, etc.

**How It Works:**
1. By default, uses Gemini API (fast, reliable)
2. When quota exceeded, automatically switches to Ollama
3. Or manually set `AI_BACKEND=ollama` in `.env`

## Files Changed

### Core Changes
- **core/gemini_agent.py**: Major improvements to system prompt and configuration
- **core/ollama_agent.py**: New local LLM agent implementation
- **portfolio_manager.py**: Added backend selection and automatic fallback

### Configuration
- **.env.example**: Added AI_BACKEND, OLLAMA_MODEL, OLLAMA_BASE_URL options

### Documentation
- **IMPROVEMENTS_MADE.md**: Detailed explanation of all Gemini fixes
- **RESEARCH_FINDINGS.md**: Community research on Gemini issues
- **OLLAMA_SETUP.md**: Complete Ollama installation and setup guide
- **BRANCH_SUMMARY.md**: This file

## How to Use

### Option 1: Gemini with Auto-Fallback (Recommended)

`.env` file:
```bash
AI_BACKEND=gemini
GEMINI_API_KEY=your_key_here
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```

App will use Gemini, then automatically switch to Ollama when credits run out.

### Option 2: Ollama Only

1. Install Ollama: https://ollama.ai/
2. Start server: `ollama serve`
3. Pull model: `ollama pull llama3.1`
4. Set `.env`:
```bash
AI_BACKEND=ollama
OLLAMA_MODEL=llama3.1
```

### Option 3: Gemini Only

`.env` file:
```bash
AI_BACKEND=gemini
GEMINI_API_KEY=your_key_here
```

## Testing Recommendations

### Test 1: Simple Query
```
You: What stocks do I own?
```
Should call `get_all_positions()` and respond immediately.

### Test 2: Multi-Step Task
```
You: Get news on my stocks and sell any with bad news
```
Should chain: positions → news → sell → report results

### Test 3: Complex Workflow
```
You: Get news, sell stocks with bad news, buy SCHD and TLT equally, show me the dividend yield
```
Should execute entire workflow without stopping.

### Test 4: Ollama Fallback
When Gemini credits run out, should automatically switch and continue working.

## Switching Between Branches

### Go Back to Stable Main
```bash
git checkout main
```

### Return to Experimental
```bash
git checkout experimental-gemini-improvements
```

### View All Branches
```bash
git branch -a
```

## Performance Comparison

### Gemini API
- ✅ Very fast (cloud-based)
- ✅ Highly reliable
- ✅ Native function calling
- ❌ Free tier limits
- ❌ Requires internet
- ❌ Data sent to Google

### Ollama (Local)
- ✅ Unlimited usage
- ✅ Works offline
- ✅ 100% private
- ✅ No API costs
- ⚠️ Slower (depends on hardware)
- ⚠️ Simulated function calling
- ❌ Requires model download (several GB)

## Merging to Main

Once tested and stable:

```bash
# Switch to main
git checkout main

# Merge experimental branch
git merge experimental-gemini-improvements

# Push to GitHub
git push origin main
```

Or create a Pull Request on GitHub for review.

## GitHub Links

- Main Branch: https://github.com/evangandy/ai-portfolio-manager/tree/main
- Experimental Branch: https://github.com/evangandy/ai-portfolio-manager/tree/experimental-gemini-improvements
- Create PR: https://github.com/evangandy/ai-portfolio-manager/pull/new/experimental-gemini-improvements

## Next Steps

1. **Test thoroughly** with various commands
2. **Try Ollama** to ensure fallback works
3. **Monitor performance** and compare Gemini vs Ollama
4. **Report issues** if any problems occur
5. **Merge to main** once confident it's stable

## Rollback Plan

If anything breaks:

```bash
# Quick rollback to main
git checkout main

# Or revert specific commit
git revert <commit-hash>

# Or reset branch (destructive)
git reset --hard origin/main
```

## Questions?

- Check [IMPROVEMENTS_MADE.md](IMPROVEMENTS_MADE.md) for technical details
- Check [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for Ollama setup help
- Check [RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md) for community solutions

---

**Created**: 2025-11-14
**Branch**: experimental-gemini-improvements
**Status**: Testing Phase
**Recommendation**: Test before merging to main
