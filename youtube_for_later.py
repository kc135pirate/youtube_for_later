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

import os
import urllib
import re
import sqlite3 as db

def installer():

    setupVariable = createDB()

    if setupVariable == 0:

        conn = db.connect('.telegram_for_later.db')
        c = conn.cursor()
        c.execute('create table token(ID varchar primary key);')
        token = raw_input('Please enter your Telegram Bot token:')
        c.execute('insert into token values ("%s");') % token
        conn.commit

    return

def createDB():

    conn = db.connect('.telegram_for_later.db')
    c = conn.cursor()

    try:
        text='create table link(links varchar primary key);'
        c.execute(text)

    except db.OperationalError:
        return 1

    return 0



if __name__ == '__main__':
    installer()
