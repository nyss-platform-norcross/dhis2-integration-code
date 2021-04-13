import requests 
import globalsNyss
import uuid

def initializeVariables():
    global geoStructureURL
    geoStructureURL = globalsNyss.nyssRootURL + "nationalSocietyStructure/get?nationalSocietyId=" + str(globalsNyss.nationalSocietyId)

def getGeoStructure():
    with requests.Session() as session:
        post = session.post(globalsNyss.loginURL, json=globalsNyss.loginPARAMS)
        if post.json()['isSuccess'] is True:
            geoStructureNyss = session.get(geoStructureURL).json()
    for region in geoStructureNyss['value']['regions']:
        regionId = str(uuid.uuid4())[:11]
        globalsNyss.organisationUnits['organisationUnits'].append(
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
            globalsNyss.organisationUnits['organisationUnits'].append(
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
                globalsNyss.organisationUnits['organisationUnits'].append(
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
    if len(globalsNyss.organisationUnits['organisationUnits']) > 1:
        print("Something was appended to the organisation units.")
def postGeoStructureToOrgUnitsDHIS2():
    print("Posting geo structure to DHIS2...")
    r = requests.post(globalsNyss.metadataURL + "identifier=CODE", auth=(globalsNyss.dhisUsername, globalsNyss.dhisPassword), json=globalsNyss.organisationUnits)
    if r.ok is True:
        print("Synchronizing geo structure: Post to DHIS2 returned ok")
def synchronizeOrgUnits():
    initializeVariables()
    getGeoStructure()
    postGeoStructureToOrgUnitsDHIS2() 
    print("Please remeber to add organizations to the users access rights in dhis2 before doing anything else!")
