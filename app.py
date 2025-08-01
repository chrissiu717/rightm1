from flask import Flask, send_file
import subprocess
import os
import glob

app = Flask(__name__)

@app.route('/')
def index():
    return 'Rightmove Scraper is running. Visit /run to trigger scraping.'

@app.route('/run')
def run_scraper():
    try:
        subprocess.run(["python", "rightmove_scraper.py"], check=True)
        latest_file = sorted(glob.glob("rightmove_*.csv"))[-1]
        return send_file(latest_file, as_attachment=True)
    except Exception as e:
        return f"❌ Error: {e}", 500