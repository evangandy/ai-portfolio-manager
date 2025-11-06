"""
Alpaca API client wrapper for trading, market data, and news operations.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.data import StockHistoricalDataClient, NewsClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest, NewsRequest
from alpaca.data.timeframe import TimeFrame


class AlpacaClient:
    """
    Unified wrapper for Alpaca Trading, Market Data, and News APIs.
    """

    def __init__(self, api_key: str, secret_key: str, paper: bool = True):
        """
        Initialize Alpaca client with API credentials.

        Args:
            api_key: Alpaca API key
            secret_key: Alpaca secret key
            paper: Whether to use paper trading (default: True)
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.paper = paper

        # Initialize clients
        self.trading_client = TradingClient(api_key, secret_key, paper=paper)
        self.data_client = StockHistoricalDataClient(api_key, secret_key)
        self.news_client = NewsClient(api_key, secret_key)

    # ==================== Account Operations ====================

    def get_account(self) -> Optional[Dict[str, Any]]:
        """
        Get account information.

        Returns:
            Dict with account info (cash, portfolio_value, buying_power) or None on error
        """
        try:
            account = self.trading_client.get_account()
            return {
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'buying_power': float(account.buying_power),
                'equity': float(account.equity)
            }
        except Exception as e:
            print(f"Error getting account: {e}")
            return None

    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Get all open positions.

        Returns:
            List of position dicts or empty list on error
        """
        try:
            positions = self.trading_client.get_all_positions()
            return [
                {
                    'symbol': p.symbol,
                    'qty': float(p.qty),
                    'market_value': float(p.market_value),
                    'avg_entry_price': float(p.avg_entry_price),
                    'current_price': float(p.current_price),
                    'unrealized_pl': float(p.unrealized_pl),
                    'unrealized_plpc': float(p.unrealized_plpc)
                }
                for p in positions
            ]
        except Exception as e:
            print(f"Error getting positions: {e}")
            return []

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get specific position by symbol.

        Args:
            symbol: Stock symbol (e.g., 'AAPL')

        Returns:
            Position dict or None if not found/error
        """
        try:
            position = self.trading_client.get_open_position(symbol)
            return {
                'symbol': position.symbol,
                'qty': float(position.qty),
                'market_value': float(position.market_value),
                'avg_entry_price': float(position.avg_entry_price),
                'current_price': float(position.current_price),
                'unrealized_pl': float(position.unrealized_pl),
                'unrealized_plpc': float(position.unrealized_plpc)
            }
        except Exception as e:
            print(f"Error getting position for {symbol}: {e}")
            return None

    # ==================== Trading Operations ====================

    def place_market_order(self, symbol: str, qty: float, side: str) -> Optional[Dict[str, Any]]:
        """
        Place a market order.

        Args:
            symbol: Stock symbol
            qty: Quantity to trade
            side: 'buy' or 'sell'

        Returns:
            Order dict or None on error
        """
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL

            request = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.DAY
            )

            order = self.trading_client.submit_order(request)
            return {
                'id': str(order.id),
                'symbol': order.symbol,
                'qty': float(order.qty),
                'side': order.side.value,
                'type': order.type.value,
                'status': order.status.value,
                'created_at': str(order.created_at)
            }
        except Exception as e:
            print(f"Error placing market order: {e}")
            return None

    def place_limit_order(self, symbol: str, qty: float, side: str, limit_price: float) -> Optional[Dict[str, Any]]:
        """
        Place a limit order.

        Args:
            symbol: Stock symbol
            qty: Quantity to trade
            side: 'buy' or 'sell'
            limit_price: Limit price

        Returns:
            Order dict or None on error
        """
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL

            request = LimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.DAY,
                limit_price=limit_price
            )

            order = self.trading_client.submit_order(request)
            return {
                'id': str(order.id),
                'symbol': order.symbol,
                'qty': float(order.qty),
                'side': order.side.value,
                'type': order.type.value,
                'limit_price': float(order.limit_price),
                'status': order.status.value,
                'created_at': str(order.created_at)
            }
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return None

    def get_orders(self, status: str = 'all') -> List[Dict[str, Any]]:
        """
        Get orders filtered by status.

        Args:
            status: 'open', 'closed', or 'all'

        Returns:
            List of order dicts or empty list on error
        """
        try:
            if status == 'open':
                query_status = QueryOrderStatus.OPEN
            elif status == 'closed':
                query_status = QueryOrderStatus.CLOSED
            else:
                query_status = QueryOrderStatus.ALL

            from alpaca.trading.requests import GetOrdersRequest
            request = GetOrdersRequest(status=query_status)
            orders = self.trading_client.get_orders(filter=request)
            return [
                {
                    'id': str(o.id),
                    'symbol': o.symbol,
                    'qty': float(o.qty),
                    'side': o.side.value,
                    'type': o.type.value,
                    'status': o.status.value,
                    'created_at': str(o.created_at)
                }
                for o in orders
            ]
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []

    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel a specific order.

        Args:
            order_id: Order ID to cancel

        Returns:
            True if successful, False otherwise
        """
        try:
            self.trading_client.cancel_order_by_id(order_id)
            return True
        except Exception as e:
            print(f"Error canceling order: {e}")
            return False

    # ==================== Market Data ====================

    def get_latest_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get the latest quote for a symbol.

        Args:
            symbol: Stock symbol

        Returns:
            Quote dict with bid/ask prices or None on error
        """
        try:
            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quotes = self.data_client.get_stock_latest_quote(request)
            quote = quotes[symbol]

            # Convert timestamp to string
            timestamp = quote.timestamp
            if hasattr(timestamp, 'isoformat'):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)

            return {
                'symbol': symbol,
                'bid_price': float(quote.bid_price),
                'ask_price': float(quote.ask_price),
                'bid_size': float(quote.bid_size),
                'ask_size': float(quote.ask_size),
                'timestamp': timestamp
            }
        except Exception as e:
            print(f"Error getting quote for {symbol}: {e}")
            return None

    def get_bars(self, symbol: str, days: int = 30, timeframe: str = '1Day') -> List[Dict[str, Any]]:
        """
        Get historical price bars.

        Args:
            symbol: Stock symbol
            days: Number of days of history
            timeframe: Bar timeframe (e.g., '1Day', '1Hour')

        Returns:
            List of bar dicts or empty list on error
        """
        try:
            # Map timeframe string to TimeFrame enum
            if timeframe == '1Day':
                tf = TimeFrame.Day
            elif timeframe == '1Hour':
                tf = TimeFrame.Hour
            else:
                tf = TimeFrame.Day

            start = datetime.now() - timedelta(days=days)

            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=tf,
                start=start
            )

            bars = self.data_client.get_stock_bars(request)

            return [
                {
                    'timestamp': bar.timestamp.isoformat() if hasattr(bar.timestamp, 'isoformat') else str(bar.timestamp),
                    'open': float(bar.open),
                    'high': float(bar.high),
                    'low': float(bar.low),
                    'close': float(bar.close),
                    'volume': float(bar.volume)
                }
                for bar in bars[symbol]
            ]
        except Exception as e:
            print(f"Error getting bars for {symbol}: {e}")
            return []

    # ==================== News Operations ====================

    def get_news(self, symbols: List[str], days: int = 7, limit: int = 50) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get news articles for symbols.

        Args:
            symbols: List of stock symbols
            days: Number of days of news history
            limit: Max number of articles per symbol

        Returns:
            Dict mapping symbol to list of article dicts
        """
        try:
            start = datetime.now() - timedelta(days=days)

            # Convert list to comma-separated string if needed
            symbols_param = ','.join(symbols) if isinstance(symbols, list) else symbols

            request = NewsRequest(
                symbols=symbols_param,
                start=start,
                limit=limit
            )

            news_response = self.news_client.get_news(request)

            # Extract news articles from response (NewsSet.data['news'])
            news_articles = news_response.data.get('news', []) if hasattr(news_response, 'data') else []

            # Group news by symbol
            news_by_symbol = {symbol: [] for symbol in symbols}

            for article in news_articles:
                try:
                    # Articles are already dictionaries from the API response
                    if isinstance(article, dict):
                        article_dict = article.copy()
                    else:
                        # If they're objects, extract attributes
                        article_dict = {
                            'headline': getattr(article, 'headline', 'No headline'),
                            'summary': getattr(article, 'summary', ''),
                            'author': getattr(article, 'author', 'Unknown'),
                            'url': getattr(article, 'url', ''),
                            'created_at': getattr(article, 'created_at', None),
                            'symbols': getattr(article, 'symbols', [])
                        }

                    # Convert datetime to string for JSON serialization
                    if 'created_at' in article_dict and article_dict['created_at']:
                        if hasattr(article_dict['created_at'], 'isoformat'):
                            article_dict['created_at'] = article_dict['created_at'].isoformat()
                        else:
                            article_dict['created_at'] = str(article_dict['created_at'])
                    
                    # Ensure all values are serializable
                    article_dict['headline'] = str(article_dict.get('headline', 'No headline'))
                    article_dict['summary'] = str(article_dict.get('summary', ''))
                    article_dict['author'] = str(article_dict.get('author', 'Unknown'))
                    article_dict['url'] = str(article_dict.get('url', ''))
                    
                    # Ensure symbols is a list of strings
                    symbols_list = article_dict.get('symbols', [])
                    if not isinstance(symbols_list, list):
                        symbols_list = [str(symbols_list)]
                    article_dict['symbols'] = [str(s) for s in symbols_list]

                    # Add article to each relevant symbol
                    for symbol in article_dict['symbols']:
                        if symbol in news_by_symbol:
                            news_by_symbol[symbol].append(article_dict)
                            
                except Exception as article_error:
                    print(f"Error processing article: {article_error}")
                    continue

            return news_by_symbol
        except Exception as e:
            print(f"Error getting news: {e}")
            return {symbol: [] for symbol in symbols}

    # ==================== Portfolio Analysis ====================

    def get_best_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top performing positions by unrealized profit/loss percentage.

        Args:
            limit: Number of positions to return

        Returns:
            List of position dicts sorted by performance
        """
        try:
            positions = self.get_positions()
            # Sort by unrealized profit/loss percentage, descending
            positions.sort(key=lambda p: p.get('unrealized_plpc', 0), reverse=True)
            return positions[:limit]
        except Exception as e:
            print(f"Error getting best performers: {e}")
            return []

    def get_worst_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get worst performing positions by unrealized profit/loss percentage.

        Args:
            limit: Number of positions to return

        Returns:
            List of position dicts sorted by performance
        """
        try:
            positions = self.get_positions()
            # Sort by unrealized profit/loss percentage, ascending
            positions.sort(key=lambda p: p.get('unrealized_plpc', 0))
            return positions[:limit]
        except Exception as e:
            print(f"Error getting worst performers: {e}")
            return []

    # ==================== Helper Methods ====================

    def get_portfolio_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get complete portfolio summary with account and positions.

        Returns:
            Dict with cash, portfolio_value, equity, buying_power, and positions list
        """
        try:
            account = self.get_account()
            positions = self.get_positions()

            if account is None:
                return None

            return {
                'cash': account['cash'],
                'portfolio_value': account['portfolio_value'],
                'equity': account['equity'],
                'buying_power': account['buying_power'],
                'positions': positions
            }
        except Exception as e:
            print(f"Error getting portfolio summary: {e}")
            return None

    def get_position_allocation(self) -> List[Dict[str, Any]]:
        """
        Get portfolio allocation by position (percentage breakdown).

        Returns:
            List of positions with allocation percentages
        """
        try:
            account = self.get_account()
            positions = self.get_positions()

            if not account or not positions:
                return []

            portfolio_value = account['portfolio_value']
            
            allocations = []
            for position in positions:
                allocation_pct = (position['market_value'] / portfolio_value) * 100 if portfolio_value > 0 else 0
                allocations.append({
                    'symbol': position['symbol'],
                    'market_value': position['market_value'],
                    'allocation_pct': allocation_pct,
                    'qty': position['qty']
                })

            # Sort by allocation percentage descending
            allocations.sort(key=lambda x: x['allocation_pct'], reverse=True)
            return allocations

        except Exception as e:
            print(f"Error getting position allocation: {e}")
            return []

    def calculate_shares_from_dollars(self, symbol: str, dollar_amount: float) -> Optional[Dict[str, Any]]:
        """
        Calculate how many shares can be purchased with a dollar amount.

        Args:
            symbol: Stock symbol
            dollar_amount: Dollar amount to invest

        Returns:
            Dict with shares and estimated cost
        """
        try:
            quote = self.get_latest_quote(symbol)
            if not quote:
                return None

            ask_price = quote['ask_price']
            if ask_price <= 0:
                return None

            shares = dollar_amount / ask_price
            estimated_cost = shares * ask_price

            return {
                'symbol': symbol,
                'dollar_amount': dollar_amount,
                'ask_price': ask_price,
                'shares': shares,
                'whole_shares': int(shares),
                'estimated_cost': estimated_cost,
                'estimated_cost_whole': int(shares) * ask_price
            }

        except Exception as e:
            print(f"Error calculating shares from dollars: {e}")
            return None

    def get_total_return(self) -> Optional[Dict[str, Any]]:
        """
        Calculate total portfolio return metrics.

        Returns:
            Dict with total P&L, percentage return, and position count
        """
        try:
            positions = self.get_positions()
            if not positions:
                return {
                    'total_unrealized_pl': 0,
                    'total_market_value': 0,
                    'total_cost_basis': 0,
                    'total_return_pct': 0,
                    'position_count': 0,
                    'winning_positions': 0,
                    'losing_positions': 0
                }

            total_unrealized_pl = sum(p['unrealized_pl'] for p in positions)
            total_market_value = sum(p['market_value'] for p in positions)
            total_cost_basis = sum(p['qty'] * p['avg_entry_price'] for p in positions)
            
            total_return_pct = (total_unrealized_pl / total_cost_basis * 100) if total_cost_basis > 0 else 0
            
            winning_positions = sum(1 for p in positions if p['unrealized_pl'] > 0)
            losing_positions = sum(1 for p in positions if p['unrealized_pl'] < 0)

            return {
                'total_unrealized_pl': total_unrealized_pl,
                'total_market_value': total_market_value,
                'total_cost_basis': total_cost_basis,
                'total_return_pct': total_return_pct,
                'position_count': len(positions),
                'winning_positions': winning_positions,
                'losing_positions': losing_positions
            }

        except Exception as e:
            print(f"Error calculating total return: {e}")
            return None

    def get_largest_position(self) -> Optional[Dict[str, Any]]:
        """
        Get the largest position by market value.

        Returns:
            Position dict or None
        """
        try:
            positions = self.get_positions()
            if not positions:
                return None

            return max(positions, key=lambda p: p['market_value'])

        except Exception as e:
            print(f"Error getting largest position: {e}")
            return None

    def get_smallest_position(self) -> Optional[Dict[str, Any]]:
        """
        Get the smallest position by market value.

        Returns:
            Position dict or None
        """
        try:
            positions = self.get_positions()
            if not positions:
                return None

            return min(positions, key=lambda p: p['market_value'])

        except Exception as e:
            print(f"Error getting smallest position: {e}")
            return None

    def get_concentrated_positions(self, threshold_pct: float = 20.0) -> List[Dict[str, Any]]:
        """
        Get positions that exceed a certain percentage of portfolio.

        Args:
            threshold_pct: Percentage threshold (default 20%)

        Returns:
            List of concentrated positions with allocation percentages
        """
        try:
            allocations = self.get_position_allocation()
            return [p for p in allocations if p['allocation_pct'] >= threshold_pct]

        except Exception as e:
            print(f"Error getting concentrated positions: {e}")
            return []
