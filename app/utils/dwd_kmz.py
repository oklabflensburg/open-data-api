import zipfile
from lxml import etree
import re
from datetime import datetime
from io import BytesIO
import aiohttp
from fastapi import HTTPException


def numeric(s: str) -> float | int:
    try:
        if '-' in s:
            return 0
        return int(s)
    except ValueError:
        return round(float(s), 1)


def get_element_value_as_list(tree: etree._ElementTree, element: str) -> list:
    for df in tree.xpath(f'////*[name()="dwd:Forecast" and @*[name()="dwd:elementName" and .="{element}"]]'):
        elements = re.sub(
            r'\s+', ';', str(df.getchildren()[0].text).lstrip(' '))
        lst = elements.split(";")
        return [numeric(item) for item in lst]
    return []


def analyse(tree: etree._ElementTree) -> dict:
    result = {}

    # Station ID
    for df in tree.xpath('////*[name()="dwd:Issuer"]'):
        result["issuer"] = df.text.strip()

    # Product ID
    for df in tree.xpath('////*[name()="dwd:ProductID"]'):
        result["productId"] = df.text.strip()

    # generating process
    for df in tree.xpath('////*[name()="dwd:GeneratingProcess"]'):
        result["generatingProcess"] = df.text.strip()

    # Location name
    for df in tree.xpath('////*[name()="kml:description"]'):
        result["location"] = df.text.strip()

    # Issue time
    for df in tree.xpath('////*[name()="dwd:IssueTime"]'):
        dt = datetime.fromisoformat(df.text.replace("Z", "+00:00"))
        result["issue_time"] = dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    result['station'] = {}
    # Station id
    for df in tree.xpath('//*[name()="kml:Placemark"]/*[name()="kml:name"]'):
        result['station']["name"] = df.text.strip()

    # Station name
    for df in tree.xpath('//*[name()="kml:Placemark"]/*[name()="kml:description"]'):
        result['station']["description"] = df.text.strip()

    # Time steps
    time_stamps = []
    for df in tree.xpath('//*[name()="dwd:ForecastTimeSteps"]'):
        for timeslot in df:
            dt = datetime.fromisoformat(timeslot.text.replace("Z", "+00:00"))
            time_stamps.append(dt.strftime("%Y-%m-%dT%H:%M:%S%z"))
    result['station']["timeSteps"] = time_stamps

    # Weather values
    def add_transformed(key: str, values: list, transform=None):
        if transform:
            result['station'][key] = [transform(v) for v in values]
        else:
            result['station'][key] = values

    add_transformed("PPPP", get_element_value_as_list(
        tree, 'PPPP'), lambda x: round(float(x) / 100.0, 2))
    add_transformed("FX1", get_element_value_as_list(tree, 'FX1'))
    add_transformed("ww", get_element_value_as_list(tree, 'ww'))
    add_transformed("SunD", get_element_value_as_list(
        tree, 'SunD'), lambda x: round(float(x), 2))

    TX = get_element_value_as_list(tree, 'TX')
    result["TX"] = [round(float(t) - 273.15, 2) if int(t)
                    > 99 else t for t in TX]

    TN = get_element_value_as_list(tree, 'TN')
    result["TN"] = [round(float(t) - 273.15, 2) if int(t)
                    > 99 else t for t in TN]

    add_transformed("Neff", get_element_value_as_list(
        tree, 'Neff'), lambda x: round(float(x) * 8 / 100, 2))
    add_transformed("R101", get_element_value_as_list(tree, 'R101'))

    return result


async def retrieve_station_kmz(station_id) -> dict:
    url = (
        f'https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/single_stations/{station_id}/kml/MOSMIX_L_LATEST_{station_id}.kmz'
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f'DWD returned status code {response.status}'
                    )

                content = await response.read()
                with zipfile.ZipFile(BytesIO(content), 'r') as kmz:
                    kml_filename = kmz.namelist()[0]
                    tree = etree.parse(kmz.open(kml_filename))
                    return analyse(tree)
    except aiohttp.ClientConnectionError as e:
        raise HTTPException(
            status_code=503, detail=f'Could not connect to DWD: {str(e)}')
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f'Error fetching data from DWD: {str(e)}')
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=422, detail='Received invalid data format from DWD')
