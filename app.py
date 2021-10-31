from flask import Flask, request, render_template
import json, urllib.request
import requests
from flask_cors import CORS
from YelpKey import get_key
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    city = "city=New%York"
    state = "&state=NY"

    url = "http://flip1.engr.oregonstate.edu:9797/search?" + city + state

    print(url)
    data = urllib.request.urlopen(url).read()
    rest_list = json.loads(data)
    return render_template("index.html", data=rest_list)


@app.route('/search', methods=['GET'])
def search():
    city = request.args["city"] + request.args["state"]


    key = get_key()

    url = "https://api.yelp.com/v3/businesses/search"
    header = {'Authorization': 'bearer %s' % key}
    params = {
        'location': city
    }

    response = requests.get(url=url, params=params, headers=header)

    data = response.json()

    payload = []

    count = 1
    rest_num = 1
    for restaurant in data["businesses"]:

        rest_data = dict()

        name = data["businesses"][rest_num]["name"]
        try:
            price = data["businesses"][rest_num]["price"]
        except:
            price = False
        try:
            street = data["businesses"][rest_num]["location"]["address1"]
            city = data["businesses"][rest_num]["location"]["city"]
            state = data["businesses"][rest_num]["location"]["state"]
        except:
            street = False

        if price is not False and street is not False:
            rest_data["name"] = name
            rest_data["price"] = price
            rest_data["street"] = street
            rest_data["city"] = city
            rest_data["state"] = state
            count += 1

            payload.append(rest_data)

        rest_num += 1
        if count > 5:
            break

    return json.dumps(payload)
