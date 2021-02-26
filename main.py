from flask import Flask, render_template, redirect, url_for
 
app = Flask(__name__)


@app.route("/login")
def login():
	return render_template("login.html")
	
@app.route("/signup")
def signup():
	return render_template("signup.html")

@app.route("/home")
def home():
	return render_template("home.html", name=="khalil")

@app.route("/")
def begin():
	return redirect("login")
	
if __name__ == "__main__":
	app.run()
