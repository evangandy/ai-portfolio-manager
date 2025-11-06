# AI Portfolio Manager - Usage Guide

## Quick Start

```bash
python3 portfolio_manager.py
```

## Features

### 1. Natural Language Portfolio Queries
Ask questions about your portfolio in plain English:

- "What do I own?"
- "How is my portfolio performing?"
- "Show me details on AAPL"
- "What's my cash balance?"

### 2. News Updates
Keep track of news for all your holdings:

```
update news
```

This will:
- Fetch the latest news for all your portfolio positions
- Save to `data/news.md` (human-readable)
- Save to `data/news.json` (machine-readable)

### 3. AI-Powered Trading Suggestions
Ask the AI for trading advice:

- "Should I buy more tech stocks?"
- "What do you think about diversifying?"
- "Buy $500 of VOO"

The AI will:
- Analyze your current portfolio
- Provide reasoning for suggestions
- Ask for confirmation before executing trades

### 4. Available Commands

- `update news` - Fetch latest news for portfolio positions
- `report` - Generate portfolio report (coming soon)
- `exit` - Quit the application

## Example Session

```
AI Portfolio Manager
Connected to Alpaca (Paper Trading)

Commands: 'update news', 'report', 'exit'

💰 Portfolio Value: $10,206.19
💵 Cash Available: $7,520.99

You: what do I own?

AI: You currently hold 10 shares of AAPL with an average entry price of $247.90.
    The current price is $268.72, giving your AAPL position a market value of
    $2,687.15 and an unrealized profit of $208.15 (+8.4%). You also have $7,520.99
    in cash available.

You: should I diversify?

AI: Yes, I'd recommend diversifying. You're currently 100% in AAPL, which is risky.
    Consider adding:
    1. Index funds (VOO, SPY) for broad market exposure
    2. Bonds (TLT, BND) for stability
    3. Other sectors (healthcare, consumer staples)

    Would you like me to suggest specific allocations?

You: update news

AI: Fetching latest news...
    ✓ AAPL - 8 articles
    Saved to: data/news.md

You: exit

AI: Goodbye! Happy trading!
```

## Tips

1. **Be Specific**: The more specific your questions, the better the AI can help
2. **Check News Regularly**: Run `update news` to stay informed about your holdings
3. **Review Before Trading**: Always review the AI's reasoning before confirming trades
4. **Paper Trading**: This uses Alpaca's paper trading environment - no real money

## Troubleshooting

### API Connection Issues
- Verify your `.env` file has the correct API keys
- Check your internet connection
- Ensure API keys haven't expired

### Error Messages
The AI will provide error messages if:
- A stock symbol isn't found
- You don't have enough cash for a trade
- API rate limits are hit

## Advanced Usage

### Function Calling
The AI has access to these functions:
- `get_portfolio_summary()` - Full portfolio overview
- `get_position_detail(symbol)` - Details on specific holdings
- `get_news(symbols, days)` - News for specific stocks
- `place_order(symbol, qty, side)` - Execute trades (with confirmation)

The AI automatically calls these functions based on your questions!

## Safety Notes

- ⚠️ This is paper trading only - no real money involved
- ⚠️ Always verify trade details before confirming
- ⚠️ The AI provides suggestions, not financial advice
- ⚠️ Never share your API keys

## Next Steps

- Try different types of queries
- Experiment with trade suggestions
- Monitor your portfolio's performance
- Use the news feature to stay informed

Happy trading! 📈
