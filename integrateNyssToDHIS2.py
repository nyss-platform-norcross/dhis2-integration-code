# importing the requests library 
import requests 
import uuid
from requests.auth import HTTPBasicAuth
import json
import csv
import hashlib

# load config file and configure necessary variables
with open("configuration.json") as json_file:
        config = json.load(json_file)
        loginPARAMS = {
            "username" : config["nyssUsername"],
            "password" : config["nyssPassword"]
        }
        dhisUsername = config["dhisUsername"]
        dhisPassword = config["dhisPassword"]
        nyssRootURL = config["nyssRootURL"]
        dhisRootURL = config["dhisRootURL"]
        organisationUnits = config["seedOrgUnit"]
        idSeedOrgUnit = config["idSeedOrgUnit"]
        nationalSocietyId = config["nationalSocietyId"]
        projectId = config["projectId"]

geoStructureNyss = {}

# api-endpoint nyss
loginURL = nyssRootURL + "authentication/login"
geoStructureURL = nyssRootURL + "nationalSocietyStructure/get?nationalSocietyId=" + str(nationalSocietyId)
reportsURL = nyssRootURL + "dhis2/list?nationalSocietyId=" + str(nationalSocietyId)
healthRisksURL = nyssRootURL + "healthRisk/list"
exportToCsv = nyssRootURL + "report/exportToCsv"

# api endpoint DHIS2
metadataURL = dhisRootURL + "metadata?"
organisationUnitsURL = dhisRootURL + "organisationUnits"
eventsURL = dhisRootURL + "events.json"

def getGeoStructure():
    with requests.Session() as session:
        post = session.post(loginURL, json=loginPARAMS)
        if post.json()['isSuccess'] is True:
            geoStructureNyss = session.get(geoStructureURL).json()
    for region in geoStructureNyss['value']['regions']:
        regionId = str(uuid.uuid4())[:11]
        organisationUnits['organisationUnits'].append(
            {
                "id": regionId,
                "code" : "nyss_region_" + region['name'],
                "level": 2,
                "openingDate": "2020-10-15T00:00:00.000",
                "name": region['name'],
                "shortName": "short" + region['name'],
                "parent" : {
                    "code" : "nyss_country_mandawi"
                }
            }
        )
        for district in region['districts']:
            districtId = str(uuid.uuid4())[:11]
            organisationUnits['organisationUnits'].append(
                {
                    "id": districtId,
                    "code" : "nyss_district_" + district['name'],
                    "level": 3,
                    "openingDate": "2020-10-15T00:00:00.000",
                    "name": district['name'],
                    "shortName": "short" + district['name'],
                    "parent": {
                        "code" : "nyss_region_" + region['name']
                    }
                }
            )
            for village in district['villages']:
                villageId = str(uuid.uuid4())[:11]
                organisationUnits['organisationUnits'].append(
                    {
                        "id": villageId,
                        "code" : "nyss_village_" + village['name'],
                        "level": 4,
                        "openingDate": "2020-10-15T00:00:00.000",
                        "name": village['name'],
                        "shortName": "short" + village['name'],
                        "parent" : {
                            "code" : "nyss_district_" + district['name']
                        }
                    }
                )
    if len(organisationUnits['organisationUnits']) > 1:
        print("Something was appended to the organisation units.")
def postGeoStructureToOrgUnitsDHIS2():
    print("Posting geo structure to DHIS2...")
    r = requests.post(metadataURL + "identifier=CODE", auth=(dhisUsername, dhisPassword), json=organisationUnits)
    if r.ok is True:
        print("Synchronizing geo structure: Post to DHIS2 returned ok")
def synchronizeOrgUnits():
    getGeoStructure()
    postGeoStructureToOrgUnitsDHIS2() 
    print("Please remeber to add organizations to the users access rights in dhis2 before doing anything else!")

def createDataElements():
    with open("data_elements_structure_for_import.json") as json_file:
        dataStructureDHIS2 = json.load(json_file)
        with requests.Session() as session:
            post = session.post(loginURL, json=loginPARAMS)
            options = []
            if post.json()['isSuccess'] is True:
                healthRisksList = session.get(healthRisksURL).json()
                for healthRisk in healthRisksList['value']:
                    options.append({
                        "code" : "nyss_" + str(healthRisk['name']).replace(" ", "_"),
                        "name" : healthRisk['name'],
                        "sortOrder" : healthRisk['id'],
                        "optionSet" : {
                            "code": "nyss_healthRiskEventsTitles"
                        }
                    })
                    dataStructureDHIS2['optionSets'][0]['options'].append({
                        "code" : "nyss_" + str(healthRisk['name']).replace(" ", "_")
                    })
                dataStructureDHIS2['options'] = options
        r = requests.post(metadataURL + "identifier=CODE", auth=(dhisUsername, dhisPassword), json=dataStructureDHIS2)
        if r.ok is True:
            print("Adding data elements: Post to DHIS2 returned ok")

def createProgram():
    with open("program_events.json") as json_file:
        dataStructureProgramDHIS2 = json.load(json_file)
        dataStructureProgramDHIS2['programs'][0]['organisationUnits'] = requests.get(organisationUnitsURL, auth=(dhisUsername, dhisPassword)).json()['organisationUnits']
        print()
        r = requests.post(metadataURL + "identifier=UID", auth=(dhisUsername, dhisPassword), json=dataStructureProgramDHIS2)
        if r.ok is True:
           print("Adding program & stage: Post to DHIS2 returned ok")
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
        1: synchronizeOrgUnits,
        2: createDataElements,
        3: createProgram,
        4: synchronizeReports
    }
    func = switcher.get(argument)
    func()

print("Please type + enter what you want to do:")
print("Synchronize organisational structure: 1")
print("Create necessary data elements & options: 2")
print("Create program & stages: 3")
print("Synchronize reports: 4")
switch(int(input()))