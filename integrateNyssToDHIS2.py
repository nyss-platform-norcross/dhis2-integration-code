import globalsNyss
import synchronizeGeostructure
import createDataElements
import createProgram
import synchronizeReportsToEvents

# Set up all necessary global variables
globalsNyss.initialize()
      
def switch(argument):
    switcher = {
        1: synchronizeGeostructure.synchronizeOrgUnits,
        2: createDataElements.createDataElements,
        3: createProgram.createProgramInDhis,
        4: synchronizeReportsToEvents.synchronizeReports
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
