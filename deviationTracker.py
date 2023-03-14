import requests
from bs4 import BeautifulSoup
import csv

# The URL to scrape
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Send a request to the URL and get the page content
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object from the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find the table that contains the S&P 500 companies data
table = soup.find("table", {"class": "wikitable sortable"})

# Find all the rows in the table except for the header row
rows = table.findAll("tr")[1:]

# Define an empty list to store the data for each row
data = []

# Loop through each row and extract the Symbol, Security, GICS Sector and GICS Sub-Industry
for row in rows:
    cells = row.findAll("td")
    symbol = cells[0].text.strip()
    security = cells[1].text.strip()
    sector = cells[2].text.strip()
    sub_sector = cells[3].text.strip()
    data.append([symbol, security, sector, sub_sector])

# Define the output filename and column header titles
output_filename = "sp500.csv"
column_headers = ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry"]

# Open the output file in write mode and write the data and column headers to it
with open(output_filename, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(column_headers)
    writer.writerows(data)

import pandas as pd
import yfinance as yf

# Read the CSV file produced by the previous script
df = pd.read_csv("sp500.csv", encoding="ISO-8859-1")

# Define the output filename
output_filename = "stockDataPull.csv"

# Loop through each symbol in the "Symbol" column
for symbol in df["Symbol"]:
    # Download the past 25 days of trading data for the symbol using yfinance
    stock_data = yf.download(symbol, period="25d")
    
    # Add a new column to the stock_data DataFrame to store the symbol
    stock_data["Symbol"] = symbol
    
    # Write the stock_data DataFrame to the output CSV file
    with open(output_filename, "a", newline="") as csv_file:
        stock_data.to_csv(csv_file, header=csv_file.tell()==0)

import pandas as pd

# Read in the CSV file produced by the previous script
df = pd.read_csv("stockDataPull.csv")

# Group the data by Symbol and calculate the average "Close" for each group
avg_close = df.groupby("Symbol")["Close"].mean()

# Merge the average "Close" back into the original DataFrame
df = df.merge(avg_close, on="Symbol", suffixes=("", "_avg"))

# Calculate the deviation of the last "Close" value for each symbol from the average "Close" value for that symbol as a percentage
df["Close_deviation_pct"] = ((df["Close"] - df["Close_avg"]) / df["Close_avg"]) * 100

# Export the updated DataFrame to a new CSV file named "deviationCalc.csv"
df.to_csv("deviationCalc.csv", index=False)

# Print a message to indicate that the export has completed
print("Deviation calculation completed and exported to deviationCalc.csv")

import pandas as pd

# Read in the "deviationCalc.csv" file
df = pd.read_csv("deviationCalc.csv")

# Convert the "Date" column to datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Find the most recent date in the DataFrame
max_date = df["Date"].max()

# Filter the DataFrame to only include rows with the most recent date
df = df[df["Date"] == max_date]

# Export the filtered DataFrame to a new CSV file named "devAnalysis.csv"
df.to_csv("devAnalysis.csv", index=False)

# Print a message to indicate that the export has completed
print('⣿⣿⡿⠟⣛⣉⣩⣭⣭⣉⣙⣛⠻⣿⣿⣿⠿⢛⣛⣛⣛⣛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⠋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⠙⣡⣾⣿⣿⣿⣿⣿⣿⣶⣌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')
print('⢁⣾⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠧⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⡿⢋⣥⣶⣾⣿⣿⣿⣿⣷⣶⣦⣍⠻⠛⣛⣉⣭⣭⣍⣙⡛⠣⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⢻⣿⣿⣿⣿⣿⣿⣿⣶⣌⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣆⠹⣿⣿⣿⣿⣿⣿⠿⠿⠿⠆⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⠟⣡⠶⠞⣛⣋⣀⣨⣌⣉⠓⠦⣬⡙⢷⣦⡀⢿⣿⣿⡿⠃⠀⠀⠀⠀⠀⢀⠈⠛⢿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⠁⠞⣡⠾⠿⠿⠿⠟⠛⠛⠛⠻⠒⠈⠙⠂⠙⢿⡄⢻⣏⡠⠚⠁⠀⠰⠶⢦⣬⡙⠄⣼⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣶⣶⣦⣄⡛⠻⠃⠀⠂⠀⣠⣄⠀⣻⣿⣿⡄⢢⡀⢸⠟⠀⠀⠄⠀⣀⠀⢶⣬⣑⠀⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣦⡙⢷⣤⣀⠁⠀⠉⠁⢀⣿⣿⣿⡿⠌⠧⡄⠸⠀⠀⠂⠀⠉⠁⣼⠿⢋⠀⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣦⣍⣛⡻⠷⠶⠦⠬⠭⠭⠥⠶⠚⣠⣿⡐⠶⢶⣶⣶⣤⡶⠶⠞⢁⣾⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⠟⠛⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⢀⣴⣿⣿⣿⣿⣷⣄⠲⣶⣿⣅⣀⣴⣦⠙⣿⣿⣿⣿⣿⣿⣿')
print('⣿⠿⠚⠛⣋⣹⣿⣿⣿⣿⣿⣿⣿⠿⠟⣛⣩⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⣿⣿⣿⣿⣿⡇⠘⣿⣿⣿⣿⣿⣿')
print('⣇⡔⢠⣦⠤⣍⣛⠻⠿⠿⣿⣷⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣰⠗⣸⣿⣿⣿⣿⣿')
print('⣿⣿⣄⡙⠷⣬⣉⣛⠻⠶⣶⣶⣤⣭⣍⣙⣛⣛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⣋⡴⢋⣴⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣶⣬⣙⠻⢿⣷⣦⣬⣭⣉⣉⣉⣉⣛⠛⠿⠿⠿⠿⠿⠶⠶⠶⠶⠶⠿⠟⣋⣴⠀⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣾⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣦⣤⣭⣭⣭⣭⣭⣛⣛⣛⣭⣭⣭⣭⣭⣭⣥⡶⢸⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣋⣥⣤⣌⠛⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣥⣾⣿⣿⣿⣿⣧⣍⠻⢿⣿⣿⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣴⣦⡈⢴⡦⢸⡿⢋⡭⢀⡉⠻⢋⣿⣦⣌⠻⣿⣿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⢿⣷⣤⡄⣤⡶⢋⠴⢋⣠⣾⣿⣿⣿⣿⣷⡘⢿⣿⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢻⣿⣧⠉⡴⢡⣾⣿⣿⡿⢋⣽⣿⣿⣿⣿⣆⠻⣿⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣷⣄⡙⢿⣿⠏⣰⣿⣿⡿⢋⣼⡿⢻⣦⠹⣿')
print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢁⡈⢻⣿⣿⣿⣿⣶⣦⣐⣿⣿⢋⣴⣿⡟⣠⣿⣿⡆⢻')

print("Deviation analysis completed and exported to a file in your downloads called devAnalysis.csv")
print("This PY program was created by Ryan Plett")

import pandas as pd

# Read in the "devAnalysis.csv" file
df_dev = pd.read_csv("devAnalysis.csv")

# Read in the "sp500.csv" file
df_sp500 = pd.read_csv("sp500.csv", encoding="ISO-8859-1")

# Join the two DataFrames on the "Symbol" column
df_merged = pd.merge(df_dev, df_sp500[["Symbol", "GICS Sector"]], on="Symbol", how="left")

# Export the merged DataFrame to a new CSV file named "devAnalysisWithSector.csv"
df_merged.to_csv("devAnalysisWithSector.csv", index=False)

# Print a message to indicate that the export has completed
print("Sector information appended to devAnalysis.csv and exported to devAnalysisWithSector.csv")

