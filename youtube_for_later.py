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

def installer():

    createDB()
    token = raw_input('Please enter your Telegram Bot token:')
    f = open('.youtube_for_later','w')
    f.write(name + '\n')
    f.write(token)

def createDB():

    conn = db.connect('.telegram_for_later.db')
    c = conn.cursor()

    try:
        text='create table link(links varchar primary key);'
        c.execute(text)

    except db.OperationalError:
        pass

    return



if __name__ == '__main__':
    installer()
