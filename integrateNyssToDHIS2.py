# importing the requests library 
import requests 
import uuid
from requests.auth import HTTPBasicAuth
import json
import csv
import hashlib

import globalsNyss
import synchronizeGeostructure
import createDataElements
import createProgram

# Set up all necessary global variables
globalsNyss.initialize()

def synchronizeReports():
    reports = {
        "events" : []
    }
    with requests.Session() as session:
        #Get already existing events
        r = requests.get(eventsURL + "?orgUnit=" + idSeedOrgUnit + "&ouMode=DESCENDANTS&paging=false&payloadFormat=json", auth=(dhisUsername, dhisPassword), json=reports).json()    
        eventIdentifiers = []
        for event in r['events']:
            for value in event['dataValues']:
                if value['dataElement'] == "TtnAsCEqwf2":
                    eventIdentifiers.append(value['value'])
        #Proceed to new events
        post = session.post(loginURL, json=loginPARAMS)
        if post.json()['isSuccess'] is True:
            data = {
                    "reportsType": "Main",
                    "status": True,
                    "orderBy": "date",
                    "sortAscending": True,
                    "utcOffset": 0,
                    }
            reportsNyss = session.post(exportToCsv + "?projectID=" + str(projectId), json = data)
            cr = csv.reader(reportsNyss.content.decode('utf-8').splitlines(), delimiter=',')
            reportsList = list(cr)
            reportsReformatted = []
            for index,report in enumerate(reportsList):
                if index == 0:
                    continue
                reportDict = {}
                for indexInner, item in enumerate(report):
                    reportDict[reportsList[0][indexInner]] = item    
                reportsReformatted.append(reportDict)
            # correct for faulty naming in date key
            for report in reportsReformatted:
                report['Date'] = report['\ufeffDate']
                report.pop('\ufeffDate')
        for report in reportsReformatted:
            identifier = hashlib.md5(str.encode("nyss_" + report['Phone number'] + "_" + report['Date'] + "_" + report['Time'])).hexdigest()[0:11]
            if identifier in eventIdentifiers:
                continue
            else:
                reports['events'].append(
                    {
                        "program" : "nyss_rep_pr",
                        "programStage" : "nyss_55c401",
                        "orgUnit" : "nyss_village_" + report['Village'],
                        "status": "COMPLETED",
                        "orgUnitName": report['Village'], 
                        "eventDate": report['Date'] + "T" + report['Time'] + ":00.000",
                        "completedDate": report['Date'] + "T" + report['Time'],
                        "dataValues" : [
                            {
                                "dataElement" : "rANqSWN0Ehq",
                                "value" : str(report['Male 0–4 years'])
                            },
                            {
                                "dataElement" : "go4soBvUeOH",
                                "value" : str(report['Female 0–4 years'])
                            },
                            {
                                "dataElement" : "TtnAvCEqnf5",
                                "value" : str(report['Male 5 years or older'])
                            },
                            {
                                "dataElement" : "s9M3Gq8LgPs",
                                "value" : str(report['Female 5 years and older'])
                            },
                            {
                                "dataElement": "xJSf5LyGP94",
                                "value": "nyss_" + str(report['Health risk']).replace(" ", "_")
                            },
                            {
                                "dataElement": "xXkaRheq7VM",
                                "value": "[" + report['Location'].split('/')[0] + "," + report['Location'].split('/')[1] + "]"
                            },
                            {
                                "dataElement": "TtnAsCEqwf2",
                                "value": identifier
                            }
                        ]
                    }
                )
        r = requests.post(eventsURL + "?skipFirst=true&async=true&dryRun=false&dataElementIdScheme=UID&orgUnitIdScheme=CODE&eventIdScheme=UID&idScheme=UID&payloadFormat=json", auth=(dhisUsername, dhisPassword), json=reports)    
        if r.ok is True:
            print("Adding events: Post to DHIS2 returned ok")
        
def switch(argument):
    switcher = {
        1: synchronizeGeostructure.synchronizeOrgUnits,
        2: createDataElements.createDataElements,
        3: createProgram.createProgramInDhis,
        4: synchronizeReports
    }
    func = switcher.get(argument)
    func()

if __name__ == "__main__":
    globalsNyss.initialize()
    print("Please type + enter what you want to do:")
    print("Synchronize organisational structure: 1")
    print("Create necessary data elements & options: 2")
    print("Create program & stages: 3")
    print("Synchronize reports: 4")
    switch(int(input()))
