"""
Ollama AI agent with function calling capabilities as fallback for Gemini.
Uses local LLMs via Ollama for when API credits run out.
"""
from typing import Dict, Any, List
import json
import requests


class OllamaAgent:
    """
    AI agent using Ollama (local LLM) with function calling for portfolio interaction.
    This serves as a fallback when Gemini API credits are exhausted.
    """

    def __init__(self, alpaca_client, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama agent with Alpaca client.

        Args:
            alpaca_client: AlpacaClient instance for executing functions
            model: Ollama model name (default: llama3.1)
            base_url: Ollama API base URL (default: http://localhost:11434)
        """
        self.alpaca_client = alpaca_client
        self.model = model
        self.base_url = base_url
        self.conversation_history = []

        # System instruction (same as Gemini for consistency)
        self.system_instruction = """You are an AI portfolio assistant with access to the user's Alpaca trading account. You can:
- View portfolio positions, account details, and performance metrics
- Get stock quotes, historical data, and news
- Analyze portfolio allocation, concentration, and returns
- Execute trades (market and limit orders) after user confirmation
- Provide financial insights and recommendations

CRITICAL: You are outputting to a TERMINAL, not a markdown renderer. Format responses for plain text readability.

CRITICAL FUNCTION CALLING RULES - READ CAREFULLY:
1. You have DIRECT ACCESS to data through functions - USE THEM IMMEDIATELY
2. NEVER ask the user for information you can get yourself (positions, quotes, news, etc.)
3. When you need data, you MUST use function calling format
4. NEVER output code blocks showing function calls (no ```, no print(), no tool_code)
5. After getting function results, use the ACTUAL RESULT DATA in your response
6. The user ONLY sees your final text response - not the function calls

AVAILABLE FUNCTIONS - YOU MUST USE THESE:
- get_all_positions: Get all current stock positions (NO ARGS NEEDED)
- get_account_info: Get account cash, portfolio value, buying power (NO ARGS NEEDED)
- get_stock_quote: Get current price (args: symbol)
- get_stock_news: Get recent news (args: symbols as array, days)
- place_market_order: Place order (args: symbol, qty, side)
- calculate_dollar_amount: Calculate shares from dollars (args: symbol, dollar_amount)
- get_portfolio_summary: Complete portfolio analysis (NO ARGS NEEDED)
- get_position_allocation: Portfolio breakdown (NO ARGS NEEDED)
- get_best_performers: Top performers (args: limit)
- get_worst_performers: Worst performers (args: limit)

FUNCTION CALLING FORMAT:
When you need to call a function, output ONLY this JSON format on a single line:
{"function": "function_name", "args": {"arg1": "value1", "arg2": "value2"}}

If no args needed, use empty object:
{"function": "get_all_positions", "args": {}}

EXAMPLES:
To get positions: {"function": "get_all_positions", "args": {}}
To get news: {"function": "get_stock_news", "args": {"symbols": ["AAPL", "TSLA"], "days": 7}}
To get quote: {"function": "get_stock_quote", "args": {"symbol": "AAPL"}}

MULTI-STEP TASK EXECUTION - IMPORTANT LIMITATIONS:
You are running on Ollama (local LLM) which has limitations:
- You can handle 2-3 function calls per request maximum
- For complex multi-step tasks, break them into phases
- After completing 2-3 steps, tell the user what you did and what still needs to be done
- Ask them to confirm to continue with the next phase

WORKFLOW FOR COMPLEX REQUESTS:
1. Do first 2-3 steps (e.g., get positions, get news, analyze)
2. Report what you found
3. Say: "I've completed the first phase. To continue with [next steps], please respond 'continue' or tell me to proceed."
4. Wait for user confirmation before executing trades

ALWAYS start by getting positions with get_all_positions if the user asks about "my stocks".

RESPONSE FORMATTING RULES - CRITICAL:
1. DO NOT use markdown syntax (NEVER use *, **, #, ##, etc.)
2. DO NOT output code blocks (NEVER use ```)
3. DO NOT show the user the JSON function call syntax
4. DO NOT explain what you're going to do - JUST DO IT
5. The user CANNOT see function calls - they are invisible to them
3. Use simple plain text formatting:
   - Use line breaks for readability
   - Use indentation (2-4 spaces) for sub-items
   - Use simple bullets: • or -
   - Use CAPS for emphasis
4. Format money: $1,234.56
5. Format percentages: 12.5% or +8.4%
6. Keep responses concise (2-4 sentences for simple queries)

Be conversational, helpful, and financially prudent. Always explain your reasoning.
When discussing money, use proper formatting ($1,234.56).

Keep responses concise but informative."""

        # Available functions (same as Gemini)
        self.available_functions = {
            'get_account_info': 'Get account cash, portfolio value, buying power',
            'get_all_positions': 'Get all current stock positions',
            'get_position': 'Get details on a specific position (args: symbol)',
            'get_stock_quote': 'Get current price and quote for a stock (args: symbol)',
            'get_stock_bars': 'Get historical price data (args: symbol, days)',
            'place_market_order': 'Place a market order (args: symbol, qty, side)',
            'get_orders': 'Get order history (args: status)',
            'cancel_order': 'Cancel a pending order (args: order_id)',
            'get_stock_news': 'Get recent news for stocks (args: symbols, days)',
            'get_portfolio_summary': 'Get complete portfolio analysis',
            'get_best_performers': 'Get top performing positions (args: limit)',
            'get_worst_performers': 'Get worst performing positions (args: limit)',
            'get_position_allocation': 'Get portfolio breakdown by position',
            'get_total_return': 'Get total portfolio return and P&L',
            'get_largest_position': 'Get the largest position by market value',
            'get_smallest_position': 'Get the smallest position by market value',
            'get_concentrated_positions': 'Get positions exceeding threshold (args: threshold_pct)',
            'calculate_dollar_amount': 'Calculate shares for dollar amount (args: symbol, dollar_amount)',
            'place_limit_order': 'Place a limit order (args: symbol, qty, side, limit_price)',
        }

    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def _execute_function(self, function_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function call (reuses Gemini agent's implementation logic).

        Args:
            function_name: Name of the function to execute
            args: Function arguments

        Returns:
            Function result as dict
        """
        try:
            result = None

            if function_name == 'get_account_info':
                result = self.alpaca_client.get_account()
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'Could not retrieve account info'}

            elif function_name == 'get_all_positions':
                result = self.alpaca_client.get_positions()
                return {'success': True, 'data': result}

            elif function_name == 'get_position':
                symbol = str(args.get('symbol', '')).upper().strip()
                if not symbol:
                    return {'success': False, 'error': 'Symbol is required'}
                result = self.alpaca_client.get_position(symbol)
                return {'success': True, 'data': result} if result else {'success': False, 'error': f'No position found for {symbol}'}

            elif function_name == 'get_stock_quote':
                symbol = str(args.get('symbol', '')).upper().strip()
                if not symbol:
                    return {'success': False, 'error': 'Symbol is required'}
                result = self.alpaca_client.get_latest_quote(symbol)
                return {'success': True, 'data': result} if result else {'success': False, 'error': f'Could not retrieve quote for {symbol}'}

            elif function_name == 'get_stock_bars':
                symbol = str(args.get('symbol', '')).upper().strip()
                if not symbol:
                    return {'success': False, 'error': 'Symbol is required'}
                days = int(args.get('days', 30))
                result = self.alpaca_client.get_bars(symbol, days=days)
                return {'success': True, 'data': result}

            elif function_name == 'place_market_order':
                symbol = str(args.get('symbol', '')).upper().strip()
                qty = float(args.get('qty', 0))
                side = str(args.get('side', 'buy')).lower()

                if not symbol or qty <= 0:
                    return {'success': False, 'error': 'Valid symbol and quantity required'}

                result = self.alpaca_client.place_market_order(symbol, qty, side)
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'Failed to place order'}

            elif function_name == 'get_orders':
                status = str(args.get('status', 'all')).lower()
                result = self.alpaca_client.get_orders(status)
                return {'success': True, 'data': result}

            elif function_name == 'cancel_order':
                order_id = str(args.get('order_id', ''))
                if not order_id:
                    return {'success': False, 'error': 'Order ID is required'}
                result = self.alpaca_client.cancel_order(order_id)
                return {'success': result}

            elif function_name == 'get_stock_news':
                symbols = args.get('symbols', [])
                if isinstance(symbols, str):
                    symbols = [symbols]
                symbols = [str(s).upper().strip() for s in symbols if s]

                if not symbols:
                    return {'success': False, 'error': 'At least one symbol is required'}

                days = int(args.get('days', 7))
                result = self.alpaca_client.get_news(symbols, days=days)
                return {'success': True, 'data': result}

            elif function_name == 'get_portfolio_summary':
                result = self.alpaca_client.get_portfolio_summary()
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'Could not retrieve portfolio summary'}

            elif function_name == 'get_best_performers':
                limit = int(args.get('limit', 5))
                result = self.alpaca_client.get_best_performers(limit)
                return {'success': True, 'data': result}

            elif function_name == 'get_worst_performers':
                limit = int(args.get('limit', 5))
                result = self.alpaca_client.get_worst_performers(limit)
                return {'success': True, 'data': result}

            elif function_name == 'get_position_allocation':
                result = self.alpaca_client.get_position_allocation()
                return {'success': True, 'data': result}

            elif function_name == 'get_total_return':
                result = self.alpaca_client.get_total_return()
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'Could not calculate total return'}

            elif function_name == 'get_largest_position':
                result = self.alpaca_client.get_largest_position()
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'No positions found'}

            elif function_name == 'get_smallest_position':
                result = self.alpaca_client.get_smallest_position()
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'No positions found'}

            elif function_name == 'get_concentrated_positions':
                threshold_pct = float(args.get('threshold_pct', 20.0))
                result = self.alpaca_client.get_concentrated_positions(threshold_pct)
                return {'success': True, 'data': result}

            elif function_name == 'calculate_dollar_amount':
                symbol = str(args.get('symbol', '')).upper().strip()
                dollar_amount = float(args.get('dollar_amount', 0))

                if not symbol or dollar_amount <= 0:
                    return {'success': False, 'error': 'Valid symbol and dollar amount required'}

                result = self.alpaca_client.calculate_shares_from_dollars(symbol, dollar_amount)
                return {'success': True, 'data': result} if result else {'success': False, 'error': f'Could not calculate shares for {symbol}'}

            elif function_name == 'place_limit_order':
                symbol = str(args.get('symbol', '')).upper().strip()
                qty = float(args.get('qty', 0))
                side = str(args.get('side', 'buy')).lower()
                limit_price = float(args.get('limit_price', 0))

                if not symbol or qty <= 0 or limit_price <= 0:
                    return {'success': False, 'error': 'Valid symbol, quantity, and limit price required'}

                result = self.alpaca_client.place_limit_order(symbol, qty, side, limit_price)
                return {'success': True, 'data': result} if result else {'success': False, 'error': 'Failed to place limit order'}

            else:
                return {'success': False, 'error': f'Unknown function: {function_name}'}

        except ValueError as ve:
            return {'success': False, 'error': f'Invalid argument: {str(ve)}'}
        except Exception as e:
            return {'success': False, 'error': f'Function execution error: {str(e)}'}

    def _clean_response(self, text: str) -> str:
        """
        Clean the response text by removing markdown and exposed function calls.

        Args:
            text: Raw response text

        Returns:
            Cleaned response text
        """
        import re

        # Remove markdown bold (**text**)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

        # Remove markdown italic (*text* or _text_)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)

        # Remove markdown headers (# ## ###)
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        # Remove exposed JSON function calls
        text = re.sub(r'\{"function":\s*"[^"]+",\s*"args":\s*\{[^}]*\}\}', '', text)

        # Remove code blocks
        text = re.sub(r'```[a-z]*\n.*?```', '', text, flags=re.DOTALL)

        # Remove inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

        return text.strip()

    def _parse_function_call(self, text: str) -> tuple[str, Dict[str, Any]] | None:
        """
        Parse function call from LLM output.

        Args:
            text: LLM output text

        Returns:
            Tuple of (function_name, args) or None if no valid function call
        """
        try:
            # Look for JSON function call format
            lines = text.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('{') and '"function"' in line:
                    data = json.loads(line)
                    if 'function' in data:
                        return data['function'], data.get('args', {})
        except Exception:
            pass
        return None

    def chat(self, user_message: str) -> str:
        """
        Main chat interface - send message and get response.

        Args:
            user_message: User's message

        Returns:
            AI's text response
        """
        # Check if Ollama is available
        if not self._check_ollama_available():
            return "Error: Ollama is not running. Please start Ollama with 'ollama serve' and ensure the model is installed."

        try:
            # Add user message to history
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })

            # Prepare messages for Ollama
            messages = [
                {'role': 'system', 'content': self.system_instruction},
                *self.conversation_history
            ]

            # Call Ollama API
            # Limited iterations for Ollama due to function calling limitations
            max_iterations = 5  # Ollama handles fewer steps than Gemini
            iteration = 0

            while iteration < max_iterations:
                # Generate response
                response = requests.post(
                    f"{self.base_url}/api/chat",
                    json={
                        'model': self.model,
                        'messages': messages,
                        'stream': False
                    },
                    timeout=30
                )

                if response.status_code != 200:
                    return f"Error calling Ollama API: {response.status_code}"

                result = response.json()
                assistant_message = result['message']['content']

                # Check if there's a function call
                function_call = self._parse_function_call(assistant_message)

                if function_call:
                    function_name, args = function_call

                    # Execute function
                    function_result = self._execute_function(function_name, args)

                    # Add function result to conversation
                    messages.append({
                        'role': 'assistant',
                        'content': assistant_message
                    })
                    messages.append({
                        'role': 'user',
                        'content': f"Function result: {json.dumps(function_result)}"
                    })

                    iteration += 1
                else:
                    # No function call, this is the final response
                    # Clean up markdown and exposed function calls
                    cleaned_message = self._clean_response(assistant_message)

                    self.conversation_history.append({
                        'role': 'assistant',
                        'content': cleaned_message
                    })
                    return cleaned_message

            # If we hit max iterations, give helpful message
            return ("I've reached my function calling limit (Ollama can handle 2-3 steps at a time). "
                   "I need you to break this into smaller tasks:\n\n"
                   "Example workflow:\n"
                   "1. First ask: 'Get news on my stocks and tell me which have bad news'\n"
                   "2. Then ask: 'Sell half my shares in [STOCK]'\n"
                   "3. Then ask: 'Buy equal parts SCHD and TLT with the proceeds'\n\n"
                   "Or switch to Gemini for complex multi-step tasks: ./switch_ai.sh gemini")

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Please ensure Ollama is running with 'ollama serve'."
        except Exception as e:
            return f"Error: {str(e)}"

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
