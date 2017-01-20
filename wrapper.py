from pyld import jsonld
import json
import configparser
import requests
import sys
from flask import Flask, render_template, flash, session, redirect, url_for, request, jsonify, abort, Response
config = configparser.ConfigParser()
config.read('config.ini')

key = config["apikeys"]["wunderground_key"]

app = Flask(__name__)
app.config.from_object(__name__)
app.url_map.strict_slashes = False

@app.route("/weather/<country>/<city>", defaults={'mode': None})
@app.route('/weather/<country>/<city>/<mode>')
def weather(country, city, mode):
    wunderground_json = requests.request(
        url = "http://api.wunderground.com/api/%s/conditions/q/%s/%s.json" % (key, country, city),
        method="GET",
    )

    obs = wunderground_json.json()["current_observation"]
    doc = {
        "https://schema.org/addressCountry": obs["display_location"]["country_iso3166"],
        "https://schema.org/City": obs["display_location"]["city"],
        "http://codes.wmo.int/common/quantity-kind/airTemperature": obs["temp_c"],
        "http://codes.wmo.int/common/quantity-kind/totalPrecipitation": obs["precip_1hr_metric"],
        "http://codes.wmo.int/common/quantity-kind/horizontalVisibility": obs["visibility_km"],
        "http://codes.wmo.int/common/quantity-kind/windSpeed": obs["wind_kph"]
    }

    context = {
        "country": "https://schema.org/addressCountry",
        "city": "https://schema.org/City",
        "airTemperature": "http://codes.wmo.int/common/quantity-kind/airTemperature",
        "precipitation": "http://codes.wmo.int/common/quantity-kind/totalPrecipitation",
        "visibility": "http://codes.wmo.int/common/quantity-kind/horizontalVisibility",
        "windSpeed": "http://codes.wmo.int/common/quantity-kind/windSpeed"
    }

    if mode is not None and mode == "expand":
        output = jsonld.expand(doc, context)
    else:
        output = jsonld.compact(doc, context)
    response = Response(response=json.dumps(output, indent=2), status=200, mimetype="application/ld+json")
    return response

if __name__ == "__main__":
    app.run()