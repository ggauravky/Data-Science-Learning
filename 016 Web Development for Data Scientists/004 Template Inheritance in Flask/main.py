from flask import Flask, render_template , flash

app=Flask(__name__)

app.secret_key = 'your_secret_key'  # Replace with your actual secret

@app.route('/')
def hello_world():
    flash('Welcome to the Flask app!', 'info')
    return render_template('index.html')

app.run(debug=True) 