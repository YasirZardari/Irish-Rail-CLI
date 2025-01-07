import typer
import requests
import xml.etree.ElementTree as ET

app = typer.Typer()

@app.command()
def getListOfStations(do_print: bool = True):
    response = requests.get('https://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML')
    root = ET.fromstring(response.content)
    station_list = []
    for child in root:
        station_name = child[0].text
        if (do_print):
            print(station_name)
        station_list.append(station_name)
    return station_list
    
@app.command()
def getTrainsByStation(station: str, minutes: str = 'false'):
    """
    Fetch and display due trains for the given station.
    
    - station: The name of the station to fetch due trains for (mandatory).
    - minutes: Optional filter to show trains due within the next N minutes (between 5 and 90).
    """

    if station not in getListOfStations(False):
        print("Please specify a valid station name")

    response = None
    if not minutes.isdigit() or (int(minutes) >= 5 and int(minutes) <= 90):
        response = requests.get('https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc=' + station)
    else:
        print("Minutes parameter must be a valid integer between 5 and 90")
        return 

    root = ET.fromstring(response.content)
    for child in root:
        namespace = {'ns': 'http://api.irishrail.ie/realtime/'}
        destination = child.find('ns:Destination', namespace).text
        dueIn = child.find('ns:Duein', namespace).text
        late = child.find('ns:Late', namespace).text
        if destination != station and (minutes == 'false' or int(dueIn) < int(minutes)):
            if late == '0':
                print(f"{destination} is due in {dueIn} mins")
            else:
                print(f"{destination} is due in {dueIn} mins (late by {late} mins)")

if __name__ == "__main__":  
    app()