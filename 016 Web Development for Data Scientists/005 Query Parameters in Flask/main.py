from flask import Flask, render_template ,request

app = Flask(__name__ )

@app.route("/")
def hello_world():
    name=request.args.get("name" , default="Gaurav")
    lang=request.args.get("lang" , default="Python")
    print(name)
    print(lang)
    return render_template("index.html" , name=name, lang=lang)

@app.route("/about")
def about():
    name = request.args.get("name")
    lang = request.args.get("lang")
    return render_template("about.html", name=name, lang=lang)

@app.route("/contact")
def contact():
    name = request.args.get("name")
    return render_template("contact.html", name=name)

app.run(debug=True)
