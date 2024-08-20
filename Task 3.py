import requests
import time

# Set your ZAP API key and target URL
zap_api_key = 'lutesvdk2jb7sfdp520n48t4gh'  # Replace with your actual API key
target_url = 'https://owasp.org/www-project-juice-shop/'  # Replace with your target URL
context_name = 'JuiceShopContext'  # Name for the context

# Function to create a context in ZAP
def create_context(context_name):
    create_context_url = f'http://localhost:8080/JSON/context/action/newContext/?apikey={zap_api_key}&contextName={context_name}'
    response = requests.get(create_context_url)
    if response.status_code != 200:
        print(f"Error creating context: {response.status_code} - {response.text}")
        return False
    return True

# Function to add the target URL to ZAP
def add_target_to_zap(url):
    add_url = f'http://localhost:8080/JSON/core/action/addUrl/?apikey={zap_api_key}&url={url}'
    response = requests.get(add_url)
    if response.status_code != 200:
        print(f"Error adding URL to ZAP: {response.status_code} - {response.text}")
        return False
    return True

# Create a context for the target URL
if not create_context(context_name):
    print("Failed to create context in ZAP. Exiting.")
    exit(1)

# Add the target URL to ZAP
if not add_target_to_zap(target_url):
    print("Failed to add target URL to ZAP. Exiting.")
    exit(1)

# Start a new scan
scan_url = f'http://localhost:8080/JSON/ascan/action/scan/?apikey={zap_api_key}&url={target_url}'
response = requests.get(scan_url)

# Check if the response is valid and contains the 'scan' key
if response.status_code != 200:
    print(f"Error starting scan: {response.status_code} - {response.text}")
else:
    try:
        scan_id = response.json()['scan']
    except KeyError:
        print("Scan ID not found in response. Response content:")
        print(response.json())
        exit(1)

# Check the status of the scan
status_url = f'http://localhost:8080/JSON/ascan/view/status/?apikey={zap_api_key}&scanId={scan_id}'

while True:
    status_response = requests.get(status_url)
    status = status_response.json().get('status', 'unknown')
    print(f'Scan Status: {status}%')
    if status == '100':
        print('Scan completed.')
        break
    time.sleep(5)  # Wait for 5 seconds before checking the status again

# Retrieve the results
results_url = f'http://localhost:8080/JSON/ascan/view/results/?apikey={zap_api_key}&scanId={scan_id}'
results_response = requests.get(results_url)
print(results_response.json())