#!/usr/bin/python2


#    UniCal Notifier
#    Copyright (C) 2011 jishnu7@gmail.com

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import urllib
from BeautifulSoup import BeautifulSoup
import re
import cPickle as Pickle
import os
#import MySQLdb
import twitterbot

# File to store site data
PICKLE_FILE = "lastupdate.p"

# Number of entries to check whether the site is updated or not.
# More than one needed to avoid problems if one entry is deleted
ENTRIES = 2

#DBHOST = "localhost"
#DBPASS = "root"
#DBUSER = "root"
#DB = "test"

#db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)

#def send_sms(msg,number):
#    print msg number

#def send_mail(msg, email):
#    print msg. email

#def push(text, content_type, link):
#    cursor = db.cursor()
#    query = "INSERT INTO post (content, type, link) VALUES (\"%s\", %s, \"%s\")" % (text, content_type, link)
#    cursor.execute(query)
#    print "here"
#    rows = int(cursor.rowcount)
#    print rows

def pull(query):
    cursor = db.cursor()
    cursor.execute(query)
    return int(cursor.rowcount)

def pickling(data):
    pfile = open(PICKLE_FILE, 'wb')
    Pickle.dump(data, pfile)
    pfile.close()
    return

def unpickling():
    data = []
    if os.path.isfile(PICKLE_FILE):
        pfile = open(PICKLE_FILE, 'rb')
        data = Pickle.load(pfile)
        pfile.close()
        return data
    else:
        return None

def update_search(link):
    lastupdate = unpickling()
    if lastupdate:
        for i in range(0, ENTRIES):
            if lastupdate[i]['link'] == link:
                # No updates
                return True
        # Update found
    return False

def fetch_data():
    web = urllib.urlopen("http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324")
    #web = urllib.urlopen("notification.htm")
    data = BeautifulSoup(web)
    i = 10
    top = 0

    update = []
    new_data = []

    while 1:
        print "-------------------------------------"
        try:
            row = data.findAll("tr")[i].findAll("td")
            i = i+2
        except:
            # reached end
            pickling(update)
            break
        for column in row:
            try:
                link = column.findAll("a")[0]['href']
            except:
                continue
            text = column.renderContents()

            # Remove comments
            text = re.sub(r"<!--(.*?)-->","", text)
            # Remove HTML tags
            text = re.sub(r"<[^>]+>","", text)
            # Replace html characters
            text = re.sub(r"&nbsp;","", text)
            text = re.sub(r"&amp;","&",text)
            # trim
            text = text.strip()

            if update_search(link):
            # Search data found
            # No new update
                j = 0
                while len(update) < ENTRIES:
                    lastupdate = unpickling()
                    update.append(lastupdate[j])
                    j = j + 1
                if(j==2):
                    print "No new updates"
                pickling(update)
                return new_data
            else:
            # Search data not found
            # Update Found
                print link
                print text
                temp = {'text' : text, 'link' : link}
                new_data.append(temp)
                if top < ENTRIES:
                    update.append(temp)
                    top = top + 1
    return new_data

def search(datas):
    terms = {
                'b.tech' : ['b.tech', 'btech', 'b tech', 'bachelor of technology'],
                'b.arch' : ['b.arch', 'barch', 'b arch', 'bachelor of architecture'],
                'm.tech' : ['m.tech', 'mtech', 'm tech']
            }

    for term in terms:
        temp = list()
        for subterm in term:
            for data in datas:
                if data['text'].lower().find(subterm) !=-1:
                    temp.append(data['text'])
        if len(temp) != 0:
            print "found"

#        send_mail("")
#        send_sms("")

a = fetch_data()
if a != None:
    search(a)
