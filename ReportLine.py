#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from datetime import date
import pygal
from pygal.style import DarkStyle

year = date.today().year
monthinteger = datetime.datetime.now().strftime("%m")
month = datetime.date(1900, int(monthinteger), 1).strftime('%B')
