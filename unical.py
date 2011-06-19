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
    web = urllib.urlopen("http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744&pop=1&page=0&Itemid=324")
    #web = urllib.urlopen("Notification.html")
    data = BeautifulSoup(web)
    i = 12

    row = data.findAll("tr")[i].findAll("td")[1].contents[1]

    #print row, "\n"
    print row.findAll("a"), "\n"
    link = row.findAll("a")[0]['href']

    text = row.renderContents()
    text = re.sub(r"<[^>]+>","", text)

    #print text
    #print link
    i = i+2
    push(text,"1",link)

fetch_data()
