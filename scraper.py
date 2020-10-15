import requests
import re
import pandas as pd

class Item():
    def __init__(self,section, date, role):
        self.date = date
        self.section = section
        self.role = role

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

names = ['Severs', 'Kania']
table_list = pd.read_html(get_content())
for i in range(5, len(table_list)):
    table = table_list[i]
    # print (table)
    for index, row in table.iterrows():
        for name in names:
            chat_name = '-' + name
            if name in row.tolist():
                print ('%s is presenting: %s on %s' % (name, row[0], row[len(row) - 1]))
            elif chat_name in row.tolist():
                # print (row)
                print ('%s is discussant for: %s on %s' % (name, table.loc[index - 1][0], table.loc[index - 1][len(row) - 1]))
