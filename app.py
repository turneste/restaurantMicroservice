from flask import Flask, request
import json, requests, urllib.request
from YelpKey import get_key
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/search', methods=['GET'])
def search():
    city = request.args["city"]


    key = get_key()

    url = "https://api.yelp.com/v3/businesses/search"
    header = {'Authorization': 'bearer %s' % key}
    params = {
        'location': city
    }

    response = requests.get(url=url, params=params, headers=header)

    data = response.json()

    payload = dict()

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
            road = data["businesses"][rest_num]["location"]["address1"]
            city = data["businesses"][rest_num]["location"]["city"]
            state = data["businesses"][rest_num]["location"]["state"]
            address = [road, city, state]
        except:
            address = False

        if price is not False and address is not False:
            rest_data["name"] = name
            rest_data["price"] = price
            rest_data["address"] = address
            count += 1

            payload[str(rest_num)] = rest_data

        rest_num += 1
        if count > 10:
            break

    return json.dumps(payload)

if __name__ == '__main__':
    app.run(debug=True)