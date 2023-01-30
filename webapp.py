from flask import Flask, request, redirect, url_for
import folium
import json
import requests
import math

app = Flask(__name__)

header = {"User-Agent":"SkidKid/1.0.0"}

def check_hotspots(hotspot_list, lat, lng):
    map = folium.Map(location=[lat, lng], zoom_start=12)
    folium.Marker(location=[lat, lng], icon=folium.Icon(color='red'), popup='Initial Location').add_to(map)
    while True:
        current_block = requests.get("https://api.helium.io/v1/blocks", headers=header)
        if current_block.status_code == 200:
            current_block = current_block.json()['data'][0]['height']
            break
    blue_shades = ['lightblue', 'blue', 'darkblue']
    time_stamps = [' is on a block within 10 days\n', ' is on a block within 20 days\n', ' is on a block within 31 days\n']
    for hotspot in hotspot_list:
        if 'lat' in hotspot and 'long' in hotspot:
            lat_diff = abs(float(hotspot['lat']) - lat)
            lng_diff = abs(float(hotspot['long']) - lng)
            distance = math.sqrt(lat_diff**2 + lng_diff**2)
            if distance <= 0.05:
                popup_text = hotspot['name']
                if 'last_block' in hotspot:
                    block_dif = abs(float(current_block) - float(hotspot['last_block']))
                    if block_dif <= 44640:
                        shade_index = int(block_dif / 14881.33)
                        popup_text += time_stamps[shade_index % 3]
                        color = blue_shades[shade_index % 3]
                        folium.Marker(location=[float(hotspot['lat']), float(hotspot['long'])], popup=popup_text, icon=folium.Icon(color=color)).add_to(map)
    return map

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        lat = request.form.get('lat', default=41.684709, type=float)
        lng = request.form.get('lng', default=-87.7895665, type=float)
        endpoint = f"http://localhost:5000/?lat={lat}&lng={lng}"
        return redirect(endpoint)
    else:
        lat = request.args.get('lat', default=41.684709, type=float)
        lng = request.args.get('lng', default=-87.7895665, type=float)

    with open('hotspots.json', 'r', encoding='utf-8') as hotspots:
        hotspot_list = json.load(hotspots)

    map = check_hotspots(hotspot_list, lat, lng)

    return '''
    <html>
        <body>
            <form method="post">
                Latitude: <input type="text" name="lat">
                Longitude: <input type="text" name="lng">
                <input type="submit" value="Submit">
            </form>
            {}
        </body>
    </html>
    '''.format(map._repr_html_())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
