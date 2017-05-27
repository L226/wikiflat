"""
I am a flask app
"""

from flask import Flask
from flask import request
from flask import render_template
from utils import generate_unravelled_text
app = Flask(__name__)
app.config.from_object('siteconfig')


@app.route("/")
def hello():
    return render_template('index.html'), 200

@app.route('/', methods=['POST'])
def query():

    text = request.form['text']
    processed_text = generate_unravelled_text(text)
    return render_template('query_result.html', disp_text=processed_text, topic_name=text), 200

@app.route("/about")
def about_page():
    return render_template('about.html'), 200

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(503)
def server_issues(error):
    return render_template('503.html'), 503

@app.route("/maintenance")
def server_maintenance():
    return render_template('maintenance.html'), 200

@app.route('/favicon.ico')
def favicon():
    return "", 200

if __name__ == "__main__":
    app.run(debug=True)