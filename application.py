"""
I am a flask app
"""

from flask import Flask
from flask import render_template
app = Flask(__name__)
app.config.from_object('siteconfig')


@app.route("/")
def hello():
    return render_template('index.html'), 200

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(503)
def server_issues(error):
    return render_template('503.html'), 503

@app.route("/maintenance")
def server_maintenance():
    return render_template('maintenance.html'), 200

if __name__ == "__main__":
    app.run()