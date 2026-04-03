const pingBtn = document.getElementById("ping-btn");
const sweepBtn = document.getElementById("sweep-btn");

const isString = (val) => typeof val === "string" || val instanceof String;

// Fetch
async function fetchResult(endpoint, items = null) {
    try {
        if (items) {
            const string = new URLSearchParams(items).toString();
            const response = await fetch(`/${endpoint}?${string}`);
            const data = await response.json();

            if (!response.ok) {
                return `Error: ${data.error}`;
            }
            
            return data;
        } 
        else {
            const response = await fetch(`/${endpoint}`);
            const data = await response.json();

            if (!response.ok) {
                return `Error: ${data.error}`;
            }

            return data;
        }
    } catch (err) {
        return `Request failed: ${err}`;
    }
};

// Ping
pingBtn.addEventListener("click", async () => {
    const target = document.getElementById("ping-target").value;
    const resultDiv = document.getElementById("ping-result");

    if (!target){
        resultDiv.textContent = "Please enter a target.";
        return;
    }

    resultDiv.textContent = "Pinging...";
    
    const return_value = await fetchResult("ping", {"target": target});

    if (isString(return_value)) {
        resultDiv.textContent = return_value;
    } else {
        resultDiv.textContent = return_value.is_up ? `${target} is up.` : `${target} is not up.`;
    }
});

// Sweep
sweepBtn.addEventListener("click", async () => {
    const target = document.getElementById("ping-sweep").value;
    const resultDiv = document.getElementById("sweep-result");

    if (!target){
        resultDiv.textContent = "Please enter a target.";
        return;
    }

    resultDiv.textContent = "Sweeping...";

    const return_value = await fetchResult("sweep", {"target": target});

    if (isString(return_value)) {
        resultDiv.textContent = return_value;
    } else {
        const string = `Amount of hosts up: ${return_value.hosts_up.length}\nHosts up:\n${return_value.hosts_up.join("\n")}`;
        resultDiv.textContent = string;
    }
});

