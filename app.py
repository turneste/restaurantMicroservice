from flask import Flask, request
import json, urllib.request
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/search', methods=['GET'])
def search():
    city = request.args["city"]


    url = "https://api.yelp.com/v3/businesses/search?location=" + city
    data = urllib.request.urlopen(url).read()
    rest_list = json.loads(data)
    
    print(rest_list)

    """
    restaurants = dict()

    
    for i in range(1, 11):
        restaurants[str(i)] = {
            "name" : city,
            "vegetarian" : False
        }
    
    data = json.dumps(restaurants)

    """
    return data

if __name__ == '__main__':
    app.run(debug=True, port=9797)