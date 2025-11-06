"""
News fetching and formatting utilities for portfolio stocks.
"""
from typing import Dict, List, Any
from datetime import datetime
import json


class NewsFetcher:
    """
    Fetch and format news for portfolio positions.
    """

    def __init__(self, alpaca_client):
        """
        Initialize news fetcher with Alpaca client.

        Args:
            alpaca_client: AlpacaClient instance
        """
        self.alpaca_client = alpaca_client

    def fetch_portfolio_news(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch news for all portfolio positions.

        Args:
            days: Number of days of news history

        Returns:
            Dict mapping symbol to list of news articles
        """
        try:
            # Get all positions
            positions = self.alpaca_client.get_positions()

            if not positions:
                return {}

            # Extract symbols
            symbols = [p['symbol'] for p in positions]

            # Fetch news for all symbols
            news_data = self.alpaca_client.get_news(symbols, days=days)

            return news_data

        except Exception as e:
            print(f"Error fetching portfolio news: {e}")
            return {}

    def generate_markdown(self, news_data: Dict[str, List[Dict[str, Any]]], output_path: str = 'data/news.md'):
        """
        Generate markdown file from news data.

        Args:
            news_data: Dict mapping symbol to news articles
            output_path: Path to save markdown file
        """
        try:
            lines = []
            lines.append("# Portfolio News Cache")
            lines.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")

            # Sort symbols alphabetically
            for symbol in sorted(news_data.keys()):
                articles = news_data[symbol]

                if not articles:
                    continue

                # Header for symbol
                lines.append(f"## {symbol} ({len(articles)} Articles)")
                lines.append("")

                # Show top 5 articles
                for i, article in enumerate(articles[:5], 1):
                    lines.append(f"**{article['headline']}**")
                    lines.append(f"- Source: {article['author'] or 'Unknown'}")

                    # Calculate time ago
                    created_at = article['created_at']
                    if isinstance(created_at, str):
                        try:
                            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        except:
                            created_at = datetime.now()

                    age = self._format_age(self._hours_ago(created_at))
                    lines.append(f"- Published: {created_at.strftime('%Y-%m-%d %H:%M')} ({age})")

                    if article['summary']:
                        lines.append(f"- Summary: {article['summary']}")

                    if article['url']:
                        lines.append(f"- URL: {article['url']}")

                    lines.append("")

                # Show count of additional articles
                if len(articles) > 5:
                    lines.append(f"*...and {len(articles) - 5} more articles*")
                    lines.append("")

                lines.append("---")
                lines.append("")

            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            return True

        except Exception as e:
            print(f"Error generating markdown: {e}")
            return False

    def save_json(self, news_data: Dict[str, List[Dict[str, Any]]], output_path: str = 'data/news.json'):
        """
        Save news data as JSON.

        Args:
            news_data: Dict mapping symbol to news articles
            output_path: Path to save JSON file
        """
        try:
            # Convert datetime objects to strings for JSON serialization
            serializable_data = {}
            for symbol, articles in news_data.items():
                serializable_data[symbol] = [
                    {
                        'headline': a['headline'],
                        'summary': a['summary'],
                        'author': a['author'],
                        'url': a['url'],
                        'created_at': str(a['created_at']),
                        'symbols': a.get('symbols', [])
                    }
                    for a in articles
                ]

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False

    def _hours_ago(self, timestamp: datetime) -> float:
        """
        Calculate hours since timestamp.

        Args:
            timestamp: DateTime to compare

        Returns:
            Hours elapsed
        """
        if not isinstance(timestamp, datetime):
            return 0

        now = datetime.now(timestamp.tzinfo) if timestamp.tzinfo else datetime.now()
        delta = now - timestamp
        return delta.total_seconds() / 3600

    def _format_age(self, hours: float) -> str:
        """
        Format hours into human-readable age string.

        Args:
            hours: Number of hours

        Returns:
            Formatted string (e.g., "2 hours ago", "3 days ago")
        """
        if hours < 1:
            minutes = int(hours * 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif hours < 24:
            hours_int = int(hours)
            return f"{hours_int} hour{'s' if hours_int != 1 else ''} ago"
        else:
            days = int(hours / 24)
            return f"{days} day{'s' if days != 1 else ''} ago"
