import urllib
from BeautifulSoup import BeautifulSoup
import re
import MySQLdb
import cPickle as Pickle
import os

PICKLE_FILE = "lastupdate.p"

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

def store():
    pfile = open(PICKE_FILE, 'wb')
    pickle.dump(data, pfile)
    pfile.close()
    return

def read_old_data():
    if os.path.isfile(PICKLE_FILE):
        data = {}
        pfile = open(PICKLE_FILE, 'rb')
        data = pickle.load(pfile)
        pfile.close()
        return data
    return None

def fetch_data():
    top = True
    #web = urllib.urlopen("http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324")
    web = urllib.urlopen("Notification.html")
    data = BeautifulSoup(web)
    i = 12

    lastupdate = read_old_data()

    while 1:
        try:
            row = data.findAll("tr")[i].findAll("td")
        except:
            return
        for rows in row:
            try:
                link = rows.findAll("a")[0]['href']
            except:
                continue
            text = rows.renderContents()
            text = re.sub(r"<[^>]+>","", text)
            text = re.sub(r"&nbsp;","", text)
            text = re.sub(r"&amp;","&",text)
#        print "--------------------------------------------------------"
#            print link
#            print text

            if top:
                data = {'text' : text, 'link' : link}
                store(data)
                top = False

            query = "SELECT (id, content, type, link) FROM post WHERE (content = %s)", % text
            check = pull(query)

#    if :
        push(text,"1",link)
#        break
#    else:
#        query = "SELECT (id, content, type, link) FROM post WHERE"
#        send_mail("")
#        send_sms("")
        i = i+2

fetch_data()
