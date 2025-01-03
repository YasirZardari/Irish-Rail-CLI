import typer
import requests
import xml.etree.ElementTree as ET

app = typer.Typer()

@app.command()
def getListOfStations():
    response = requests.get('https://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML')
    root = ET.fromstring(response.content)
    for child in root:
        print(child[0].text)

@app.command()
def getTrainsByStation(station: str):
    response = requests.get('https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc=' + station)
    root = ET.fromstring(response.content)
    for child in root:
        namespace = {'ns': 'http://api.irishrail.ie/realtime/'}
        destination = child.find('ns:Destination', namespace).text
        dueIn = child.find('ns:Duein', namespace).text
        late = child.find('ns:Late', namespace).text
        if destination != station:
            if late == '0':
                print(f"{destination} is due in {dueIn} mins")
            else:
                print(f"{destination} is due in {dueIn} mins (late by {late} mins)")

if __name__ == "__main__":  
    app()