# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-06

### Added
- Initial release of AI Portfolio Manager
- Natural language interface powered by Google Gemini 2.0 Flash
- Full trading capabilities (market and limit orders)
- Real-time portfolio tracking via Alpaca API
- Advanced analytics:
  - Best/worst performers
  - Portfolio allocation analysis
  - Concentration risk detection
  - Total return calculation
  - Win/loss position tracking
- News integration for portfolio holdings
- Dollar-based investing (automatic share calculation)
- Two-step trade confirmation workflow
- Rate limiting and input validation
- Paper trading environment (safe testing)
- Rich terminal UI with colors and formatting
- Comprehensive documentation:
  - Usage guide
  - Development guide
  - Interactive walkthrough
  - Academic paper on function-calling AI
- 20+ AI function declarations for portfolio operations
- Multi-step workflow orchestration
- Data serialization for protobuf compatibility
- Error handling at all API layers

### Security
- Mandatory trade confirmation before execution
- Session rate limiting (20 turns max)
- Message rate limiting (10 per minute)
- Input length validation (2000 char limit)
- Paper trading default (no real money risk)
- API key protection via .env
- Prompt injection prevention

### Technical
- Modular architecture with clean separation of concerns
- Function-calling pattern with Google Gemini
- Alpaca Markets API integration (trading, data, news)
- Recursive data serialization for complex types
- Infinite loop prevention in AI workflows
- Graceful error handling and user-friendly messages

## [Unreleased]

### Planned Features
- Portfolio performance charts (ASCII art)
- Automated portfolio rebalancing
- Risk analysis and alerts
- Sector allocation analysis
- Options trading support
- Multi-account management
- PDF report generation
- Web UI with real-time updates
- Voice interface
- Price alert notifications
- Backtesting capabilities

---

For more details, see the [Development Guide](docs/DEVELOPMENT_GUIDE.md).
