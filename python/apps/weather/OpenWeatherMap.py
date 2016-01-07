from parLED.core.Interface import SerialRGB
from parLED.core.Temperature import farenheit2rgb, celsius2rgb
from datetime import datetime
from lxml import objectify as Obj, etree as ET
import time
import requests

INTERVAL = (60)/1

ApiKey = ""
URL = ""
CountryCode = ""
ZipCode = ""


def getCurrentWeather():
    global ApiKey
    global CountryCode
    global ZipCode
    
    url = URL % \
    {
        "CountryCode":CountryCode,
        "ZipCode":ZipCode
    }
    
    params = \
    {
        "APPID" : ApiKey,
        "mode" : "xml",
        "units" : "imperial"
    }
    
    res = requests.get(url, params=params)
    if res.ok or res.status_code is 200:
        return Obj.fromstring(res.text)
    else:
        return None


if __name__ == "__main__":
    Strip = SerialRGB("/dev/ttyUSB0", baud=115200)
    
    FirstRun = True
    lastUpdated = datetime.now()
    
    try:
        while 1:
            if ((datetime.now() - lastUpdated).seconds == INTERVAL) or (FirstRun):
                data = getCurrentWeather()
                if  isinstance(data, Obj.ObjectifiedElement):
                    print ET.tostring(data, pretty_print=1, xml_declaration=1, encoding="utf-8")
                    temp = farenheit2rgb(float(data.temperature.attrib["value"]))
                    Strip.cross_fade(temp)
                    lastUpdated = datetime.now()
                    if FirstRun:
                        FirstRun = False
                else:
                    print "Failed to parse data. Time:", datetime.now()
                    continue
                time.sleep(2)
    except KeyboardInterrupt:
        print "Aborting!"
        sys.exit(1)
    except Exception, e:
        import traceback
        traceback.print_exc()
            
