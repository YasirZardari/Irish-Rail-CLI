import typer
import requests
import xml.etree.ElementTree as ET

app = typer.Typer()

@app.command()
def hello():
    print("Hello")
    response = requests.get('https://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML')
    root = ET.fromstring(response.content)
    for child in root:
        print(child.tag, child.attrib)

if __name__ == "__main__":
    app()