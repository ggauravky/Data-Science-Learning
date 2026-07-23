from flask import Flask, render_template, request

app = Flask(__name__ )

@app.route("/",methods=["GET", "POST"])
def hello_world():
    if request.method=="POST":
        print(request.form)
        name=request.form["name"]
        email=request.form["email"]
        print(f"Name: {name}, Email: {email}")
        return "<b>Form submitted successfully!</b>"
    return render_template("index.html")


app.run(debug=True)