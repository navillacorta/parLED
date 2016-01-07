from parLED.core.Interface import SerialRGB
from parLED.core.Temperature import farenheit2rgb, celsius2rgb
from datetime import datetime
from lxml import objectify as Obj, etree as ET
import time
import requests


INTERVAL = (60*24)/5

ApiKey = ""
URL = ""


def getCurrentWeather():
    global ApiKey
    
    url = URL % {"ApiKey":ApiKey}
    res = requests.get(url)
    if res.ok or res.status_code is 200:
        return Obj.fromstring(res.text)
    else:
        return None

def main():
    Strip = SerialRGB("/dev/ttyUSB0", baud=115200)
    
    FirstRun = True
    lastUpdated = datetime.now()
    
    try:
        while 1:
            if ((datetime.now() - lastUpdated).seconds == INTERVAL) or (FirstRun):
                data = getCurrentWeather()
                if  isinstance(data, Obj.ObjectifiedElement):
                    print ET.tostring(data, pretty_print=1, xml_declaration=1, encoding="utf-8")
                    temp = farenheit2rgb(float(data.current_observation.temp_f.text))
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

if __name__ == "__main__":
    main()
