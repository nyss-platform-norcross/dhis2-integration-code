import json
import requests
import globalsNyss

def createDataElements():
    with open("data_elements_structure_for_import.json") as json_file:
        dataStructureDHIS2 = json.load(json_file)
        with requests.Session() as session:
            post = session.post(globalsNyss.loginURL, json=globalsNyss.loginPARAMS)
            options = []
            if post.json()['isSuccess'] is True:
                healthRisksList = session.get(globalsNyss.projectHealthRisksURL).json()
                for healthRisk in healthRisksList['value']['projectHealthRisks']:
                    options.append({
                        "code" : "nyss_" + str(healthRisk['healthRiskName']).replace(" ", "_"),
                        "name" : healthRisk['healthRiskName'],
                        "sortOrder" : healthRisk['id'],
                        "optionSet" : {
                            "code": "nyss_healthRiskEventsTitles"
                        }
                    })
                    dataStructureDHIS2['optionSets'][0]['options'].append({
                        "code" : "nyss_" + str(healthRisk['healthRiskName']).replace(" ", "_")
                    })
                dataStructureDHIS2['options'] = options
        r = requests.post(globalsNyss.metadataURL + "identifier=CODE", auth=(globalsNyss.dhisUsername, globalsNyss.dhisPassword), json=dataStructureDHIS2)
        if r.ok is True:
            print("Adding data elements: Post to DHIS2 returned ok")
