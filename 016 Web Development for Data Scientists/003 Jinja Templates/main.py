from flask import Flask , render_template , request

app = Flask(__name__)

@app.route("/")
def hello_world():
    name="Gaurav"
    lucky=[1,2,3,4,5]
    footer="<p>Copyright 2024</p>"
    return render_template("index.html", name=name, lucky=lucky, footer=footer)

app.run(debug=True)