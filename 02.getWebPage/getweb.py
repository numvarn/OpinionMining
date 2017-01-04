#!/usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        getweb.py
# Purpose:     Use for dowload webpage from URL
#              and use BeautifulSoup to process hypertext document to plain text
# Author:      Phisan Sookkhee
# Created:     22 NOV 2016
# Edited:      26 NOV 2016
# Parameter    Get from comand line
#              @startID
#              @stopID
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib2 import HTTPError
from getURLDB import GetPath
import requests
import os
import sys
import re

def getWeb(urlid, url, directory):
    check = 1
    htmlError = 0
    check = validateURLFormat(url)
    if not check:
        print "+++++ Invalid URL Address", url, "\n"
        return 0

    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')

    except HTTPError, e:
        print "HTTP Error ", e.code, " : ", url, "\n"
        print "Using Requests to downlaod web page\n"
        htmlError = 1
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "lxml") #********


    # for none utf-8 web page
    if soup.original_encoding != 'utf-8':
        try :
            decoded_html = html.decode('tis-620')
            soup = BeautifulSoup(decoded_html, 'html.parser')
        except :
            print "Dectect error ", urlid, " -- ", url
            pass

    # remove javascript
    to_extract = soup.findAll('script')
    for item in to_extract:
        item.extract()

    # remove inner CSS
    to_extract = soup.findAll('style')
    for item in to_extract:
        item.extract()

    # get only text from hypertext document
    text = soup.get_text()
    text = u''.join(text).encode('utf-8').strip()

    # write original html to file
    original = directory+'/original/'
    if not os.path.exists(original):
        os.makedirs(original)

    filename = original+str(urlid)+'.html'
    if htmlError == 1:
        writeHTMLToFile(html.content, filename)
    else:
        writeHTMLToFile(html, filename)

    # process for file name from url
    target = directory+'/processed/'
    if not os.path.exists(target):
        os.makedirs(target)
    filename = target+str(urlid)+'.txt'
    writeToFile(text, filename, target)

def validateURLFormat(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    m = regex.match(url)

    if m:
        return 1
    else:
        return 0

def writeHTMLToFile(html, filename):
    file = open(filename, 'w')
    file.write(html)
    file.close()

def writeToFile(str, filename, directory):
    # write data in tmp file
    tmpfile = directory+"/tmp.txt"
    file = open(tmpfile, 'w')
    file.write(str)
    file.close()

    removeEmptyLine(filename, tmpfile)

    # remove tmp file
    if os.path.exists(tmpfile):
        os.remove(tmpfile)

def removeEmptyLine(filename, tmpfile):
    newcontent = []
    file1 = open(tmpfile, 'r')

    for line in file1:
        if not line.strip():
            continue
        else:
            newcontent.append(line)

    # write data in target file
    filecontent = "".join(newcontent)
    file2 = open(filename, 'w')
    file2.write(filecontent)
    file2.close()

# Start program
def main(netloc):
    # Create Object from GetPath Class
    # And query urlpath from DB
    getPath = GetPath(netloc)
    rows = getPath.getResult()

    count = 1
    for row in rows:
        print "Processed : %s : #%s : ID - %s : %s\n" \
                %(netloc, count, row[0], row[1].encode('utf-8', 'replace'))

        count += 1

        directory = '/Volumes/Phisan/rawData/'+row[2]

        if not os.path.exists(directory):
            os.makedirs(directory)

        getWeb(row[0], row[3].encode('utf-8', 'replace'), directory)

# Main Program
# Get Network Location from command line argument
if __name__ == '__main__':
    if len(sys.argv) > 1:
        print "\nNetwork Location : %s\n" %(sys.argv[1])
        main(sys.argv[1])
    else:
        print "Please, Enter Network Location"
