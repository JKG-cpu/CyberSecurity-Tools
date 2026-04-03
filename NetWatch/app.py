from flask import Flask, render_template, request, jsonify
from .app_helper import sweep_host, ping_host, scan_host, whois_info, banner_info

app = Flask(__name__, template_folder = "dashboard")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sweep")
def sweep():
    pass 

@app.route("/ping")
def ping():
    pass

@app.route("/scan")
def scan():
    pass

@app.route("/whois")
def whois():
    pass

@app.route("/banner")
def banner():
    pass

if __name__ == "__main__":
    app.run(
        debug = True
    )