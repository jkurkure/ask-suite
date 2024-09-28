import requests, random, sys, platformdirs, datetime, os, pickle
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

site = "https://www.onthisday.com/"
console = Console()

if "--date" in sys.argv:
    month = sys.argv[sys.argv.index('--date')+1]
    day = sys.argv[sys.argv.index('--date')+2]
else:
    month = datetime.datetime.now().strftime("%B").lower()
    day = datetime.datetime.now().day

data_dir = platformdirs.user_data_dir(appname="today-cli", appauthor="jkurkure")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
file_path = os.path.join(data_dir, "day-archive.sav")

if os.path.exists(file_path):
    with open(file_path, "rb") as file:
        registry = pickle.load(file)

    if f"{month} {day}" in registry:
        console = Console()
        console.print(registry[f"{month} {day}"])
        sys.exit()
else:
    registry = {}

try:
    response = requests.get(f"{site}day/{month}/{day}")
except:
    console.print("[bright_red]You need an internet connection the first time you look up this date![/]")
    exit()

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all li elements with class "event"
event_elements = soup.find_all("li", class_="event")

table = Table(title="Today in History")
table.add_column("Event", style="bold")
table.add_column("Year", justify="right", style="red")
colors = ["green", "yellow", "blue", "magenta", "cyan", "white", "bright_yellow", "dark_olive_green3"]

# Create a list to store the events
events = []

# Iterate over the event elements and extract the event and year
for event in event_elements:
    try:
        year = event.find("a", class_="date").text.strip()
    except AttributeError:
        year = event.find("b").text.strip()
    incident = " ".join(event.text.strip().split()[1:])
    
    # Check if the year is present in the incident string
    if year in incident:
        incident = incident.split(year)[-1].strip()
    
    # Add the event to the events list
    events.append((incident, year))

# Sort the events list by year
def year_parse(s):
    if "BC" in s:
        return -int(s.replace(" BC", ""))
    else:
        return int(s)  
events = sorted(events, key=lambda x: year_parse(x[1]))

# Add the sorted events to the table
lastcol = "red"
for event in events:
    rowcol = random.choice(colors)
    while rowcol == lastcol:
        rowcol = random.choice(colors)
    table.add_row(f"[{rowcol}]{event[0]}[/]", event[1])

console.print(table)

registry[f"{month} {day}"] = table

with open(file_path, "wb") as file:
    pickle.dump(registry, file)