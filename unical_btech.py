#! /usr/bin/python


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

from unical import *

if __name__ == "__main__":
    unical = unical()
    updates = unical.check_update()
    instance = Twitter()
    txt = text()

    terms = ['b.tech', 'btech', 'b tech', 'bachelor of technology',
             'b.arch', 'barch', 'b arch', 'bachelor of architecture']
    updates = unical.search(updates, terms)

    for item in updates:
        if item:
            try:
                instance.tweet(txt.truncate(item['text'])+' '+ unical.link_to_url(item['link']))
                #print txt.truncate(item['text'])+' '+ unical.link_to_url(item['link'])
            except:
                continue
