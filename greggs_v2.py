import requests
import math
import pandas as pd
import json
from geojson import Point, Feature, FeatureCollection, dump
from urllib.request import urlopen
import qrcode
import hashlib

x = input("Please enter your address")
x = x.replace(" ","%20")
print(x)

url = "https://5mkbhgaoteannli3swlmenjaei0oliqz.lambda-url.eu-west-1.on.aws/https://5mkbhgaoteannli3swlmenjaei0oliqz.lambda-url.eu-west-1.on.aws/?address="+str(x)
operUrl = urlopen(url)
arr = json.loads(operUrl.read())

res_lambda = str(soup)
square = arr["sq"]
coord = arr["coord"]
print(coord,square)

# square = '46-65'
def findtheCentre(start,end):
    zero = (start[0]+end[0])/2
    one = (start[1]+end[1])/2
    start[0] = zero
    start[1] = one
    return [start[1],start[0]]


def create_qr_code(data):
    """
    Create a QR code from a string.
    """
    path = "Desktop/"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = hashlib.md5(data.encode()).hexdigest() + ".png"
    img.save(path+filename)
    
    return filename

def find_closest_location(coord,temp_array):
        df_dist = pd.DataFrame(columns=['dist','id']) 
        c = 0
        for c in range(len(temp_array)):
            temp_array.loc[c,"id"] = c
            temp_spoons = [float(temp_array.loc[c,'lat']),float(temp_array.loc[c,'log'])] 
            xc = math.dist(coord,temp_spoons)
            df_num = len(df_dist)
            df_dist.loc[df_num,'dist'] = xc*100000
            df_dist.loc[df_num,'id'] = c

        df_dist_copy = df_dist.sort_values(by=['dist'])
        df_dist_copy = (df_dist_copy.reset_index())
        print(df_dist_copy)
        result_key = df_dist_copy.loc[0,"id"]
        
        y = 0
        for y in range(len(temp_array)):
            if temp_array.loc[y,"id"] == result_key:
                temp_array.loc[y,"dist"] = df_dist_copy.loc[0,"dist"]
                return temp_array.loc[y]

url = "https://webpagebucket77.s3.eu-west-1.amazonaws.com/greegs_stores"
resp = requests.get(url)
r = resp.json()

filtered = []
for y in range(len(r)):
    json_object = json.loads(r[y])
    if (json_object["square"]) is not None:
        if json_object["square"].strip() == square.strip():
            filtered.append(json_object)

temp_array = pd.DataFrame(data=filtered)
display(temp_array)

print(coord, temp_array)
result = find_closest_location(coord,temp_array)
print(result["lat"])

Head_map = []
       
map_item =  {
                                        "type": "Feature",
                                        "geometry": {
                                            "type": "Point",
                                            "coordinates": [
                                            float(result["log"]),float(result["lat"])
                                            ]
                                        },
                                        "properties": {
                                            "title": result["name"],
                                            "dist": result["dist"]
                                        }
                                    } 

Head_map.append(map_item)

map_item =  {
                                        "type": "Feature",
                                        "geometry": {
                                            "type": "Point",
                                            "coordinates": [
                                            coord[1],coord[0]
                                            ]
                                        },
                                        "properties": {
                                            "title": "startpnt"
                                        }
                                    } 

Head_map.append(map_item)

feature_collection = FeatureCollection(Head_map)
# with open('Desktop/pnttopnt.geojson', 'w') as f:
#     dump(feature_collection, f)

print(feature_collection)

points = feature_collection

line_Arr = []

line_feature = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            coord[1],
            coord[0]
          ],
          [
           float(result["log"]),
            float(result["lat"])
          ]
        ],
        "type": "LineString"
      }
    }

line_Arr.append(line_feature)


feature_collection_line = FeatureCollection(line_Arr)

line = feature_collection_line
end = [float(result["lat"]),float(result["log"])]
map_centre = findtheCentre(coord,end)
print("centre",map_centre)


start_google = str(coord[0])+','+str(coord[1])
end_google = (result["lat"])+','+(result["log"])
payload = """ '"""+start_google+"""'/'"""+end_google+"""' """

data = "https://www.google.com/maps/dir/"+payload
print(data)
file_name = create_qr_code(data)


distance = round(result["dist"])

zoom_dict = {"1":30,"2":20,"3":15,"4":8}

zoom = len(str(round(result["dist"])))
zoom = zoom_dict[str(zoom)]
print(zoom)

#     need to then from the lambda create a html file with the map and and line and distance on it

# mapbox copy with a point to point

full_file = """
<html>
<head>
    <style>
        body{
            background-color: #99ffcc;
        }
        body {
            margin: 0;
            padding: 0;
        }
        #qr{
        margin-left: 20px;
        }
        
        #map {
            position: absolute;
            top: 120px;
            bottom: 30px;
            margin-left: 500px;
            padding-right: 30px;
            border: 3px solid black;
            display: block;
            width: 60%;
        }
        
@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
/* Add animation to "page content" */
.animate-bottom {
  position: relative;
  -webkit-animation-name: animatebottom;
  -webkit-animation-duration: 1s;
  animation-name: animatebottom;
  animation-duration: 1s
}
@-webkit-keyframes animatebottom {
  from { bottom:-100px; opacity:0 } 
  to { bottom:0px; opacity:1 }
}
@keyframes animatebottom { 
  from{ bottom:-100px; opacity:0 } 
  to{ bottom:0; opacity:1 }
}
#myDiv {
  display: none;
  text-align: center;
}
</style>
</head>
<link href="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.css" rel="stylesheet">
<script src="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.js"></script>
<script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v5.0.0/mapbox-gl-geocoder.min.js"></script>
<link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v5.0.0/mapbox-gl-geocoder.css" type="text/css">
<body>
    <h2>Your closest greggs is <strong>"""+str(distance)+"""meters away</strong></h2>
    <div id="map"></div>
    <div id="qr"><h2>Scan to get google maps directions</h2>
                <img src=" """+str(file_name)+""" " width="400" height="500"></div>
    

</body>
<script>
mapboxgl.accessToken = 'pk.eyJ1IjoiZXVhbmNoYWxtZXJzIiwiYSI6ImNsMzMyYWN4NDAzM2EzYm4xdGxyY3lnbnUifQ.IKwG-sz-SSWYqK_Ke97eVQ';
                
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
//   
// change here to the middle of it 
// 
  center: """+str(map_centre)+""",
  zoom: """+str(zoom)+"""
});
map.on('load', () => {
                    // Add an image to use as a custom marker
                    map.loadImage(
                        'https://webpagebucket77.s3.eu-west-1.amazonaws.com/roll_img.png',
                        (error, image) => {
                            if (error) throw error;
                            map.addImage('custom-marker', image);
                            map.addControl(
                                new MapboxGeocoder({
                                accessToken: mapboxgl.accessToken,
                                mapboxgl: mapboxgl
                                })
                                );
                            map.addSource("joiner",{
                                type: 'geojson',
                              data: 
                                """+str(line)+"""
                              
                            });
                            // Add a GeoJSON source with 2 points
                            map.addSource('basic', {
                              type: 'geojson',
                              data: 
                                  """+str(points)+"""
                                  
                                  });
                            // Add a symbol layer
                            map.addLayer({
'id': 'joiner',
'type': 'line',
'source': 'joiner',
'layout': {
'line-join': 'round',
'line-cap': 'round'
},
'paint': {
'line-color': '#888',
'line-width': 8
}
});
                            map.addLayer({
                                'id': 'basic',
                                'type': 'symbol',
                                'source': 'basic',
                                'layout': {
                                    'icon-image': 'custom-marker',
                                    // get the title name from the source's "title" prop
                                    'text-font': [
                                        'Open Sans Semibold',
                                        'Arial Unicode MS Bold'
                                    ],
                                    'text-offset': [0, 1.25],
                                    'text-anchor': 'top'
                                }
                            });
                            
                        }
                    );
                });
    </script>
</html>
"""

with open("Desktop/YourClosestGreggs.html", "w") as file:
    file.write(full_file)
    
print("success")