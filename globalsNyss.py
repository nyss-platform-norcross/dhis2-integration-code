import json

def initialize():
    global loginURL, loginPARAMS, dhisUsername, dhisPassword
    global nyssRootURL, healthRisksURL, organisationUnitsURL, dhisRootURL, metadataURL
    global nationalSocietyId, projectId, organisationUnits, idSeedOrgUnit, codeSeedOrgUnit, nameSeedOrgUnit
    global useFlatOrganisationStructure
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
            codeSeedOrgUnit = config["codeSeedOrgUnit"]
            nameSeedOrgUnit = config["nameSeedOrgUnit"]
            nationalSocietyId = config["nationalSocietyId"]
            projectId = config["projectId"]
            useFlatOrganisationStructure = config["useFlatOrganisationStructure"]
    geoStructureNyss = {}
    # api-endpoint nyss
    loginURL = nyssRootURL + "authentication/login"
    reportsURL = nyssRootURL + "dhis2/list?nationalSocietyId=" + str(nationalSocietyId)
    healthRisksURL = nyssRootURL + "healthRisk/list"
    # api endpoint DHIS2
    metadataURL = dhisRootURL + "metadata?"
    organisationUnitsURL = dhisRootURL + "organisationUnits"