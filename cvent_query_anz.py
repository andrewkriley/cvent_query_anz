#!/usr/bin/env python2
#  -*- coding: utf-8 -*-

__author__ = "Andrew Riley"
__author_email__ = "andreril@cisco.com"
__contributors__ = [""]
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"

import urllib2
import json
import urlparse
import sys

if sys.argv[1:]:
   query = sys.argv[1]
else:
    print "Please enter a string to search for"
    print "e.g \'python " + sys.argv[0] + " ALL\' to see ALL training for the current month"
    print "e.g \'python " + sys.argv[0] + " Sydney\' to see Sydney training for the current month"
    print "e.g \'python " + sys.argv[0] + " Webinar\' to see Webinar based training for the current month"
    print "e.g \'python " + sys.argv[0] + " Live\' to see Live instructor led training for the current month"
    sys.exit()

url = 'http://cisco.cvent.com/Events/Calendar/Calendar.aspx?cal=d984e131-6347-400b-ba36-a9bb3f6b5216'

print ("Getting you a list of training based on your query")

def getTestUrl(url):
    urldata = urllib2.Request(url)
    try:
    	resp = urllib2.urlopen(urldata)
    except urllib2.HTTPError as e:
    	if e.code == 404:
    		print 'http 400 response - something wrong'
                sys.exit()
    	else:
    		urllib2.urlopen(urldata)
    		print '1st else'
    except urllib2.URLError as e:
    		print 'Not an HTTP-specific error (e.g. connection refused)'
                sys.exit()
    else:
        response = urllib2.urlopen(urldata)
        html = response.read()
        print 'URL Good'
        return html
html = getTestUrl(url)

def writeHtml2File(html):
    print 'Writing HTML to File'
    hs = open("cvent.html","a")
    hs.write(html)
    hs.close()
writeHtml2File(html)


#html_source = resp.read() #reads the HTML body response from the urllib2.urlopen
html1 = html.replace("\\","")
data1 = html1.split("v.events = [")[1]
data2 = data1.split("v.innerBorderColor")[0]
data3 = data2.replace(",{\"RecurrentMasterId\"","++{\"RecurrentMasterId\"")
data4 = data3.split("++")
#loop through list of events and get title, data and link

d = {}

for i in data4:
    #get event title
    #data = unicode(i).encode('utf8')
    data = i
    title = data.split('\"Text\":\"')[1].split('\"},')[0]
    title2 = title.split('\"}')[0]
    title3 = title2.replace('&amp;','&')
    #get event start date
    date = data.split('\"Start\":\"')[1].split('\"')[0]
    date1 = date.split('T')[0]
    date2 = date1.split('-')
    date3 = date2[2] + "-" + date2[1] + "-" + date2[0] + " (DD/MM/YYYY)"
    #get event registration link
    link = data.split('Redirect(\'')[1].split('\'')[0]
    #display results
    #print {"Title": str(title3), "Date": str(date3), "URL": str(response),}
    myjson = [title3, date3,link]
    d[title3] = {}
    d[title3]["Date"] = date3
    d[title3]["URL"] = link

#eventJson = json.dumps(d)

#hs = open("event.json","a")
#hs.write(eventJson)
#hs.close()

#for key in d:
#    value = d[key]
#    print("The key and value are {} = {}".format(key, value))

count = 0

def myquery(query):
    for a in d:
        if query in a:
            #count +=1
            print a
            for b in d[a]:
                print (d[a][b])

def all():
    for a in d:
        print a
        for b in d[a]:
            print (d[a][b])

if query == "ALL":
    print 'Showing ALL Training'
    all()
else:
    print 'Showing Training that matched your query'
    myquery(query)
