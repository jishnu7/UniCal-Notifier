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
import MySQLdb
import cPickle as Pickle
import os

# File to store site data
PICKLE_FILE = "lastupdate.p"

# Number of entries to check whether the site is updated or not.
# More than one needed to avoid problems if one wntry is deleted
ENTRIES = 2

DBHOST = "localhost"
DBPASS = "root"
DBUSER = "root"
DB = "test"

db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)

def send_sms(msg,number):
    print msg, number

def send_mail(msg, email):
    print msg. email

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

def store(data):
    pfile = open(PICKLE_FILE, 'wb')
    Pickle.dump(data, pfile)
    pfile.close()
    return

def read_old_data():
    data = []
    if os.path.isfile(PICKLE_FILE):
        pfile = open(PICKLE_FILE, 'rb')
        data = Pickle.load(pfile)
        pfile.close()
    return data

def search(link):
    lastupdate = read_old_data()
    for i in range(0, ENTRIES):
        if lastupdate[i]['link'] == link:
            return True
    return False

def fetch_data():
    web = urllib.urlopen("http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324")
    #web = urllib.urlopen("Notification.html")
    data = BeautifulSoup(web)
    i = 12
    top = 0

    update = []

    while 1:
        print "--------------------------------------------------------"
        try:
            row = data.findAll("tr")[i].findAll("td")
        except:
            break
        for rows in row:
            try:
                link = rows.findAll("a")[0]['href']
            except:
                continue
            text = rows.renderContents()
            text = re.sub(r"<[^>]+>","", text)
            text = re.sub(r"&nbsp;","", text)
            text = re.sub(r"&amp;","&",text)

            #print link
            #print text

            if search(link):
            # Search data found
            # No new update
                j = 0
                while len(update) < ENTRIES:
                    lastupdate = read_old_data()
                    update.append(lastupdate[j])
                    j = j + 1
                store(update)
                return
            else:
            # Update Found
                print link
                print text
                #New update found
                if top < ENTRIES:
                    temp = {'text' : text, 'link' : link}
                    update.append(temp)
                    top = top + 1
                i = i+2

    

#        send_mail("")
#        send_sms("")

fetch_data()
