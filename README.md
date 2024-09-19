# CYC Calendar Generator
Generates a calendar for the CYC Racing Season

### Data Preparation
Get the events into a CSV file e.g. events/2024-2025.csv

Format is:
`Date, Event, Description`

Note there are no start times, these are currently all day events. 
Dates must be DD/MM/YYYY format.
Put any extra details in the description.

## Setup
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install ics
```

## Generate
./generate.py events/2024-2025.csv

The file is generated into the calendars/ folder with the same name as the events CSV file.

## Upload
Import the generated ICS file into your calendar.
