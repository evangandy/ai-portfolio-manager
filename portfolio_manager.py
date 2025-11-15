"""
AI Portfolio Manager - Main CLI Application
"""
import os
import sys
import warnings
import logging

# Suppress benign warnings BEFORE any imports
os.environ['GRPC_VERBOSITY'] = 'ERROR'  # Suppress GRPC/ALTS warnings
os.environ['GRPC_TRACE'] = ''           # Disable GRPC tracing
os.environ['GRPC_VERBOSITY'] = 'NONE'   # More aggressive GRPC suppression
os.environ['GLOG_minloglevel'] = '3'    # Suppress GLOG warnings (3 = FATAL only)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings if present

# Redirect stderr temporarily to suppress ALTS warning
import io
stderr_backup = sys.stderr
sys.stderr = io.StringIO()

# Now safe to import
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')
logging.getLogger('absl').setLevel(logging.CRITICAL)
logging.getLogger('google').setLevel(logging.CRITICAL)
logging.getLogger('grpc').setLevel(logging.CRITICAL)

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from core.alpaca_client import AlpacaClient
from core.gemini_agent import GeminiAgent
from core.ollama_agent import OllamaAgent
from core.news_fetcher import NewsFetcher

# Restore stderr after imports
sys.stderr = stderr_backup


class PortfolioManager:
    """
    Main CLI application for AI-powered portfolio management.
    """

    def __init__(self):
        """Initialize the portfolio manager with API clients."""
        # Load environment variables
        load_dotenv()

        # Get API keys and configuration
        self.alpaca_api_key = os.getenv('ALPACA_API_KEY')
        self.alpaca_secret_key = os.getenv('ALPACA_SECRET_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.ai_backend = os.getenv('AI_BACKEND', 'gemini').lower()
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1')
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

        # Validate Alpaca keys (always required)
        if not all([self.alpaca_api_key, self.alpaca_secret_key]):
            raise ValueError("Missing required Alpaca API keys in .env file")

        # Validate AI backend configuration
        if self.ai_backend == 'gemini' and not self.gemini_api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env file (required when AI_BACKEND=gemini)")

        # Initialize Rich console
        self.console = Console()

        # Rate limiting configuration
        self.MAX_TURNS = 20  # Maximum conversation turns per session
        self.MAX_MESSAGES_PER_MINUTE = 10  # Maximum messages per minute
        self.turn_count = 0
        self.message_times = []  # Track message timestamps for rate limiting

        # Initialize clients
        self.console.print("[yellow]Initializing API clients...[/yellow]")
        self.alpaca_client = AlpacaClient(
            self.alpaca_api_key,
            self.alpaca_secret_key,
            paper=True
        )

        # Initialize AI agent based on backend selection
        if self.ai_backend == 'ollama':
            self.console.print("[cyan]Using Ollama (local LLM) backend[/cyan]")
            self.ai_agent = OllamaAgent(
                self.alpaca_client,
                model=self.ollama_model,
                base_url=self.ollama_base_url
            )
        else:
            self.console.print("[cyan]Using Gemini API backend[/cyan]")
            try:
                self.ai_agent = GeminiAgent(
                    self.gemini_api_key,
                    self.alpaca_client
                )
            except Exception as e:
                # Fallback to Ollama if Gemini fails
                self.console.print(f"[yellow]Gemini initialization failed: {e}[/yellow]")
                self.console.print("[cyan]Falling back to Ollama backend...[/cyan]")
                self.ai_agent = OllamaAgent(
                    self.alpaca_client,
                    model=self.ollama_model,
                    base_url=self.ollama_base_url
                )

        self.news_fetcher = NewsFetcher(self.alpaca_client)

        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        os.makedirs('reports', exist_ok=True)

    def display_welcome_banner(self):
        """Display welcome banner and connection info."""
        banner_text = Text()
        banner_text.append("AI Portfolio Manager\n", style="bold cyan")
        banner_text.append("Connected to Alpaca (Paper Trading)\n", style="green")
        banner_text.append("\nCommands: ", style="white")
        banner_text.append("'update news'", style="yellow")
        banner_text.append(", ", style="white")
        banner_text.append("'report'", style="yellow")
        banner_text.append(", ", style="white")
        banner_text.append("'exit'", style="yellow")

        self.console.print(Panel(banner_text, border_style="cyan"))

    def display_portfolio_summary(self):
        """Display portfolio summary (cash and total value)."""
        try:
            summary = self.alpaca_client.get_portfolio_summary()

            if summary:
                portfolio_value = summary['portfolio_value']
                cash = summary['cash']

                self.console.print(f"\n💰 Portfolio Value: [bold green]${portfolio_value:,.2f}[/bold green]")
                self.console.print(f"💵 Cash Available: [bold cyan]${cash:,.2f}[/bold cyan]\n")
            else:
                self.console.print("[red]Could not retrieve portfolio summary[/red]\n")

        except Exception as e:
            self.console.print(f"[red]Error displaying portfolio: {e}[/red]\n")

    def update_news(self):
        """Fetch and save news for portfolio positions."""
        try:
            self.console.print("\n[yellow]Fetching latest news...[/yellow]")

            # Fetch news
            news_data = self.news_fetcher.fetch_portfolio_news(days=7)

            if not news_data:
                self.console.print("[yellow]No positions found or no news available[/yellow]\n")
                return

            # Display article counts
            for symbol, articles in news_data.items():
                count = len(articles)
                self.console.print(f"✓ {symbol} - {count} article{'s' if count != 1 else ''}")

            # Save markdown
            markdown_path = 'data/news.md'
            if self.news_fetcher.generate_markdown(news_data, markdown_path):
                self.console.print(f"\n[green]Saved to: {markdown_path}[/green]\n")
            else:
                self.console.print("[red]Error saving markdown file[/red]\n")

            # Also save JSON
            self.news_fetcher.save_json(news_data, 'data/news.json')

        except Exception as e:
            self.console.print(f"[red]Error updating news: {e}[/red]\n")

    def run(self):
        """Main application loop."""
        try:
            # Display welcome banner
            self.display_welcome_banner()

            # Display portfolio summary
            self.display_portfolio_summary()

            # Main chat loop
            while True:
                try:
                    # Get user input
                    user_input = self.console.input("[bold cyan]You:[/bold cyan] ").strip()

                    if not user_input:
                        continue

                    # Character limit validation (prevent system overload)
                    MAX_INPUT_LENGTH = 2000
                    if len(user_input) > MAX_INPUT_LENGTH:
                        self.console.print(
                            f"[red]Input too long! Maximum {MAX_INPUT_LENGTH} characters allowed. "
                            f"Your input: {len(user_input)} characters.[/red]\n"
                        )
                        continue

                    # Check for special commands (don't count toward limits)
                    if user_input.lower() == 'exit':
                        self.console.print("\n[cyan]Goodbye! Happy trading![/cyan]\n")
                        break

                    elif user_input.lower() == 'update news':
                        self.update_news()
                        continue

                    elif user_input.lower() == 'report':
                        self.console.print("\n[yellow]Report generation coming soon![/yellow]\n")
                        continue

                    # Rate limiting: Check turn limit
                    if self.turn_count >= self.MAX_TURNS:
                        self.console.print(
                            f"[yellow]Maximum conversation limit reached ({self.MAX_TURNS} turns). "
                            f"Please restart the application to continue.[/yellow]\n"
                        )
                        self.console.print("[cyan]Type 'exit' to quit.[/cyan]\n")
                        continue

                    # Rate limiting: Check messages per minute
                    import time
                    current_time = time.time()
                    
                    # Remove messages older than 1 minute
                    self.message_times = [t for t in self.message_times if current_time - t < 60]
                    
                    # Check if at rate limit
                    if len(self.message_times) >= self.MAX_MESSAGES_PER_MINUTE:
                        self.console.print(
                            f"[yellow]Rate limit reached! Maximum {self.MAX_MESSAGES_PER_MINUTE} messages per minute. "
                            f"Please wait a moment.[/yellow]\n"
                        )
                        continue
                    
                    # Add current message timestamp
                    self.message_times.append(current_time)
                    
                    # Increment turn counter
                    self.turn_count += 1

                    # Send to AI agent with error handling and fallback
                    try:
                        response = self.ai_agent.chat(user_input)
                    except Exception as e:
                        error_str = str(e)
                        # Check if it's a Gemini quota/credit error
                        if 'quota' in error_str.lower() or 'resource_exhausted' in error_str.lower() or '429' in error_str:
                            self.console.print("[yellow]Gemini API quota exhausted. Switching to Ollama...[/yellow]")
                            # Switch to Ollama
                            self.ai_agent = OllamaAgent(
                                self.alpaca_client,
                                model=self.ollama_model,
                                base_url=self.ollama_base_url
                            )
                            # Retry with Ollama
                            response = self.ai_agent.chat(user_input)
                        else:
                            raise

                    # Display AI response
                    self.console.print(f"[bold green]AI:[/bold green] {response}\n")

                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Use 'exit' to quit[/yellow]\n")
                    continue

                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/red]\n")
                    continue

        except KeyboardInterrupt:
            self.console.print("\n[cyan]Goodbye! Happy trading![/cyan]\n")

        except Exception as e:
            self.console.print(f"[red]Fatal error: {e}[/red]\n")


def main():
    """Entry point for the application."""
    try:
        manager = PortfolioManager()
        manager.run()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()