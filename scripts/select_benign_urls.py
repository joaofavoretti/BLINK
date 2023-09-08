import os
import sys
import json
import requests
import warc
import random
import csv

FILENAME = '../files/urls.warc.wet'

if __name__ == '__main__':
    if not os.path.isfile(FILENAME):
        print('File not found: {}'.format(FILENAME))
        sys.exit(1)
    
    benign_urls = []
    
    with warc.open(FILENAME, 'rb') as f:
        for record in f:
           
            if 'WARC-Target-URI' in record:
                url = record['WARC-Target-URI']
                benign_urls.append({
                    'url': url,
                    'benign': True,
                })

    # randomly select 5000 benign urls
    random.shuffle(benign_urls)
    benign_urls = benign_urls[:5000]

    phishing_urls = []
    i = 0
    with open('../files/online-valid.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            phishing_urls.append({
                'url': row[1],
                'benign': False,
            })

            if (i > 500):
                break

            i += 1

    phishing_urls = phishing_urls[1:501]

    urls = benign_urls + phishing_urls
    random.shuffle(urls)
    
    print(len(urls))

    input()

    # save urls to database
    for i, url in enumerate(urls):
        print(f'\rSaving {url} ({i}/5500)', end='                                       ')
        data = {
            'url': url.get('url'),
        }
        if url.get('benign') == True:
            r = requests.post('http://localhost:5000/urls/save_from_url', json=data)
        else:
            r = requests.post('http://localhost:5000/urls/save_from_phishtank', json=data)

    print()