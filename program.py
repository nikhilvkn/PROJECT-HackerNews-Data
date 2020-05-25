from bs4 import BeautifulSoup

import requests
import datetime
import boto3
import json
import os


def main(links,votes):
    s3 = boto3.resource('s3')
    data = []
    for idx, item in enumerate(links):
        text = item.getText()
        url = item.get('href', None)
        points = votes[idx].select('.score')
        if len(points):
            vote = int(points[0].getText().replace(' points',''))
            if vote > 99:
                data.append({'Title': text, "Url": url, "Votes": vote})
                data = sorted(data, key=lambda x: x['Votes'], reverse=True )
                
    date_object = datetime.date.today()
    filename = "data_{}_{}.json".format(os.getenv('FILENAME'), date_object)

    # Printing filename in logs
    print(filename)

    obj = s3.Object('nnarayanan-hacker-news',filename)
    obj.put(Body=json.dumps(data, separators=(',', ':')))


def lambda_handler(event, context):
    resonse = requests.get('https://news.ycombinator.com/')
    soup = BeautifulSoup(resonse.text, 'html.parser')
        
    links = soup.select('.storylink')
    votes = soup.select('.subtext')
    main(links,votes)
