
import requests
import csv
import hashlib
import globalsNyss


def initializeVariables():
    global eventsURL, exportToCsv
    eventsURL = globalsNyss.dhisRootURL + "events.json"
    exportToCsv = globalsNyss.nyssRootURL + "report/exportToCsv"

def synchronizeReports():
    initializeVariables()
    with requests.Session() as session:
        #Get already existing events
        r = requests.get(eventsURL + "?orgUnit=" + globalsNyss.idSeedOrgUnit + "&ouMode=DESCENDANTS&paging=false&payloadFormat=json", auth=(globalsNyss.dhisUsername, globalsNyss.dhisPassword)).json()    
        eventIdentifiers = []
        if 'events' in r:
            for event in r['events']:
                for value in event['dataValues']:
                    if value['dataElement'] == "TtnAsCEqwf2":
                        eventIdentifiers.append(value['value'])
        #Proceed to new events
        post = session.post(globalsNyss.loginURL, json=globalsNyss.loginPARAMS)
        if post.json()['isSuccess'] is True:
            data = {
                    "reportsType": "Main",
                    "status": True,
                    "orderBy": "date",
                    "sortAscending": True,
                    "utcOffset": 0,
                    }
            reportsNyss = session.post(exportToCsv + "?projectID=" + str(globalsNyss.projectId), json = data)
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
        
        reports = formatReports(reportsReformatted, eventIdentifiers)
        r = requests.post(eventsURL + "?skipFirst=true&async=true&dryRun=false&dataElementIdScheme=UID&orgUnitIdScheme=CODE&eventIdScheme=UID&idScheme=UID&payloadFormat=json", auth=(globalsNyss.dhisUsername, globalsNyss.dhisPassword), json=reports)    
        if r.ok is True:
            print("Adding events: Post to DHIS2 returned ok")
  
def formatReports(reportsReformatted, eventIdentifiers):
    reports = {
        "events" : []
    }
    for report in reportsReformatted:
            if report['Health risk'] == 'Activity report' or report['Health risk'] == 'zero report':
                continue
            if '\ufeffID' in report:
                report['ID'] = report['\ufeffID']
                report.pop('\ufeffID', None)
            # Switch to use report id as basis for hash
            identifier = hashlib.md5(str.encode("nyss_" + report['ID'])).hexdigest()[0:11]
            if identifier in eventIdentifiers:
                continue
            else:
                if globalsNyss.useFlatOrganisationStructure:
                    codeOrgUnit = globalsNyss.codeSeedOrgUnit
                    nameSeedOrgUnit = globalsNyss.nameSeedOrgUnit
                else:
                    codeOrgUnit = "nyss_village_" + report['Village'],
                    nameSeedOrgUnit = report['Village']
                
                reports['events'].append(
                    {
                        "program" : "nyss_rep_pr",
                        "programStage" : "nyss_55c401",
                        "orgUnit" : codeOrgUnit,
                        "status": "COMPLETED",
                        "orgUnitName": nameSeedOrgUnit,
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
                                "dataElement": "fb21c617ca9",
                                "value": report['District']
                            },
                            {
                                "dataElement": "b048acb1e1a",
                                "value": report['Region']
                            },
                            {
                                "dataElement": "d8d6b1c48a4",
                                "value": report['Village']
                            },
                            {
                                "dataElement": "TtnAsCEqwf2",
                                "value": identifier
                            }
                        ]
                    }
                )
    return reports

if __name__ == "__main__":
    globalsNyss.initialize()
    synchronizeReports()
