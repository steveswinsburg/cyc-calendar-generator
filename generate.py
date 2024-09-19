#! /usr/bin/env python3

import argparse
import sys
from ics import Calendar, Event
from datetime import datetime
import csv
import os

# Function to convert the date from D/M/Y format to a datetime.date object (which makes it an all-day event)
def convert_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()  # Ensure we return only the date object
    except ValueError as e:
        raise ValueError(f"Error parsing date. '{date_str}'. Fix the data and run it again: {e}")

# Function to parse the CSV file and create events
def read_csv_and_create_events(file_path):
    events = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        
        # Process each row
        for row in reader:
            date_str, event_name, description = row
            event_date = convert_date(date_str)  # Will raise ValueError if date is invalid
            
            # Create an all-day event by passing a date object, ensuring it has no time component
            event = Event(
                name=event_name,
                begin=event_date,  # Date only, making it an all-day event
                description=description
            )
            event.make_all_day()  # Explicitly enforce it as an all-day event
            events.append(event)
    return events

# Main function to generate the ICS file
def generate_ics_from_csv(csv_file_path):
    # Extract the input filename without directories and extension
    base_filename = os.path.splitext(os.path.basename(csv_file_path))[0]
    
    # Construct the output filename in the "calendars" directory
    output_directory = "calendars"
    os.makedirs(output_directory, exist_ok=True)  # Ensure the directory exists
    ics_file_path = os.path.join(output_directory, f"{base_filename}.ics")
    
    # Create a calendar
    calendar = Calendar()

    # Add events to the calendar
    events = read_csv_and_create_events(csv_file_path)
    for event in events:
        calendar.events.add(event)

    # Save the calendar to an .ics file
    with open(ics_file_path, 'w') as f:
        f.writelines(calendar)

    print(f"ICS file generated: {ics_file_path}")

# Set up argument parser for command line arguments
def main():
    parser = argparse.ArgumentParser(description="Generates a calendar from a CSV of events.")
    
    # Add positional argument for the input file
    parser.add_argument('input', nargs='?', help="Path to the input CSV file.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # If no arguments are provided, print help and exit
    if not args.input:
        parser.print_help()
        sys.exit(1)
    
    # Generate the ICS file from the CSV file
    generate_ics_from_csv(args.input)

if __name__ == '__main__':
    main()