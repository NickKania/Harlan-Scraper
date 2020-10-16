import requests
import re
import pandas as pd
from ics import Calendar, Event
import argparse
from dateutil.parser import parse

parser = argparse.ArgumentParser()
parser.add_argument('--cal', dest='create_cal', action='store_true')
parser.add_argument('name', help='Last name of student')
parser.set_defaults(create_cal=False)
args = parser.parse_args()

def get_content():
    try:
        response = requests.post(
            url="https://umaine.edu/computingcoursematerials/wp-login.php",
            params={
                "action": "postpass",
            },
            headers={
                "Authority": "umaine.edu",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests": "1",
                "Origin": "https://umaine.edu",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://umaine.edu/computingcoursematerials/cos-490/lectures-and-assignments-cos-490/",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip",
                "Cookie": "wordpress_test_cookie=WP+Cookie+check; wp-postpass_91b86dd71ed90ec455a0177f6a7c0449=%24P%24BIeE2ZeOc9EigMncmGc2k%2FujUL7u5r1",
            },
            data={
                "post_password": "wickedSmart",
                "Submit": "Enter",
            },
        )
        return response.text
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def add_event(calendar, topic, date, role):
    e = Event()
    if isinstance(topic, float):
        topic = 'Chat tracker'
        role = ''
    elif not 'p' in topic:
        topic = 'Chap ' + topic
    e.name = '%s %s' % (topic, role)
    e.begin = parse(date).replace(hour=15)
    calendar.events.add(e)


calendar = Calendar()
name = args.name
table_list = pd.read_html(get_content())
for i in range(5, len(table_list)):
    table = table_list[i]
    # print (table)
    for index, row in table.iterrows():
        chat_name = '-' + name
        if name in row.tolist():
            topic = row[0]
            date = row[len(row) - 1]
            add_event(calendar, topic, date, 'reporter')
            print ('%s is presenting: %s on %s' % (name, topic, date))
        elif chat_name in row.tolist():
            # print (row)
            topic = table.loc[index - 1][0]
            date = table.loc[index - 1][len(row) - 1]
            add_event(calendar, topic, date, 'discussant')
            print ('%s is discussant for: %s on %s' % (name, topic, date))

if args.create_cal:
    with open('%s.ics' % name, 'w') as cal_file:
        cal_file.write(str(calendar))