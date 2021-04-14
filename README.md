# dhis2-integration-code

This is a python script allowing to configure a dhis2 instance with the Nyss data structure and to push nyss reports to dhis2 events. 

## 1. Usage


### 1.1. Synchronize organisational structure

If you type 1 and press enter, depending on your configuration of the "useFlatOrganisationalStructre", the script will either create one level 1 seed organisational unit in DHIS2 (flat structre), or synchronize the current geographical structure from Nyss to DHIS2. 

If you set the "useFlatOrganisationalStructure" variable to false, you need to run this option whenever you add a geographical level to Nyss (region, district or village).
## 2. Configuration

The script relies on a number configuration variables to be set in the file "configuration.json". These depend upon your user credentials in Nyss and DHIS2, your URL and your level 1 organisational unit in DHIS2. Below is an example configuration that uses the Nyss demo site, a publicly available login to the demo site and a local DHIS2 instance set up with the default credentials.

The seed organisational unit needs to be a level 1 org unit in DHIS2. If it already exists fill in the id, code, name and shortName defined in DHIS2. Otherwise the one defined will be created. With the variable "useFlatOrganisationStructure" you can configure the script to either tie every report to the level 1 (seed) organisational unit (flat structure), or do synchronize the Nyss structure to DHIS2 and tie every report to their respective level. 

The variables "nationalSocietyId" and "projectId" define the the respective variables within Nyss. The credentials set up for Nyss need to have Manager level access to the defined National Society. 

The credentials set up for DHIS2 need to have access levels set to the level 1 (seed) organisational unit. If you do create a new one using this script, make sure you set the access levels within DHIS2 before you move to options 2,3 & 4 in the script. 

```
{   
    "nyssUsername": "mary_manager@example.com",
    "nyssPassword": "DemoP@ssw0rd",
    "dhisUsername": "admin",
    "dhisPassword": "district",
    "nyssRootURL" : "https://demo.rcnyss.org/api/",
    "dhisRootURL" : "http://localhost:8080/api/",
    "seedOrgUnit" : { "organisationUnits": [
                            {
                                    "id" : "nyssMandawi",
                                    "code" : "nyss_country_mandawi",
                                    "level": 1,
                                    "openingDate": "2020-10-15T00:00:00.000",
                                    "name": "Mandawi",
                                    "shortName": "mand"
                            }
                        ]},
    "nameSeedOrgUnit" : "Mandawi",
    "codeSeedOrgUnit" : "nyss_country_mandawi",
    "idSeedOrgUnit" : "nyssMandawi",
    "nationalSocietyId" : "1",
    "projectId" : "1",
    "useFlatOrganisationStructure" : true
}
```

## 3. Usage

Run

```
python3 integrateNyssToDHIS2.py
```

and select your choice in the interactive command line interface.

### 3.1. First time 

Select 1, to synchronize the geographical structure of Nyss to DHIS2. If you set up a new level 1 organisation unit in DHIS2, go to your DHIS2 instance and set access rights to your user. 

Run the script, select option 2. Within DHIS2 under Maintenance -> Data Elements, you should see a bunch of new elements. 

Run the script, select option 3. Within DHIS2 under Maintenace -> Program, you should see a new program. 

If all went well, you can now run the script and select option 4 to get all new reports from Nyss and push them as events to DHIS2. 

### 3.2. Add new geographical structure from Nyss to DHIS2

Run the script and select 1. 

### 3.3. Synchronize new reports

Run the script and select 4. You can also directly run 
```
python3 synchronizeReportsToEvents.py
```
