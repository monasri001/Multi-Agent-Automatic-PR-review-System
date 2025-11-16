# Groq API Setup Guide

This project now uses **Llama3 via Groq API** for fast and cost-effective code reviews.

## Why Groq?

- **Extremely Fast**: Groq provides inference speeds 10x faster than traditional APIs
- **Cost-Effective**: Free tier available with generous limits
- **High Quality**: Access to Llama3 70B model for excellent code review quality
- **Easy Setup**: Simple API integration

## Quick Setup

### 1. Get Your Groq API Key

1. Visit https://console.groq.com/
2. Sign up for a free account
3. Navigate to API Keys section
4. Create and copy your API key

### 2. Configure Environment

Add to your `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
```

### 3. Available Models

**Recommended Models:**
- `llama-3.1-70b-versatile` - Best quality (default)
- `llama-3.1-8b-instant` - Faster, good quality
- `llama-3-70b-8192` - Alternative 70B model
- `llama-3-8b-8192` - Alternative 8B model
- `mixtral-8x7b-32768` - Mixtral model option

### 4. Test the Setup

```bash
python test_setup.py
```

If everything is configured correctly, you should see all imports successful.

## How It Works

The project uses a custom `GroqChatLLM` wrapper (`app/services/groq_llm.py`) that:
- Implements LangChain's `BaseChatModel` interface
- Converts LangChain messages to Groq API format
- Handles API calls to Groq's OpenAI-compatible endpoint
- Returns responses in LangChain-compatible format

This allows all existing agents to work seamlessly with Groq without code changes.

## API Endpoint

Groq uses an OpenAI-compatible API endpoint:
- URL: `https://api.groq.com/openai/v1/chat/completions`
- Authentication: Bearer token via `GROQ_API_KEY`

## Troubleshooting

### "Groq API error: 401 Unauthorized"
- Check that your `GROQ_API_KEY` is correct in `.env`
- Verify the key is active at https://console.groq.com/

### "Groq API error: 429 Too Many Requests"
- You've hit the rate limit
- Free tier has generous limits, but wait a moment and try again
- Consider upgrading if you need higher limits

### "Model not found"
- Check that the model name is correct
- Available models: `llama-3.1-70b-versatile`, `llama-3.1-8b-instant`, etc.
- See https://console.groq.com/docs/models for current models

## Benefits Over OpenAI

1. **Speed**: Groq's inference is significantly faster
2. **Cost**: Free tier available, very affordable paid tiers
3. **Quality**: Llama3 70B provides excellent code review quality
4. **Privacy**: Option to use self-hosted models in the future

## Next Steps

1. Get your API key from https://console.groq.com/
2. Add it to `.env` file
3. Start the server: `python run_server.py`
4. Test with a PR review!

For more information, see the main `README.md` and `IMPLEMENTATION_GUIDE.md`.

