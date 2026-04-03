# LangChain Multiagent Workshop

Small LangChain agent example that loads configuration from `.env`, calls an OpenAI chat model, and uses a simple weather tool.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment

Copy `.env.example` to `.env` and set your values:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## Run

```powershell
python agent.py
```
