# 🤖 AI Portfolio Manager

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Alpaca API](https://img.shields.io/badge/API-Alpaca-green.svg)](https://alpaca.markets/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.0-orange.svg)](https://ai.google.dev/)

> **AI-powered portfolio management with natural language interface and full trading capabilities using Google Gemini's function-calling architecture**

Transform your portfolio management with an AI assistant that doesn't just advise—it acts. Built on Google Gemini 2.0's function-calling architecture, this system provides real-time portfolio insights, executes trades, and delivers sophisticated analytics through natural conversation.

---

## 🎯 What Makes This Different?

Unlike traditional chatbots that only provide generic advice, this AI agent:

✅ **Accesses Real Data** - Connects directly to your Alpaca brokerage account
✅ **Executes Real Trades** - Places orders with confirmation workflow
✅ **Zero Hallucination** - All responses grounded in actual API data
✅ **Multi-Step Workflows** - Orchestrates complex operations automatically
✅ **Natural Language** - No commands to memorize, just talk naturally

**Traditional AI**: _"I can't access your portfolio, but generally you should..."_
**This AI**: _"You own 10 shares of AAPL worth $2,687 (up 8.4%). You have $7,520 in cash."_

---

## ✨ Features

### 💬 Natural Language Interface
- Ask questions in plain English—no commands, no syntax
- Conversational AI understands context and intent
- Multi-turn conversations with memory

### 📊 Real-time Portfolio Tracking
- Live positions and balances
- Unrealized P&L and performance metrics
- Current market prices with bid/ask spreads

### 📈 Advanced Analytics
- Best/worst performing positions
- Portfolio allocation breakdown
- Concentration risk analysis
- Total return and win/loss ratios

### 💰 AI-Powered Trading
- **Market orders** - Instant execution
- **Limit orders** - Set your target price
- **Dollar-based investing** - "Buy $500 of AAPL" (auto-calculates shares)
- **Two-step confirmation** - Safe workflow prevents accidents

### 📰 News Integration
- Latest news for all holdings
- Markdown and JSON export
- AI-ready cached summaries

### 🔒 Safety Features
- Paper trading by default (no real money risk)
- Mandatory trade confirmation
- Rate limiting (20 turns/session, 10 msgs/min)
- Input validation and error handling

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure API keys** (already done in `.env`):
   ```
   ALPACA_API_KEY=your_key_here
   ALPACA_SECRET_KEY=your_secret_here
   GEMINI_API_KEY=your_gemini_key_here
   ```

3. **Run the application:**
   ```bash
   python3 portfolio_manager.py
   ```

## 💬 Example Usage

### Portfolio Queries
```
You: what do I own?
You: how is AAPL performing?
You: show me my portfolio value
You: what's my best performing stock?
You: am I too concentrated in any position?
You: what's my total return?
```

### Trading
```
You: buy 1 share of SPY
AI: I've prepared an order to buy 1 share of SPY at $585.79.
    Would you like me to proceed?
You: yes
AI: Order placed successfully! BUY 1 SPY

You: buy $500 of VOO
AI: I can purchase 1 share of VOO for $485.23. Proceed?
You: yes
AI: Order placed! Invested $485.23 in VOO.

You: sell AAPL at $175 limit
AI: Limit order prepared. Proceed?
You: yes
AI: Limit order placed to sell AAPL at $175.00
```

### Advanced Analysis
```
You: show me my portfolio allocation
You: which positions are over 20% of my portfolio?
You: what's my largest position?
You: how many winning vs losing positions?
```

### News & Analysis
```
You: update news
You: what's the latest news on my stocks?
You: should I diversify?
You: any recommendations for rebalancing?
```

## 📖 Documentation

- **[Usage Guide](docs/USAGE.md)** - Comprehensive feature documentation
- **[Development Guide](docs/DEVELOPMENT_GUIDE.md)** - Architecture deep-dive and implementation
- **[Interactive Walkthrough](docs/INTERACTIVE_WALKTHROUGH.md)** - Step-by-step tutorial
- **[Academic Paper](docs/ACADEMIC_PAPER.md)** - Why function-calling AI is superior

### External Resources
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Gemini Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling)

## 🎯 Commands
- **Natural chat** - Just talk to the AI naturally
- **`update news`** - Fetch latest news for portfolio holdings
- **`report`** - Generate portfolio report (coming soon)
- **`exit`** - Quit the application

## 🏗️ Project Structure

```
ai-portfolio-manager/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── .env.example             # Template for API keys
├── .gitignore               # Git ignore rules
│
├── portfolio_manager.py     # Main CLI entry point
│
├── core/                    # Core application modules
│   ├── __init__.py
│   ├── gemini_agent.py     # AI agent with function calling
│   ├── alpaca_client.py    # Alpaca API wrapper
│   └── news_fetcher.py     # News aggregation & formatting
│
├── data/                    # Generated data (gitignored)
│   ├── news.md             # News cache (markdown)
│   └── news.json           # News cache (JSON)
│
├── reports/                 # Generated reports (future)
│
└── docs/                    # Documentation
    ├── USAGE.md            # Detailed usage guide
    ├── DEVELOPMENT_GUIDE.md # Architecture & implementation
    ├── INTERACTIVE_WALKTHROUGH.md # Step-by-step tutorial
    └── ACADEMIC_PAPER.md   # Research paper
```

---

## 🔒 Security & Safety

### Paper Trading Default
Uses Alpaca's paper trading environment—**no real money at risk**. All trades are simulated.

### Trade Confirmation Workflow
Every trade requires explicit confirmation. The AI **cannot** bypass this—it's architecturally enforced.

### Rate Limiting
- 20 turns per session
- 10 messages per minute
- 2000 character input limit

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**This software is for educational purposes only.**

- Default uses **paper trading** (no real money)
- Not financial advice
- Use at your own risk
- Author assumes no liability

---

**Built with AI, for AI-powered portfolio management** 🚀
