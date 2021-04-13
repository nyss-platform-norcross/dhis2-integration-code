import requests
import json
import globalsNyss

def createProgramInDhis():
    with open("program_events.json") as json_file:
        dataStructureProgramDHIS2 = json.load(json_file)
        dataStructureProgramDHIS2['programs'][0]['organisationUnits'] = requests.get(globalsNyss.organisationUnitsURL, auth=(globalsNyss.dhisUsername, globalsNyss.dhisPassword)).json()['organisationUnits']
        r = requests.post(globalsNyss.metadataURL + "identifier=UID", auth=(globalsNyss.dhisUsername, globalsNyss.dhisPassword), json=dataStructureProgramDHIS2)
        if r.ok is True:
           print("Adding program & stage: Post to DHIS2 returned ok")
