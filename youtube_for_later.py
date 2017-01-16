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
    launch, prompting the user for the bot iD. It will then
    call the function again which will pass the sqlite vars
    to the main function.
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
    youTubeForLater()

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

    for x in range(numberNewMessages):

        try:
            text = jsonObject['result'][x]['message']['text']
            userID = jsonObject['result'][x]['message']['from']['id']
            messageID = jsonObject['result'][x]['message']['message_id']
            messageText = str(text)
            check = dbCheck(messageText, messageID, c, conn)
            sendMessage('farts are funny', userID, apiAddress)
        except KeyError:
            pass

        if check == 1:
            status = os.system('youtube-dl '+ messageText)
            if status == 0:
                message = 'Great success downloading ' + messageText
            else:
                message = 'No joy downloading ' + messageText

            sendMessage(message , userID, apiAddress)

    c.close()
    return

def sendMessage(message, userID, apiAddress):
    """
    """

    address = apiAddress + '/sendmessage?chat_id=' + str(userID) + '&text=' + message
    urllib.urlopen(address)
    return

def dbCheck(messageText, messageID, c, conn):

    try:
        dbEntry = 'insert into link values(' + str(messageID) +', \'%s\');' % messageText
        c.execute(dbEntry)
        conn.commit()
        return 1
    except db.IntegrityError:
        return 0

if __name__ == '__main__':
    youTubeForLater()
    #youtubedl('https://www.youtube.com/watch?v=DhiHpFm0YU4')
    #sendMessage()
