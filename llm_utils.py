import requests
import os
from dotenv import load_dotenv

def gerar_mensagem_llm(prompt, api_key=None):
    """
    Envia um prompt para o Groq LLM e retorna uma mensagem personalizada.
    """
    load_dotenv()
    api_key = api_key or os.environ.get("LLM_API_KEY")
    url = os.environ.get("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    if not api_key:
        raise ValueError("A variável de ambiente LLM_API_KEY não está definida. Configure no .env.")
    if not url:
        raise ValueError("A variável de ambiente LLM_API_URL não está definida. Configure no .env.")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # ou "llama3-70b-8192"
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 80,
        "temperature": 0.7
    }
    print("Prompt enviado ao LLM:", prompt)
    print("Payload:", data)
    response = requests.post(url, headers=headers, json=data, timeout=20)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
