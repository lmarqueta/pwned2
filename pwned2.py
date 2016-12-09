#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import urllib2
import json
import time


URL = 'https://haveibeenpwned.com/api/v2'
HEADERS = {"User-Agent": "pwned2"}
SLEEP = 1.5


def check_email(e):
    service = 'breachedaccount'
    email = e.strip()
    data = []
    url = URL + '/' + service
    url = url + '/' + email
    req = urllib2.Request(url, headers=HEADERS)
    try:
        r = urllib2.urlopen(req)
        data = json.loads(r.read())
        if data:
            print email
        for breach in data:
            print "  Title:  " + breach['Title']
            # print "  Name:   " + breach['Name']
            print "  Domain: " + breach['Domain']
            print "  Date:   " + breach['BreachDate']
            # print "    " + str(breach['PwnCount'])
            # print "    " + breach['Description']
            print "  Data:   " + ', '.join(breach['DataClasses'])
            print
    except urllib2.HTTPError as e:
        if e.code == 400:
            print "Bad request"
        elif e.code == 403:
            print "Forbidden"
        elif e.code == 404:
            # print "Not found. Good!"
            pass
        elif e.code == 429:
            print "Too many requests"
        return e.code

def check_filename(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                check_email(line)
                time.sleep(SLEEP)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--email', dest='email')
    group.add_argument('-f', '--filename', dest='filename')
    args = parser.parse_args()

    email = args.email
    filename = args.filename

    if email:
        check_email(email)
    else:
        check_filename(filename)
