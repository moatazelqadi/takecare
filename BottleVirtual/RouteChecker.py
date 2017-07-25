key = 'AIzaSyDs-aavunVeflLlFSbtqhmfHRtQPAETeIM'
vicRoadsToken = "eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiI3a05aSTBSU1Jma1Bjb3lDcWhxRGRvIiwiaWF0IjoxNDkxNTM4NTk4LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy83aXg5QWVaR0trTjJKUTYxNWpnR2JaIiwiZXhwIjoxNTU0NjEwNTk4fQ.mOc3BrG0IlSULf-dukQ3cD4E4oDyoHc-WjG7X_iG4Lo"
import requests as req

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

def check(mapRoute):
    pointList = polylineDecoder(mapRoute)
    lineString = pointListToLineString(pointList)
    return checkVicRoads(lineString)

def checkVicRoads(lineString):    
    url = "http://api.vicroads.vic.gov.au/vicroads/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAMES=vicroads:erc_point&SRSNAME=EPSG:4326&CQL_FILTER=Dwithin(erc_point,{linestring},0.1,kilometers)&outputformat=json&AUTH={token}"
    url = url.format(linestring=lineString,token=vicRoadsToken)
    res = req.get(url)
    return res.json()
