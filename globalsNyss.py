import json

def initialize():
    global loginURL, loginPARAMS, nyssRootURL, healthRisksURL, organisationUnitsURL, nationalSocietyId, projectId, dhisRootURL, organisationUnits, idSeedOrgUnit, metadataURL, dhisUsername, dhisPassword
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
    reportsURL = nyssRootURL + "dhis2/list?nationalSocietyId=" + str(nationalSocietyId)
    healthRisksURL = nyssRootURL + "healthRisk/list"
    # api endpoint DHIS2
    metadataURL = dhisRootURL + "metadata?"
    organisationUnitsURL = dhisRootURL + "organisationUnits"