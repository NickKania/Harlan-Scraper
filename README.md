# Harlan-Scraper
## Description
A scrape to find all assigned report/discussant/chat tracer events over a semester. A .ics file can then be created to add each assignment to your calendar.
## Requirements
- python3
## Instructions
- Install requirements `pip install -r requirements.txt`
- Run script `python3 scraper.py <lastname>`
	- To create a .ics file pass `--cal` argument `python3 scraper.py <lastname> --cal`