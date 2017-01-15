#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#  youtube_for_later.py
#
#  Copyright 2016 Travis Neiheisel <tneiheis@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import os
import urllib
import sqlite3 as db
import json

def createTokenTable(conn, c):
    """This will only run on the initial setup of the
    script. It will query the user for the telegram bot
    ID and will store it in the sqlite database.
    """


    c.execute('create table token(bot_token varchar);')
    token = raw_input('Please enter your Telegram Bot token:')
    dbEntry = 'insert into token (bot_token) values (\'%s\');' % token
    c.execute(dbEntry)
    conn.commit()
    return

def youTubeForLater():
    """This function will check for the existance of the
    sqlite database and create it if it doesn't exist. If
    the database doesn't exist, the installer script will
    launch, prompting the user for the bot iD.
    """


    conn = db.connect('.youtube_for_later.db')
    c = conn.cursor()
    try:
        text='create table link(chatid int primary key, links varchar);'
        c.execute(text)
    except db.OperationalError:
        main(conn, c)
        c.close()
        return

    createTokenTable(conn, c)

    return

def main(conn, c):
    """
    """

    cursorObject = c.execute('select bot_token from token;')
    for x in cursorObject:
        token = x[0]

    apiAddress = 'https://api.telegram.org/bot' + token
    messageJSON = urllib.urlopen( apiAddress + '/getupdates')
    jsonObject = json.load(messageJSON)
    numberNewMessages = len(jsonObject['result'])
    #print numberNewMessages
    for x in range(numberNewMessages):

        try:
            messageText = jsonObject['result'][x]['message']['text']
            userID = jsonObject['result'][x]['message']['from']['id']
            messageID = jsonObject['result'][x]['message']['message_id']
            check = dbCheck(messageText, messageID, c, conn)
            print check

        except KeyError:
            pass


        check = dbCheck(messageText, messageID, c, conn)


    c.close()
    return

def youtubedl(link, apiAddress):
    """
    """

    x = os.system('youtube-dl '+ link)
    if x == 0:
        print 'success'
    else:
        print "failz"

    return


def dbCheck(messageText, messageID, c, conn):

    try:
        dbEntry = 'insert into link values(' + messageID +', \'%s\');' % messageText
        c.execute(dbEntry)
        c.commit()
    except:
        pass

    return 1


'''
def sendMessage(text, apiAddress):
    """
    """

    return
'''

if __name__ == '__main__':
    youTubeForLater()
    #youtubedl('https://www.youtube.com/watch?v=DhiHpFm0YU4')
