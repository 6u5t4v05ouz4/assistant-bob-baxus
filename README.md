# Assistant Bob Baxus

A web application for personalized whisky recommendations based on your BAXUS collection.

## Features
- User profile analysis based on your BAXUS collection
- Smart recommendations for similar and complementary bottles
- Visual dashboard with carousels and insights

## LLM API Key e Endpoint

Para utilizar recursos de IA (LLM), é necessário informar:
- **LLM_API_KEY:** sua chave de API do provedor escolhido (Groq, OpenAI, etc)
- **LLM_API_URL:** o endpoint do serviço LLM desejado

Essas informações devem ser configuradas no arquivo `.env` (veja o exemplo em `.env.example`).

### Exemplo para Groq
```
LLM_API_KEY=sua-chave-groq
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
```

### Exemplo para OpenAI
```
LLM_API_KEY=sua-chave-openai
LLM_API_URL=https://api.openai.com/v1/chat/completions
```

Você pode utilizar qualquer provedor compatível, bastando ajustar esses valores.

## Installation

### Requirements
- Python 3.8+
- pip

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/assistant-bob-baxus.git
   cd assistant-bob-baxus
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python app.py
   ```
4. **Access in your browser:**
   Open [http://localhost:5000](http://localhost:5000)

## Usage
- Enter your BAXUS username to get personalized whisky recommendations.
- Explore your profile, preferred brands, and spirits.
- Browse recommended bottles in an interactive carousel.

## Project Structure
```
WhiskyBob/
├── app.py
├── recommendation_engine.py
├── llm_utils.py
├── data_loader.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── recommendations.html
│   └── error.html
└── static/
    └── ...
```

## License
MIT

---
*Developed by Grottan City Lab.*
