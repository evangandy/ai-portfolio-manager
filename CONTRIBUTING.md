# Contributing to AI Portfolio Manager

Thank you for your interest in contributing to the AI Portfolio Manager! This project demonstrates function-calling AI architecture for portfolio management.

## 🎯 Project Goals

This project aims to:
1. Demonstrate the superiority of function-calling AI over traditional chatbots
2. Provide a safe, educational tool for portfolio management
3. Showcase best practices in AI agent architecture
4. Enable accessible, sophisticated portfolio analytics

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug:
1. Check if it's already reported in [Issues](https://github.com/yourusername/ai-portfolio-manager/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS)
   - Error messages/logs (if applicable)

### Suggesting Features

We welcome feature suggestions! Please:
1. Check existing issues for similar requests
2. Create a new issue describing:
   - The feature and its use case
   - Why it would benefit users
   - Potential implementation approach (optional)

### Code Contributions

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ai-portfolio-manager.git
   cd ai-portfolio-manager
   ```

2. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

**Code Style**
- Follow PEP 8 Python style guide
- Use descriptive variable names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

**Example**:
```python
def calculate_portfolio_allocation(positions: List[Dict], total_value: float) -> List[Dict]:
    """
    Calculate allocation percentage for each position.

    Args:
        positions: List of position dictionaries with market_value
        total_value: Total portfolio value

    Returns:
        List of positions with added allocation_pct field
    """
    # Implementation
```

**Error Handling**
- Use try-except blocks for external API calls
- Return meaningful error messages
- Log errors for debugging but show user-friendly messages

```python
try:
    result = self.alpaca_client.get_position(symbol)
    return {'success': True, 'data': result}
except Exception as e:
    return {'success': False, 'error': f'Could not fetch position for {symbol}'}
```

**Function Declarations**
When adding new AI functions:
- Clear, descriptive name
- Detailed description
- Well-defined parameter schema
- Document defaults for optional parameters

```python
{
    'name': 'get_portfolio_risk_metrics',
    'description': 'Calculate portfolio risk metrics (volatility, beta, Sharpe ratio)',
    'parameters': {
        'type': 'object',
        'properties': {
            'period_days': {
                'type': 'integer',
                'description': 'Historical period for calculation (default: 30)'
            }
        }
    }
}
```

#### Testing

Currently, this project doesn't have automated tests (contributions welcome!). Before submitting:
- Test your changes manually with paper trading
- Verify all error cases are handled
- Check that the AI can call your new functions correctly
- Ensure no breaking changes to existing functionality

#### Submitting a Pull Request

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add portfolio risk metrics calculation"
   ```

   Use conventional commit prefixes:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes clearly
   - Link related issues (if any)

4. **Address Review Feedback**
   - Respond to reviewer comments
   - Make requested changes
   - Push updates to the same branch

## 📋 Areas Where We Need Help

### High Priority
- [ ] Unit tests for all modules
- [ ] Integration tests for API clients
- [ ] Performance optimization for large portfolios
- [ ] Better error messages for common issues

### Features
- [ ] Portfolio performance charts (ASCII art)
- [ ] Sector allocation analysis
- [ ] Risk metrics (volatility, beta, Sharpe ratio)
- [ ] Automated rebalancing suggestions
- [ ] Options trading support

### Documentation
- [ ] Video tutorial/walkthrough
- [ ] Troubleshooting guide
- [ ] API reference documentation
- [ ] Example conversation scenarios

### Infrastructure
- [ ] Docker containerization
- [ ] GitHub Actions CI/CD
- [ ] Code coverage reporting
- [ ] Automated dependency updates

## 🔒 Security Guidelines

- **Never commit API keys** - Always use .env files
- **Validate all inputs** - Sanitize user inputs before processing
- **Rate limiting** - Implement appropriate rate limits for new features
- **Safe defaults** - Paper trading should always be the default
- **Trade confirmation** - All trading operations must require explicit confirmation

## 📝 Code Review Process

All contributions will be reviewed for:
1. **Functionality** - Does it work as intended?
2. **Code quality** - Is it readable and maintainable?
3. **Error handling** - Are edge cases covered?
4. **Documentation** - Are docstrings clear and complete?
5. **Security** - Are there any security implications?

## 💡 Questions?

- Check the [Documentation](docs/)
- Review the [Development Guide](docs/DEVELOPMENT_GUIDE.md)
- Ask in GitHub Issues
- Review existing code for patterns and examples

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be recognized in the project README and release notes.

---

Thank you for helping make AI-powered portfolio management accessible to everyone! 🚀
