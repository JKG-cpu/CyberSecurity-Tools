import subprocess
import json

from src import *

result = subprocess.run(
    ["dotnet", "run", "--project", "ReconProcessor", "--", "--config"],
    capture_output = True,
    text = True
)

if result.returncode != 0:
    print(f"Config validation failed: {result.stdout}")
    exit(1)

# Step 2 - read config and start scan
with open("config/config.json") as f:
    config = json.load(f)

NmapScanner(
    config["remote_host"],
    config["start_port"],
    config["end_port"],
    config["max_concurrent"]
).start_scan()

with open("output/results.json") as f:
    data = json.load(f)

with open("output/history.json") as f:
    cur_data = json.load(f)
    cur_data.append(data)

with open("output/history.json", "w") as f:
    json.dump(cur_data, f, indent = 4)