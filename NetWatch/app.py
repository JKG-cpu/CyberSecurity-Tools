from flask import Flask, render_template, request, jsonify
from app_helper import sweep_host, ping_host, scan_host, whois_info, banner_info
from dataclasses import asdict

app = Flask(__name__, template_folder = "dashboard", static_folder = "dashboard/static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sweep")
def sweep():
    target = request.args.get("target")

    if target is None or target == "":
        return jsonify(error = "Must provide a valid IP Address"), 400

    try:
        hosts = sweep_host(target)
        return jsonify(target = target, hosts_up = hosts)

    except ValueError:
        return jsonify(error = "Must provide a valid IP Address"), 400

    except Exception as e:
        return jsonify(error = f"Internal server error: {e}"), 500

@app.route("/ping")
def ping():
    target = request.args.get("target")

    if target is None or target == "":
        return jsonify(error = "Must provide a valid IP Address"), 400

    try:
        host_is_up = ping_host(target)
        return jsonify(target = target, is_up = host_is_up)

    except ValueError:
        return jsonify(error = "Must provide a valid IP Address"), 400

    except Exception as e:
        return jsonify(error = f"Internal server error: {e}"), 500

@app.route("/scan")
def scan():
    target = request.args.get("target")
    fast = request.args.get("fast", "true").lower() == "true"
    ports = request.args.get("ports")

    if target is None or target == "":
        return jsonify(error = "Must provide a valid IP Address"), 400

    try:
        port_results = scan_host(
            target = target,
            fast = fast,
            ports = ports
        )
        return jsonify(target = target, results = [asdict(port) for port in port_results])

    except ValueError:
        return jsonify(error = "Must provide a valid Arguments"), 400

    except Exception as e:
        return jsonify(error = f"Internal server error: {e}"), 500

@app.route("/whois")
def whois():
    target = request.args.get("target")

    if target is None or target == "":
        return jsonify(error = "Must provide a valid IP Address"), 400

    try:
        info = whois_info(target)
        whois_data, dns_data = info
        return jsonify(target = target, whois = whois_data, dns = dns_data)

    except ValueError:
        return jsonify(error = "Must provide a valid IP Address"), 400

    except Exception as e:
        return jsonify(error = f"Internal server error: {e}"), 500

@app.route("/banner")
def banner():
    target = request.args.get("target")
    ports_raw = request.args.get("ports")

    if not target:
        return jsonify(error="Must provide a valid IP Address"), 400

    if not ports_raw:
        return jsonify(error="Must provide at least one port"), 400

    ports = [int(p) for p in ports_raw.split(",")]
    ports = ports[0] if len(ports) == 1 else ports

    try:
        info = banner_info(target=target, ports=ports)
        return jsonify(target=target, info=info)

    except ValueError:
        return jsonify(error="Must provide valid arguments"), 400

    except Exception as e:
        return jsonify(error=f"Internal server error: {e}"), 500
    
if __name__ == "__main__":
    app.run(
        debug = True, port = 5000
    )