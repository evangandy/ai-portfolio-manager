#!/bin/bash
# Quick script to switch between Gemini and Ollama

if [ "$1" = "gemini" ]; then
    sed -i '' 's/AI_BACKEND=ollama/AI_BACKEND=gemini/' .env
    echo "✅ Switched to Gemini (with Ollama fallback)"
    echo "   Run: python3 portfolio_manager.py"
elif [ "$1" = "ollama" ]; then
    sed -i '' 's/AI_BACKEND=gemini/AI_BACKEND=ollama/' .env
    echo "✅ Switched to Ollama (local LLM)"
    echo "   Run: python3 portfolio_manager.py"
else
    echo "Usage: ./switch_ai.sh [gemini|ollama]"
    echo ""
    echo "Current setting:"
    grep "AI_BACKEND=" .env
    echo ""
    echo "Examples:"
    echo "  ./switch_ai.sh gemini   # Use Gemini (fast, reliable)"
    echo "  ./switch_ai.sh ollama   # Use Ollama (local, unlimited)"
fi
