#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#  youtube_for_later.py
#
#  Copyright 2016 Travis Neiheisel <tneiheis@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
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
        return

    createTokenTable(conn, c)
    youTubeForLater()

    return

def main(conn, c):
    """
    This function accomplishes the bulk of the tasks. It starts out by
    extracting the bot token from the database. It then makes a url querry
    against the bot api which returns a json object with all the messages on
    the server. The function then sends the message ID off to determine if the
    message is new. ONce determined to be new, the function initiates the
    youtube-dl function for the message. The function then sends a message to
    the user using the url querry regarding the status of the downloads.
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
        except KeyError:
            pass

        if check == 1:
            status = os.system('youtube-dl '+ messageText)
            if status == 1:
                message = 'No joy downloading ' + messageText
            #else:
            #    message = 'Successfully downloaded ' + messageText

            address = apiAddress + '/sendmessage?chat_id=' + str(userID) +\
            '&text=' + message
            urllib.urlopen(address)

    c.close()
    return

def sendMessage (apiAddress, message, userID):


def dbCheck(messageText, messageID, c, conn):
    """
    This function checks to see if the message ID already exists in the db and
    , if so, returns a 0 so that the link is not downloaded a 2nd time. If the
    message ID is new, it is added to the db and a 1 is returned indicating the
    file should be downloaded.
    """

    try:
        dbEntry = 'insert into link values(' + str(messageID) +', \'%s\');' % messageText

    except db.IntegrityError:
        return 0

    c.execute(dbEntry)
    conn.commit()
    return 1

if __name__ == '__main__':
    youTubeForLater()
