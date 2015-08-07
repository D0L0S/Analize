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
        svgChart = 'Flask/static/img/Charts/svg/{title}-{date}.svg'.format(title=FileName, date=str(date.today()))
        pngChart = 'Flask/static/img/Charts/png/{title}-{date}.png'.format(title=FileName, date=str(date.today()))
        pie_chart.render_to_file(svgChart)
        pie_chart.render_to_png(filename=pngChart)

def chart3(fromDate, toDate, ffNumbers, chromeNumbers, ieNumbers, safariNumbers):
        line_chart = pygal.StackedLine(fill=True, style=DarkStyle)
        line_chart.title = 'Browser Trends (in %)'
        line_chart.x_labels = map(str, range(fromDate, toDate))
        line_chart.add('Firefox', ffNumbers)    #[None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
        line_chart.add('Chrome', chromeNumbers) #[None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
        line_chart.add('IE', ieNumbers)         #[85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        line_chart.add('Safari', safariNumbers) #[14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
        line_chart.render()
        svgChart = 'Flask/static/img/Charts/svg/BrowserTrends-{date}.svg'.format(date=str(date.today()))
        pngChart = 'Flask/static/img/Charts/png/BrowserTrends-{date}.png'.format(date=str(date.today()))
        line_chart.render_to_file(svgChart)
        line_chart.render_to_png(filename=pngChart)

if __name__=="__main__":
        chart()
