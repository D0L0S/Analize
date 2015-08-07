#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from datetime import date
import oauth2client
from oauth2client import client, tools
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery, errors
from googleapiclient.discovery import build
from googleapiclient.http import HttpError
import httplib2
from operator import itemgetter
import sqlite3

today = date.today()
database = 'DATABASE'

filename = 'PROJECT_FILE.p12'
f = file(filename, 'rb')
key = f.read()
f.close()

AnalyticsID = "APP_ID"

def sortList(List): 
        # Sort and shorten the list of tuples provided to the top 5
        sortedList = sorted(List,key=itemgetter(1), reverse=True)
        NewList = sortedList[:5]# Number can be moved to config file
        return NewList

def Analytic(startDate, stopDate, report):
        # create the credentials
        credentials = SignedJwtAssertionCredentials('13829033349-c19cganpocr54ta85soib19t5fr6pnq8@developer.gserviceaccount.com', key, scope='https://www.googleapis.com/auth/analytics.readonly')

        # authorize the http instance with these credentials
        http = httplib2.Http()
        http = credentials.authorize(http)
    
        service = build('analytics', 'v3', http=http)

        # build the querys
        top_browsers = service.data().ga().get(
                ids=AnalyticsID,
                start_date= str(startDate),
                end_date= str(stopDate),
                metrics='ga:sessions',
                dimensions='ga:browser'
        )

        browser_versions = service.data().ga().get(
                ids=AnalyticsID,
                start_date= str(startDate),
                end_date= str(stopDate),
                metrics='ga:sessions',
                dimensions='ga:browser,ga:browserVersion'
        )

        TopFive = []
        IEVersion = []
        AndroidVersions = []
        
        try:

                today = date.today()

                versions = browser_versions.execute()
                versionbrowsers = versions['rows']
                for version in versionbrowsers:
                        versiontup = tuple((version[0], version[1], int(version[2])))
                        if version[0] == 'Internet Explorer': IEVersion.append(version)
                        elif version[0] == 'Android Browser': AndroidVersions.append(version)
                        else:pass

                result = top_browsers.execute()
                browsers = result['rows']
                for browser in browsers:
                        tup = tuple((browser[0], int(browser[1])))
                        TopFive.append(tup)

                sortedList = sortList(TopFive)
                sortedIEVersion = sortList(IEVersion)
                sortedAndroidVersion = sortList(AndroidVersions)

                if report == "Android":return sortedAndroidVersion
                elif report == "IE": return sortedIEVersion
                elif report == "TopFive": return sortedList
                else: return 0

        # handle errors in constructing a query
        except TypeError, error:
                print " [-] Error in constructing query : {e}".format(e=error)

        # handle api service errors
        except HttpError, error:
                print " [-] API error : {err}\n               {errReason}".format(err = error.resp.status, errReason = error._get_reason())
