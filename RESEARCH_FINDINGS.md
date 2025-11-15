# Research Findings: Gemini Function Calling Issues

## Problems Identified

### 1. Gemini Printing Tool Calls Instead of Executing Them
This is a **known issue** across multiple platforms (n8n, AutoGen, custom implementations). Users report that Gemini models output code blocks like:
```
```tool_code
print(get_news(symbols=["AAPL"]))
```
```
Instead of actually calling the function.

### 2. AI Asking for Data It Can Fetch
Gemini often asks users "What stocks do you own?" instead of calling `get_all_positions()` to retrieve the data itself.

### 3. Function Calling Hallucinations
Gemini 2.0 Flash has been reported to have intermittent function calling hallucinations where it claims to make a function call but doesn't actually execute it.

---

## Solutions from the Community

### 1. System Prompt Improvements
**Source**: n8n Community Forum

**Key Finding**: Be "explicit in the system prompt and user prompt to NOT wrap any values or tool calls in formatting strings / backticks"

**Recommendation**:
- Explicitly forbid code blocks in system instructions
- Add negative examples showing what NOT to do
- Emphasize that function calls are invisible to users

### 2. Configuration Options
**Source**: Google AI Forums, Official Documentation

**Key Settings**:

```python
config = types.GenerateContentConfig(
    tools=tools,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=False  # Enable automatic execution
    ),
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode='AUTO'  # or 'ANY' to force function calls
        )
    ),
    temperature=0  # Low temperature for deterministic behavior
)
```

**Function Calling Modes**:
- `AUTO` (default): Model decides between natural language and function calls
- `ANY`: Forces the model to always predict a function call
- `NONE`: Prohibits function calls completely
- `VALIDATED`: Constrains model to function calls or natural language

### 3. Pass Callable Functions Directly
**Source**: GitHub Issue #859

Instead of JSON schema declarations, pass actual Python functions:

```python
config = types.GenerateContentConfig(
    system_instruction="You are a helpful assistant...",
    tools=[get_menu, order_pizza, check_order_status],  # Actual functions
)
```

**Benefits**:
- SDK handles argument extraction and function invocation
- Returns final result in natural language
- Reduces hallucinations

### 4. Function Design Best Practices
**Source**: Official Gemini Documentation

**Recommendations**:
- **Clear descriptions**: Be extremely specific about what each function does
- **Python-friendly names**: Use snake_case, no spaces or special characters
- **Strong typing**: Use type hints and specific parameter types
- **Limit tools**: Keep active tools to 10-20 relevant functions
- **Low temperature**: Use temperature=0 for deterministic function calls

### 5. Proactive Function Calling in System Instructions
**Source**: Prompt Engineering Guide, Martin Fowler Articles

**Best Practices**:
- Tell the model to autonomously fetch data without asking users
- Provide concrete examples of correct vs incorrect behavior
- Emphasize that the model should "think" in terms of function calls
- Include instructions like:
  - "You have DIRECT ACCESS to data through functions - USE THEM IMMEDIATELY"
  - "NEVER ask the user for information you can get yourself"
  - "When you need data, SILENTLY CALL THE FUNCTION"

### 6. Post-Processing Response Cleanup
**Source**: Community workarounds

Since Gemini sometimes ignores system instructions, implement a cleanup filter:

```python
import re

def clean_response(text):
    # Remove code blocks
    text = re.sub(r'```[a-z_]*\n.*?```', '', text, flags=re.DOTALL)
    # Remove inline function calls
    text = re.sub(r'`[^`]*\([^)]*\)`', '', text)
    # Remove print statements
    text = re.sub(r'^.*print\(.*\).*$', '', text, flags=re.MULTILINE)
    return text.strip()
```

### 7. Debugging Approach
**Source**: Google AI Forums

When function calling is unreliable:
1. Start with a single tool
2. Test thoroughly
3. Add arguments back step by step
4. Check for unsupported nesting or parameter configurations
5. Gradually increase complexity

### 8. Gemini 2.0 Flash Thinking Mode
**Source**: DataCamp, Helicone Blog

For critical applications requiring fewer hallucinations:
- Use **Gemini 2.0 Flash Thinking** mode
- Provides stronger reasoning capabilities
- Significantly reduces hallucinations
- Better at following complex instructions

---

## Implemented Solutions in This Project

Based on the research, we implemented:

### ✅ 1. Enhanced System Prompt
- Added explicit "CRITICAL FUNCTION CALLING RULES" section
- Included WRONG vs RIGHT examples
- Emphasized autonomous data fetching
- Forbid code blocks and print statements

### ✅ 2. Post-Processing Filter
- Created `_clean_response()` method
- Strips code blocks, inline code, print statements
- Serves as safety net for system prompt failures

### ⚠️ 3. Configuration (Could Improve)
Current:
```python
response = self.chat_session.send_message(
    user_message,
    tools=[{'function_declarations': self.functions}]
)
```

**Potential Improvement**:
```python
# Add temperature and mode configuration
config = types.GenerateContentConfig(
    temperature=0,  # More deterministic
    tools=[{'function_declarations': self.functions}],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode='AUTO'  # Explicit mode
        )
    )
)
```

### 🔄 4. Could Try: Direct Function Passing
Instead of JSON schema, pass actual Python methods from AlpacaClient directly to Gemini.

---

## Recommendations for Further Improvement

### High Priority
1. **Add temperature=0** to the model configuration for more deterministic behavior
2. **Explicitly set function_calling_config mode** to 'AUTO' or 'ANY'
3. **Test with Gemini 2.0 Flash Thinking** mode if hallucinations persist

### Medium Priority
4. **Refactor to pass callable functions** instead of JSON schemas
5. **Add retry logic** for hallucinated function calls
6. **Implement better error messages** when function calling fails

### Low Priority
7. **Add telemetry/logging** to track when the model violates instructions
8. **Consider function call validation** before execution
9. **Experiment with different system prompt formats**

---

## Key Takeaways

1. **This is a known Gemini issue** - You're not alone!
2. **No single perfect solution exists** - Need multi-layered approach
3. **System prompts help but aren't foolproof** - Need post-processing
4. **Configuration matters** - Temperature and mode settings are important
5. **Gemini 2.0 Flash has issues** - Consider Thinking mode for critical apps
6. **Community workarounds work** - Explicit prompts + cleanup filters

---

## Sources

- n8n Community Forum: "Gemini Printing Tool Calls Instead of doing them"
- GitHub Issue #859: "Gemini function/tool calls not executing automatically"
- Google AI Forums: "Very frustrating experience with Gemini 2.5 function calling"
- Official Gemini Documentation: Function Calling Guide
- Phil Schmid: "Function Calling Guide: Google DeepMind Gemini 2.0 Flash"
- Prompt Engineering Guide: Function Calling with LLMs
- Martin Fowler: "Function calling using LLMs"
