import urllib
from BeautifulSoup import BeautifulSoup
import re
import MySQLdb

DBHOST = "localhost"
DBPASS = "root"
DBUSER = "root"
DB = "test"

db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)

def push(text, content_type,link):

    cursor = db.cursor()
    query = "INSERT INTO post (content, type, link) VALUES (\"%s\", %s, \"%s\")" % (text, 1, link)
    cursor.execute(query)

    rows = int(cursor.rowcount)


def fetch_data():
    #web = urllib.urlopen("http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324")
    web = urllib.urlopen("Notification.html")
    data = BeautifulSoup(web)
    i = 12

    while 1:
        print "--------------------------------------------------------"
        row = data.findAll("tr")[i].findAll("td")
        for rows in row:
            try:
                link = rows.findAll("a")[0]['href']
                print "+++++++++++++++++++++++"
                print link
            except:
                continue
            text = rows.renderContents()
            text = re.sub(r"<[^>]+>","", text)
            text = re.sub(r"&nbsp;","", text)
            text = re.sub(r"&amp;","&",text)
            
            #print link
            print text
        i = i+2
    #push(text,"1",link)

fetch_data()
