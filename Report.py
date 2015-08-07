#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from datetime import date
import pygal
from pygal.style import DarkStyle

year = date.today().year
monthinteger = datetime.datetime.now().strftime("%m")
month = datetime.date(1900, int(monthinteger), 1).strftime('%B')

def chart(Numbers, FileName, ChartTitle):
        pie_chart = pygal.Pie(style=DarkStyle)
        pie_chart.title = '{title} usage in {MONTH} {YEAR} (in %)'.format(title=ChartTitle, MONTH=month, YEAR=year)
        pie_chart.add(Numbers[0][0], int(Numbers[0][1]))
        pie_chart.add(Numbers[1][0], int(Numbers[1][1]))
        pie_chart.add(Numbers[2][0], int(Numbers[2][1]))
        pie_chart.add(Numbers[3][0], int(Numbers[3][1]))
        pie_chart.add(Numbers[4][0], int(Numbers[4][1]))
        pie_chart.render()
        svgChart = 'Flask/static/img/Charts/svg/{title}-{date}.svg'.format(title=FileName, date=str(date.today()))
        pngChart = 'Flask/static/img/Charts/png/{title}-{date}.png'.format(title=FileName, date=str(date.today()))
        pie_chart.render_to_file(filename=svgChart)
        pie_chart.render_to_png(filename=pngChart)

def chart2(Numbers, FileName, ChartTitle):
        pie_chart = pygal.Pie(style=DarkStyle)
        pie_chart.title = '{title} usage in {MONTH} {YEAR} (in %)'.format(title=ChartTitle, MONTH=month, YEAR=year)
        pie_chart.add(Numbers[0][1], int(Numbers[0][2]))
        pie_chart.add(Numbers[1][1], int(Numbers[1][2]))
        pie_chart.add(Numbers[2][1], int(Numbers[2][2]))
        pie_chart.add(Numbers[3][1], int(Numbers[3][2]))
        pie_chart.add(Numbers[4][1], int(Numbers[4][2]))
        pie_chart.render()
        svgChart = '{title}-{date}.svg'.format(title=FileName, date=str(date.today()))
        pngChart = '{title}-{date}.png'.format(title=FileName, date=str(date.today()))
        pie_chart.render_to_file(svgChart)
        pie_chart.render_to_png(filename=pngChart)

if __name__=="__main__":
        chart()
