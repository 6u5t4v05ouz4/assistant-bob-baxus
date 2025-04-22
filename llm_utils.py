import requests
import os

def gerar_mensagem_llm(prompt, api_key=None):
    """
    Envia um prompt para o Groq LLM e retorna uma mensagem personalizada.
    """
    api_key = "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"
    url = "https://api.groq.com/openai/v1/chat/completions"
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
