#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#  untitled.py
#
#  Copyright 2016 Unknown <travis@arch>
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
#
#
import os
import urllib
import re
import sqlite3 as db

token = '164912346:AAEzHBhxxzad6n6AHWydXOicgjVicq7ALkw'
address = 'https://api.telegram.org/bot' + token

def getMessages(address):

    createDB()
    marker = False
    count = 1
    site = urllib.urlopen(address + '/getupdates').read()
    data = re.split('"', site)
    target = []
    conn = db.connect('/home/tankrtoad/.telegram-youtubeDL.db')
    c = conn.cursor()

    for x in range(len(data)):
	if data[x] == 'text':
            if data[x+2][:4] == 'http':
		target.append(data[x+2])

    for lnks in range(len(target)):
        target[lnks] = cleanUrl(target[lnks])

    for lnk in target:

        try:
            textLink = str(lnk)
            text = 'insert into link values ("%s");' % textLink
            c.execute(text)

        except db.IntegrityError:
            pass

        else:
            conn.commit()
            sendMessage(address, 'Downloading Song #%s' % count)
            youtubeDL(lnk)
            marker = True
            count += 1

    if marker == True:
	sendMessage(address, 'All downloads complete')

    return

def sendMessage(address, words):
    address += '/sendmessage?chat_id=62818324&text=%s' % words
    site = urllib.urlopen(address)
    return

def youtubeDL (urlname):
    osInput = 'youtube-dl -x --audio-format "mp3" --audio-quality 0 --embed-thumbnail %s' % urlname
    os.system(osInput)
    return

def createDB():

    conn = db.connect('/home/tankrtoad/.telegram-youtubeDL.db')
    c = conn.cursor()

    try:
        text='create table link(links varchar primary key);'
        c.execute(text)

    except db.OperationalError:
        pass

    return

def cleanUrl(dirtyUrl):

    cleanLink = ''

    for y in dirtyUrl:
	if y != '\\':
            cleanLink += y
#        print cleanLink
    return cleanLink

getMessages(address)
