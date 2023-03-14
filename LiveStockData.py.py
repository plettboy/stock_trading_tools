import requests

# Replace YOUR_API_KEY with your Twelve Data API key
api_key = "aa92364b8aef4f3ca44835fe2cecba5c"

# The API endpoint for real-time stock data
url = f"https://api.twelvedata.com/quote?symbol=AAPL&apikey={api_key}"

# Send a GET request to the API endpoint
response = requests.get(url)

# Parse the JSON data from the response
data = response.json()

# Extract the relevant stock data from the JSON object
price = data["close"]
change = data["change"]
percent_change = data["percent_change"]

# Print the stock data
print(f"Apple Stock Price: ${price}")
print(f"Change: {change}")
print(f"Percent Change: {percent_change}")
