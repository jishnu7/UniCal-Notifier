#!/usr/bin/python


#    UniCal Notifier
#    Copyright (C) 2011-12 jishnu7@gmail.com

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


import urllib, re, cPickle, os, MySQLdb, sys, datetime
from BeautifulSoup import BeautifulSoup
from twitterbot import Twitter

# Number of entries to check whether the site is updated or not.
# More than one needed to avoid problems if one entry is deleted
ENTRIES = 3

#DB Parameters
DB_HOST = 'localhost'
DB_NAME = 'unical'
DB_USER = 'root'
DB_PASS = 'root'

# Urls to the updates listing pages
URL = {
        'Notifications' : 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324',
        'Timetable' : 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=745&pop=1&page=0&Itemid=325',
        'Results' : 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=792&pop=1&page=0&Itemid=342'
       }

class database():
    ''' To manage database operations '''
    def __init__(self,table):
        ''' Connect and init database '''
        self.table = table
        try:
            self.db = MySQLdb.connect(host=DB_HOST, \
                                      user=DB_USER, \
                                      passwd=DB_PASS, \
                                      db=DB_NAME)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        self.clean()

    def match(self, link):
        ''' Match data from database '''
        try:
            query = "SELECT * FROM %s WHERE link = " \
                    "'%s' LIMIT 1" % (self.table, link)
            cursor = self.db.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return row
        except MySQLdb.Error, e:
            print "Match Error %d: %s" % (e.args[0], e.args[1])
            return None

    def add(self, title, link):
        ''' add update to database '''
        try:
            date = self.timestamp()
            query = "INSERT INTO %s (`title`, `link`, `date`) VALUES "\
                    "('%s', '%s', '%s')" % (self.table, title, link, date)
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()
        except MySQLdb.Error, e:
            print "Add Error %d: %s" % (e.args[0], e.args[1])

    def clean(self):
        ''' Delete posts older than 30 days '''
        try:
            expiry = self.timestamp(30)
            query = "DELETE FROM %s WHERE `date` <= '%s'" \
                    % (self.table, expiry)
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()
        except MySQLdb.Error, e:
            print "Delete Error %d: %s" % (e.args[0], e.args[1])

    def timestamp(self,days=0):
        ''' Generate mysql time stamp '''
        now = datetime.datetime.now()-datetime.timedelta(days)
        return now.strftime('%Y-%m-%d %H:%M:%S')

''' TODO -- 
class fileoperation():
    def __init__:
        cache_file = "cache.pdf"

    def get(link=None):
        if link != None:
            urllib.urlretrieve(link,cache_file)
            return self.gen_hash()
        return None

    def gen_hash():
        # Generate md5 hash value
        f = file.open(cache_file)
        # read file in 128 chunks. Good for memory management.
        while True:
            data = f.read(128)
            if not data:
                break
            mdg.update(data)
        return md5.digest()

    def check():
'''

class unical():
    def check_update(self):
        updates = []
        for page in URL:
            print page
            temp = self.fetch_data(page, URL[page])
            temp.reverse()
            updates.extend(temp)
        return updates

    def full_url(self, link):
        link = str(link)
        if link.startswith('http://'):
            url = link
        else:
            url = "http://universityofcalicut.info/"+link
        return url

    def search(self, datas, terms):
        ''' 
            Search for a purticular term 
            'terms' should be an array of values
            eg:
            terms = ['b.tech', 'btech', 'b tech', 'bachelor of technology',
                    'b.arch', 'barch', 'b arch', 'bachelor of architecture']
             
            'datas' is the data ferched by the fetch_data function. 
            Which is also an array of array values.
        '''

        temp = list()
        for data in datas:
            flag = 0
            for term in terms:
                # Avoid duplicates
                if flag == 1:
                        break
                if data['text'].lower().find(term) !=-1:
                    temp.append({'text': data['text'], 'link' : data['link']})
                    flag = 1
        return temp

    def clean(self, column):
        text = column.renderContents()
        # Remove comments
        text = re.sub(r"<!--(.*?)-->","", text)
        # Remove HTML tags
        text = re.sub(r"<[^>]+>","", text)
        # Replace html characters
        text = re.sub(r"&nbsp;","", text)
        text = re.sub(r"&amp;","&",text)
        # trim
        return text.strip()

    def fetch_data(self, page, url):
        ''' Fetch data from passed link '''
        web = urllib.urlopen(url)
        data = BeautifulSoup(web)
        row_count = 10

        update = []

        db = database(page)
        data = data.findAll("tr")
        failed = 0
        while 1:
            if failed >= ENTRIES:
                break
            try:
                row = data[row_count].findAll("td")
            except:
                # reached end
                break
            row_count = row_count+2
            count = 0
            for column in row:
                count += 1
                # First column in the list is a gif image, 
                # which some times may have links too.
                # We need to skip this
                if count == 1:
                    continue

                try:
                    link = column.findAll("a")[0]['href']
                except:
                    continue
                text = self.clean(column)

                db_data = db.match(link)
                if db_data == None:
                # New data
                    print "-"*20
                    print text, link
                    update.append({'text' : page+' : '+text, 'link' : link})
                    db.add(text,link)
                else:
                # No new upadte
                    failed += 1
                    break
        return update

class text():
    def truncate(self, s):
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

if __name__ == "__main__":
    unical = unical()
    updates = unical.check_update()
    instance = Twitter()
    txt = text()

    for item in updates:
        if item:
            try:
                #instance.tweet(txt.truncate(item['text'])+' '+ unical.full_url(item['link']))
                print txt.truncate(item['text'])+' '+ unical.full_url(item['link'])
            except:
                continue

