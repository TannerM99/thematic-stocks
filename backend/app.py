import os
import requests
from flask import Flask, json, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Replace with actual Schwab URL as needed
SCHWAB_THEMES_URL = "https://www.schwab.com/thematic-investing/themes"

@app.route("/api/themes", methods=["GET"])
def get_themes():
    try:
        # Create a prompt to send to the LLM
        prompt = (
            f"Extract the thematic investment themes from the following HTML content of a Charles Schwab webpage:\n\n"
            f"{SCHWAB_THEMES_URL}\n\n"
            f"Return the extracted themes as a plain JSON array of strings, with no other text."
        )

        perplexity_headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        res = requests.post("https://api.perplexity.ai/chat/completions", json={
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": prompt}],
        }, headers=perplexity_headers)

        result = res.json()['choices'][0]['message']['content']
        if result.startswith("```json") and result.endswith("```"):
            result = result[7:-3].strip()
        themes = json.loads(result)  # Ensure JSON safety
        
        return jsonify(themes)
    
    except Exception as e:
        logging.exception("Failed to fetch or parse themes")
        return jsonify({"error": str(e)}), 500

@app.route("/api/stocks", methods=["GET"])
def get_stocks():
    theme = request.args.get("theme")

    perplexity_headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Summarize the current market sentiment for the investment theme '{theme}' in about 100 words. Also list 5 top US public companies related to this theme with their ticker symbols. Return JSON with 'summary' and 'stocks' as list of {{name, ticker}}."

    res = requests.post("https://api.perplexity.ai/chat/completions", json={
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}]
    }, headers=perplexity_headers)

    try:
        result = res.json()['choices'][0]['message']['content']
        if result.startswith("```json") and result.endswith("```"):
            result = result[7:-3].strip()
        themes = json.loads(result)  # Ensure JSON safety
        parsed = eval(result)  # Expects {'summary': str, 'stocks': [{name, ticker}]}
        for stock in parsed['stocks']:
            rec = requests.get(f"https://finnhub.io/api/v1/stock/recommendation?symbol={stock['ticker']}&token={FINNHUB_API_KEY}").json()
            if rec:
                counts = {
                    'Strong Buy': rec[0]['strongBuy'],
                    'Buy': rec[0]['buy'],
                    'Hold': rec[0]['hold'],
                    'Sell': rec[0]['sell'],
                    'Strong Sell': rec[0]['strongSell']
                }
                stock['recommendation'] = max(counts, key=lambda k: (counts[k], -list(counts).index(k)))
            else:
                stock['recommendation'] = 'N/A'
        return jsonify(parsed)
    except:
        return jsonify({"summary": "", "stocks": []}), 500

if __name__ == "__main__":
    app.run(debug=True)