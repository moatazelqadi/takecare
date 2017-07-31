key = ''
vicRoadsToken = ''
import requests as req
## This function code is from https://github.com/openeventdatabase/backend/blob/master/polyline.py
## Function name changed due to an apparent conflict in the project.
def polylineDecoder(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string.  In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them
        # later
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates

def pointListToLineString(pointList):
    lineStringValues = ",".join([str(point[0]) + " " + str(point[1]) for point in pointList])
    return "linestring({lineStringValues})".format(lineStringValues = lineStringValues)

def checkMapRoute(mapRoute):
    pointList = polylineDecoder(mapRoute)
    return checkPointList(pointList)

def checkPointList(pointList):
    vicroadsResult=""
    emergencyResult=[]
    try:
        lineString = pointListToLineString(pointList)
        vicroadsResult = checkVicRoads(lineString)
    except:
        pass
    try:
        emergencyResult = checkEmergency(pointList)
    except:
        pass
    return {'vicroads':vicroadsResult,'emergency':emergencyResult}
"""
Note: In Geoserver, Dwithin doesn't convert units, as such, the distance is expressed in Decimal degrees, although the parameter "unit" can't be set to decimal degrees [REF: https://gis.stackexchange.com/questions/132251/dwithin-wfs-filter-is-not-working]
"""
def checkVicRoads(lineString):    
    url = "http://api.vicroads.vic.gov.au/vicroads/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAMES=vicroads:erc_point&SRSNAME=EPSG:4326&CQL_FILTER=Dwithin(erc_point,{linestring},0.001,kilometers)&outputformat=json&AUTH={token}"
    url = url.format(linestring=lineString,token=vicRoadsToken)
    res = req.get(url)
    result =  res.json()
    if result['totalFeatures']<1:
        return ""
    else:
       return result['features'][0]['geometry']['coordinates'],result['features'][0]['properties']['comms_comment']
   #currently 1000 m
def checkEmergency(pointList):
    esriPath = [[point[1],point[0]] for point in pointList] # [[x,y],[x,y]]
    polylineGeometry = '{"paths":['+str(esriPath)+'], "spatialReference" : {"wkid" : 4326}}'
    url = 'https://services8.arcgis.com/7sKRS1Q85WLLVNwG/arcgis/rest/services/projected/FeatureServer/0/query?where=1%3D1&geometry={queryGeometry}&geometryType=esriGeometryPolyline&spatialRel=esriSpatialRelIntersects&distance=100&units=esriSRUnit_Meter&outFields=*&returnGeometry=true&f=pjson'
    url = url.format(queryGeometry = polylineGeometry)
    res = req.get(url)
    result = res.json()
    if len(result['features'])<1:
        return ""
    else:
        alerts = [feature['attributes']['category1']+' @ '+feature['attributes']['sourceTitl'] for feature in result['features']]
        return alerts
