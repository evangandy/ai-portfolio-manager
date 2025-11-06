# AI Portfolio Manager - Interactive Walkthrough Guide

Welcome! This guide will take you through the full capabilities of your AI Portfolio Manager with progressively complex tasks. Each section builds on the previous one.

---

## 🚀 Getting Started

First, launch the application:
```bash
python3 portfolio_manager.py
```

You'll see your current portfolio value and available cash. Now let's explore what you can do!

---

## 📚 Table of Contents
1. [Level 1: Basic Information Queries](#level-1-basic-information-queries)
2. [Level 2: Market Data & Research](#level-2-market-data--research)
3. [Level 3: Portfolio Analysis](#level-3-portfolio-analysis)
4. [Level 4: Simple Trading](#level-4-simple-trading)
5. [Level 5: Advanced Trading](#level-5-advanced-trading)
6. [Level 6: Complex Multi-Step Operations](#level-6-complex-multi-step-operations)
7. [Level 7: Strategic Portfolio Management](#level-7-strategic-portfolio-management)

---

## Level 1: Basic Information Queries

Start with simple questions to understand your portfolio.

### Try These Prompts:

**Portfolio Overview**
```
What do I own?
```
Expected: List of all your positions with quantities and values

**Account Balance**
```
How much cash do I have available?
```
Expected: Your available buying power

**Specific Position**
```
Show me my AAPL position
```
Expected: Detailed info on your Apple stock holding

**Portfolio Value**
```
What's my total portfolio worth?
```
Expected: Complete portfolio valuation

**Quick Status**
```
Give me a quick portfolio status
```
Expected: Summary with positions, cash, and total value

---

## Level 2: Market Data & Research

Now let's look at market data and news.

### Try These Prompts:

**Current Price**
```
What's the current price of SPY?
```
Expected: Real-time quote with bid/ask prices

**Multiple Quotes**
```
Get me quotes for AAPL, MSFT, and GOOGL
```
Expected: Current prices for all three stocks

**News Lookup**
```
What's the latest news on Tesla?
```
Expected: Recent news headlines for TSLA

**Historical Data**
```
Show me the last 7 days of price data for NVDA
```
Expected: Historical bars/candles for NVIDIA

**Portfolio News**
```
What's the news on my current holdings?
```
Expected: Latest news for all your positions

**Price Range Research**
```
What's SPY's 52-week high and low?
```
Expected: Historical price analysis

---

## Level 3: Portfolio Analysis

Analyze your portfolio's performance and allocation.

### Try These Prompts:

**Performance Analysis**
```
How is my portfolio performing?
```
Expected: Overall P&L, percentage returns

**Best Performers**
```
Show me my top 3 best performing stocks
```
Expected: Your winners ranked by % return

**Worst Performers**
```
What are my worst performing positions?
```
Expected: Your losers ranked by % loss

**Portfolio Allocation**
```
Break down my portfolio by allocation percentage
```
Expected: Each position with its % of total portfolio

**Risk Analysis**
```
Am I too concentrated in any single position?
```
Expected: Analysis of positions over 20% threshold

**Total Returns**
```
What's my total return across all positions?
```
Expected: Total P&L, win/loss ratio, statistics

**Position Extremes**
```
What's my largest position? What's my smallest?
```
Expected: Your biggest and smallest holdings by value

**Diversification Check**
```
How diversified is my portfolio?
```
Expected: AI analysis of your allocation spread

---

## Level 4: Simple Trading

Start executing basic trades.

### Try These Prompts:

**Simple Market Order**
```
Buy 1 share of SPY
```
Flow: AI gets current price → presents order → you confirm → AI executes

**Check Before Confirming**
```
You: Buy 1 share of VOO
AI: [Shows price and order details] Would you like me to proceed?
You: What's VOO's 52-week performance first?
AI: [Provides analysis]
You: Okay, yes proceed with the order
AI: [Executes trade]
```

**Sell Position**
```
Sell 5 shares of AAPL
```
Flow: AI prepares sell order → you confirm → execution

**Cancel Trade**
```
You: Buy 10 shares of TSLA
AI: [Presents order]
You: Actually, cancel that
AI: [Doesn't execute]
```

---

## Level 5: Advanced Trading

More sophisticated trading strategies.

### Try These Prompts:

**Dollar-Based Investing**
```
Buy $500 worth of AAPL
```
Flow: AI gets price → calculates shares → presents order → you confirm

**Multiple Dollar Amounts**
```
Put $250 into SPY and $250 into QQQ
```
Expected: AI calculates shares for both, executes both orders

**Limit Orders**
```
Buy 1 share of NVDA at a limit price of $125
```
Expected: Limit order placed, won't execute until price hits $125

**Conditional Limit Order**
```
You: What's MSFT trading at?
AI: [Provides current price, e.g., $420.50]
You: Set a limit order to buy 2 shares at $410
AI: [Creates limit order $10 below market]
```

**Sell with Limit**
```
Sell my AAPL shares at a limit of $195
```
Expected: Limit sell order placed

**Order Management**
```
Show me all my open orders
```
Expected: List of pending orders

**Cancel Specific Order**
```
You: Show me my open orders
AI: [Lists orders with IDs]
You: Cancel order #xyz123
AI: [Cancels that specific order]
```

---

## Level 6: Complex Multi-Step Operations

Combine multiple operations in one conversation flow.

### Try These Prompts:

**Research → Trade**
```
You: What's the latest news on Microsoft?
AI: [Provides MSFT news]
You: Looks good. Buy $1000 worth
AI: [Calculates shares, presents order]
You: Yes, proceed
AI: [Executes trade]
```

**Compare → Decide → Trade**
```
You: Compare SPY and QQQ performance
AI: [Provides analysis of both ETFs]
You: Which one would you recommend?
AI: [Provides recommendation with reasoning]
You: Okay, buy $500 of your recommendation
AI: [Calculates and presents order]
You: Confirm
AI: [Executes]
```

**Diversification Analysis → Rebalancing**
```
You: Analyze my portfolio diversification
AI: [Shows allocation breakdown, identifies concentration]
You: What should I do to improve it?
AI: [Provides rebalancing recommendations]
You: Buy $300 of VOO and $200 of BND
AI: [Calculates both, presents orders]
You: Yes
AI: [Executes both trades]
```

**News-Driven Decision**
```
You: Get me news on all my holdings
AI: [Provides news summaries for each position]
You: That news on AAPL looks concerning. What's my current position worth?
AI: [Shows AAPL position details]
You: Sell half of it
AI: [Calculates shares, presents sell order]
You: Proceed
AI: [Executes]
```

**Performance Review → Action**
```
You: Show me my worst performers
AI: [Lists bottom positions]
You: What's the news on [worst performer]?
AI: [Provides news]
You: Should I hold or sell?
AI: [Provides analysis and recommendation]
You: [Make decision based on advice]
```

---

## Level 7: Strategic Portfolio Management

Advanced portfolio strategy discussions and multi-operation workflows.

### Try These Prompts:

**Complete Portfolio Audit**
```
You: Give me a complete portfolio health check
AI: [Provides comprehensive analysis: allocation, performance, concentration, returns]
You: What are the biggest risks?
AI: [Identifies concentration, sector exposure, volatility]
You: Give me a plan to reduce risk
AI: [Provides detailed rebalancing strategy]
```

**Strategic Allocation**
```
I have $2000 to invest. I want 60% in index funds, 30% in tech, and 10% in bonds. What should I buy?
```
Expected: AI calculates specific amounts, recommends specific tickers, presents multiple orders

**Portfolio Rebalancing**
```
You: Show me my allocation
AI: [Shows breakdown]
You: I want to be 70% stocks, 20% bonds, 10% cash. Help me rebalance
AI: [Analyzes current vs target, suggests specific trades]
You: Proceed with your suggestions
AI: [Executes rebalancing trades]
```

**Risk Management**
```
You: Which positions are over 20% of my portfolio?
AI: [Lists concentrated positions]
You: That's too risky. Help me reduce concentration to under 15% each
AI: [Calculates required sales/purchases]
You: Show me the plan before executing
AI: [Presents detailed trade plan]
You: Approved
AI: [Executes all trades]
```

**Opportunistic Trading**
```
You: What tech stocks are down more than 5% today?
AI: [Searches and provides list]
You: Which of those have good fundamentals?
AI: [Provides analysis]
You: Allocate $1500 across your top 3 picks
AI: [Calculates $500 each, presents 3 orders]
You: Yes
AI: [Executes all 3]
```

**Tax Loss Harvesting Preparation**
```
You: Show me all my losing positions
AI: [Lists positions with losses]
You: Which ones are down more than 10%?
AI: [Filters and shows]
You: What's the total loss if I sell those?
AI: [Calculates realized loss]
You: [Decision on whether to harvest losses]
```

**Dollar Cost Averaging Setup**
```
I want to invest $500 per week into SPY and VOO. What's the current allocation that would give me 70% SPY and 30% VOO?
```
Expected: AI calculates $350 SPY + $150 VOO, shows shares for each

**Position Building with Limits**
```
You: I want to build a 5-share position in NVDA but only at good prices
AI: [Gets current price]
You: Set 5 limit orders: 1 share at current price -2%, 1 at -4%, 1 at -6%, 1 at -8%, 1 at -10%
AI: [Calculates all 5 prices, creates 5 limit orders]
```

**Complex Trade Sequencing**
```
You: Sell all my AAPL, use half the proceeds for VOO and half for BND
AI: [Gets AAPL position value, calculates sell, then calculates two buys]
You: Show me the full plan
AI: [Lists: Sell X AAPL for $Y, Buy Z VOO for $Y/2, Buy W BND for $Y/2]
You: Execute
AI: [Performs all 3 trades in sequence]
```

**Portfolio Stress Test Discussion**
```
You: What would happen to my portfolio if tech stocks dropped 20%?
AI: [Analyzes tech exposure, calculates potential impact]
You: How can I hedge against that?
AI: [Suggests defensive positions, bonds, diversification]
You: Implement your suggestion with $800
AI: [Calculates defensive purchases, presents orders]
```

---

## 🎯 Special Commands

Beyond natural language, these special commands are available:

**Update News**
```
update news
```
Fetches latest news for all your holdings and saves to `data/news.md`

**Generate Report** (Coming Soon)
```
report
```
Creates comprehensive portfolio report in `reports/`

**Exit Application**
```
exit
```
Safely closes the application

---

## 💡 Pro Tips

### Making the AI Work Best

1. **Be Specific**: Instead of "buy some Apple", say "buy 5 shares of AAPL"

2. **Multi-Step Workflows**: The AI can handle complex sequences. Break down your strategy naturally:
   - "First, show me my allocation"
   - "Now tell me which positions are too large"
   - "Help me rebalance by selling some of those"

3. **Always Review Before Trading**: The AI will always ask for confirmation before executing trades. Use this time to double-check.

4. **Combine Analysis with Action**:
   - "What's the news on MSFT? If it's positive, buy $500 worth"
   - "Show me my worst performer. Should I sell it or hold?"

5. **Ask for Explanations**: The AI can explain its reasoning:
   - "Why do you recommend diversifying?"
   - "Explain why this is a concentrated position"

6. **Use Dollar Amounts for Flexibility**: "$500 of AAPL" is easier than calculating shares yourself

7. **Check Order Status**: "Show me my open orders" to see what's pending

8. **Sequential Operations**: You can chain operations:
   - Get price → Analyze → Decide → Trade → Review result

---

## 🎓 Learning Path Recommendation

**Week 1: Information Gathering**
- Spend time with Levels 1-3
- Get comfortable with portfolio queries
- Learn to analyze your positions

**Week 2: Basic Trading**
- Progress to Level 4
- Execute simple market orders
- Practice the confirmation workflow

**Week 3: Advanced Techniques**
- Work through Level 5
- Try dollar-based investing
- Experiment with limit orders

**Week 4: Complex Strategies**
- Tackle Levels 6-7
- Combine multiple operations
- Develop your portfolio strategy

---

## 🔍 Testing Specific Features

### Function Testing Checklist

Test each capability to ensure everything works:

**Account Functions**
- [ ] Get account info
- [ ] View all positions
- [ ] Check specific position
- [ ] Portfolio summary

**Market Data**
- [ ] Get stock quote
- [ ] Historical bars
- [ ] News for specific stock
- [ ] News for portfolio holdings

**Trading**
- [ ] Market buy order
- [ ] Market sell order
- [ ] Limit order
- [ ] Cancel order
- [ ] View order history

**Analytics**
- [ ] Portfolio allocation
- [ ] Best/worst performers
- [ ] Total returns
- [ ] Largest/smallest positions
- [ ] Concentration analysis
- [ ] Dollar-to-shares calculation

**Complex Workflows**
- [ ] Research → Trade sequence
- [ ] Multi-stock purchase
- [ ] Portfolio rebalancing
- [ ] Risk reduction strategy

---

## ❓ Troubleshooting

**AI Doesn't Execute Trade**
- Did you confirm? Try saying "yes", "confirm", "proceed", or "do it"

**Price Seems Wrong**
- Market might be closed (9:30 AM - 4 PM ET)
- Check if you're using paper trading (no real money)

**Order Rejected**
- Check if you have sufficient buying power
- Verify market hours for market orders

**News Not Updating**
- Use the `update news` command
- Check your Alpaca API limits

**AI Seems Confused**
- Be more specific with stock symbols
- Break complex requests into smaller steps
- Try rephrasing your question

---

## 📊 Sample Full Session

Here's what a complete session might look like:

```
$ python3 portfolio_manager.py

AI Portfolio Manager
Connected to Alpaca (Paper Trading)
Commands: 'update news', 'report', 'exit'

💰 Portfolio Value: $10,485.23
💵 Cash Available: $2,315.67

You: What do I own?
AI: You currently own:
• 10 shares of AAPL worth $1,875.40 (up 8.2%)
• 5 shares of SPY worth $3,429.20 (up 3.5%)
• 8 shares of VOO worth $4,145.96 (up 5.1%)

You: Show me my allocation
AI: Your portfolio breakdown:
• AAPL: $1,875.40 (19.6%)
• VOO: $4,145.96 (43.4%)
• SPY: $3,429.20 (35.9%)
• Cash: $2,315.67 (1.1%)

You: Am I too concentrated?
AI: You're well diversified. No single position exceeds 50% of your portfolio. VOO at 43.4% is your largest holding but still within reasonable limits. Your tech exposure through AAPL is balanced by broad market index funds.

You: What's the news on AAPL?
AI: Latest AAPL headlines:
• Apple announces new AI features in iOS 18
• iPhone 16 sales exceed expectations in Q4
• Services revenue hits all-time high

You: Looks positive. Buy $500 more AAPL
AI: At the current price of $187.54, I can purchase 2 shares of AAPL for $375.08. Would you like me to proceed?

You: Yes
AI: Order placed successfully! Bought 2 shares of AAPL at market price.

You: What's my new allocation?
AI: Updated portfolio breakdown:
• VOO: $4,145.96 (42.1%)
• SPY: $3,429.20 (34.8%)
• AAPL: $2,250.48 (22.8%)
• Cash: $1,940.59 (0.3%)

You: Perfect. exit
Goodbye! Happy trading!
```

---

## 🚀 Next Steps

Now that you understand the full capabilities:

1. **Start Simple**: Begin with information queries to get comfortable
2. **Progress Gradually**: Move to analysis, then trading
3. **Experiment**: Try different phrasing and see how the AI responds
4. **Build Strategies**: Use complex workflows to manage your portfolio
5. **Stay Informed**: Regularly check news and performance

Remember: This is paper trading, so feel free to experiment and learn without risk!

---

## 📚 Additional Resources

- **[FEATURE_TESTING_GUIDE.md](FEATURE_TESTING_GUIDE.md)** - Comprehensive feature testing
- **[AI_FUNCTIONS_API.md](AI_FUNCTIONS_API.md)** - Technical function reference
- **[TRADING_GUIDE.md](TRADING_GUIDE.md)** - Detailed trading instructions
- **[USAGE.md](USAGE.md)** - Basic usage guide

---

**Happy Trading! 🎉**

Questions? Issues? The AI is here to help - just ask!
