#!/usr/bin/python


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
import cPickle
import os
from twitterbot import Twitter

# Number of entries to check whether the site is updated or not.
# More than one needed to avoid problems if one entry is deleted
ENTRIES = 2

URL = {
        'Notifications' : 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324',
        #'Timetable' : 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=745&pop=1&page=0&Itemid=325'#,
        'Results' : 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=792&pop=1&page=0&Itemid=342'
       }

class Pickle():
    def __init__(self, filename):
        self.filename = filename

    def pickling(self,data):
        pfile = open(self.filename, 'wb')
        cPickle.dump(data, pfile)
        pfile.close()
        return

    def unpickling(self):
        data = []
        if os.path.isfile(self.filename):
            pfile = open(self.filename, 'rb')
            data = cPickle.load(pfile)
            pfile.close()
            return data
        else:
            return None

    def update_search(self,link):
        lastupdate = self.unpickling()
        if lastupdate:
            for i in range(0, ENTRIES):
                if lastupdate[i]['link'] == link:
                    # No updates
                    return True
            # Update found
        return False

'''
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
'''

def fetch_data(page, url):
    web = urllib.urlopen(url)
    data = BeautifulSoup(web)
    i = 10
    top = 0

    update = []
    new_data = []

    # File to store site data
    pickle_file = "lastupdate_"+str(page)+".p"
    pck = Pickle(pickle_file)

    while 1:
        #print "-------------------------------------"
        try:
            row = data.findAll("tr")[i].findAll("td")
            i = i+2
        except:
            # reached end
            pck.pickling(update)
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

            if pck.update_search(link):
            # Search data found
            # No new update
                j = 0
                while len(update) < ENTRIES:
                    lastupdate = pck.unpickling()
                    update.append(lastupdate[j])
                    j = j + 1
                if(j==2):
                    print "No new updates on "+page
                pck.pickling(update)
                return new_data
            else:
            # Search data not found
            # Update Found
                #print link
                #print text
                temp = {'text' : page+' : '+text, 'link' : link}
                new_data.append(temp)
                if top < ENTRIES:
                    update.append(temp)
                    top = top + 1
    return new_data

def truncate(s):
    ''' Function to trucate long string in a nicer way '''
    charmax = 120
    suffix ="..."
    length = len(s)

    if(length <= charmax):
        return s
    else:
        # return string to nearest 'space'
        end = s.rfind(' ',0,charmax-3)
        return s[0:end] + suffix

updates = []
for page in URL:
    temp = fetch_data(page, URL[page])
    temp.reverse()
    updates.extend(temp)

instance=Twitter()

for item in updates:
    if item:
        if str(item['link']).startswith('/'):
            link = "http://universityofcalicut.info"+item['link']
        elif str(item['link']).startswith('http://'):
            link = item['link']
        else:
            link = "http://universityofcalicut.info/"+item['link']

        try:
            instance.tweet(truncate(item['text'])+' '+ link)
            #print truncate(item['text'])+' '+ link
        except:
            continue
