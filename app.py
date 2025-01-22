import main
from flask import Flask, render_template

app = Flask("canvas-to-googletasks")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/export", methods=["POST"])
def export():
    main.main()

if __name__ == "__main__":
    app.run(debug=True)