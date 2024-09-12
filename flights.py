import sys
import requests
from bs4 import BeautifulSoup

# Get the command-line arguments
origin = sys.argv[1]
destination = sys.argv[2]

# Construct the URL
url = f"https://www.flightconnections.com/flights-from-{origin}-to-{destination}"
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=request_headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all elements with class "flight-path-via" and attribute "data-connections"
    elements = soup.find_all(class_="flight-path-via", attrs={"data-connections": True})
    
    # Print the data-connections attribute of each element
    for element in elements:
        transit = element["data-connections"]
        print(f"{origin} 🡒 {transit} 🡒 {destination}")
else:
    print("Error: Failed to retrieve data from the website.")