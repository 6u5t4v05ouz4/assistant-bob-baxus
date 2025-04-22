import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import pandas as pd
from recommendation_engine import WhiskyRecommender
from data_loader import load_whisky_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Load whisky data from Google Sheets
whisky_data = None
try:
    whisky_data = load_whisky_data()
    logger.info(f"Loaded {len(whisky_data)} whisky bottles")
except Exception as e:
    logger.error(f"Error loading whisky data: {e}")

# Initialize the recommender engine
whisky_recommender = None
if whisky_data is not None:
    whisky_recommender = WhiskyRecommender(whisky_data)
    logger.info("Whisky recommender initialized")

# Função utilitária para converter numpy types para tipos nativos Python
import numpy as np

def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form.get('username')
    if not username:
        flash('Please enter a BAXUS username', 'danger')
        return redirect(url_for('index'))
    
    # Store username in session
    session['username'] = username
    
    # Fetch user bar data from BAXUS API
    try:
        api_url = f"http://services.baxus.co/api/bar/user/{username}"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            flash(f'Error fetching bar data: {response.status_code}', 'danger')
            return redirect(url_for('index'))
        
        # Store bar data in session
        bar_data = response.json()
        if not bar_data:
            flash('No bottles found in your BAXUS collection', 'warning')
            return redirect(url_for('index'))
        
        # Generate recommendations
        if whisky_recommender is not None:
            user_profile, similar_recs, complementary_recs, bar_stats = whisky_recommender.get_recommendations(bar_data)
            
            # Ensure user_profile has required keys
            user_profile = user_profile or {}
            user_profile.setdefault('avg_price', 0)
            user_profile.setdefault('min_price', 0)
            user_profile.setdefault('max_price', 0)
            
            # Converte todos os resultados para tipos nativos Python antes de salvar na sessão
            session['user_profile'] = convert_numpy(user_profile)
            session['similar_recommendations'] = convert_numpy(similar_recs)
            session['complementary_recommendations'] = convert_numpy(complementary_recs)
            session['bar_stats'] = convert_numpy(bar_stats)
            
            return redirect(url_for('recommendations'))
        else:
            flash('Recommendation engine not available', 'danger')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Error analyzing bar: {e}")
        flash(f'Error analyzing bar: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/recommendations')
def recommendations():
    username = session.get('username')
    if (
        not username or
        username.strip() == '' or
        username.lower() in ['bob', 'test', 'default', 'none']
        or 'similar_recommendations' not in session
    ):
        flash('Please enter a valid username first.', 'warning')
        return redirect(url_for('index'))

    return render_template(
        'recommendations.html',
        username=username,
        user_profile=session['user_profile'],
        similar_recommendations=session['similar_recommendations'],
        complementary_recommendations=session['complementary_recommendations'],
        bar_stats=session['bar_stats']
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Server error, please try again later"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
