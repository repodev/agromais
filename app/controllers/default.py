from flask import render_template
from app import app

@app.route("/registro")
def index():
	return render_template('registrar.html')