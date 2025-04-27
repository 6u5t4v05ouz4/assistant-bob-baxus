# Bob Assistant BAXUS

<p align="center">
  <img src="home-bob.png" alt="Print da Home" width="600"/>
</p>

A web application for personalized whisky recommendations based on your BAXUS collection.

## Features
- User profile analysis based on your BAXUS collection
- Smart recommendations for similar and complementary bottles
- Visual dashboard with carousels and insights

## LLM API Key and Endpoint

To use the AI features, you must set up your LLM API credentials in a `.env` file.

**Required variables:**
- `LLM_API_KEY`: Your API key from the provider (Groq, OpenAI, etc.)
- `LLM_API_URL`: The endpoint URL for the chosen LLM service

**How to configure:**
1. Copy the example environment file:
   - On Linux/macOS:
     ```sh
     cp .env.example .env
     ```
   - On Windows:
     ```sh
     copy .env.example .env
     ```
2. Open the new `.env` file and fill in your API credentials.

**Example for Groq:**
```env
LLM_API_KEY=your-groq-key
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
```

**Example for OpenAI:**
```env
LLM_API_KEY=your-openai-key
LLM_API_URL=https://api.openai.com/v1/chat/completions
```

---

## Installation & Setup

### Requirements
- Python 3.8 or higher
- pip

### Step-by-step
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/assistant-bob-baxus.git
   cd assistant-bob-baxus
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   - Copy `.env.example` to `.env` (see instructions above)
   - Fill in your API credentials in `.env`
4. **Run the application:**
   ```sh
   python app.py
   ```
5. **Open in your browser:**
   Visit [http://localhost:5000](http://localhost:5000)

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
