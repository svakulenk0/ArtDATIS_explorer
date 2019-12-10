from flask import Blueprint, render_template, request, jsonify
import requests,json

from settings import *


# creating a Blueprint class
search_blueprint = Blueprint('search', __name__, template_folder="templates")
search_term = ""


headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}

@search_blueprint.route("/", methods=['GET','POST'], endpoint='index')
def index():
    if request.method=='GET':
        res ={
                'hits': {'total': 0, 'hits': []}
             }
        return render_template("index.html", res=res)
    elif request.method =='POST':
        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input"]
            print("Search Term:", search_term)
            payload = {
                "query": {
                    "query_string": {
                        "analyze_wildcard": True,
                        "query": str(search_term),
                        "fields": ["doc.text"]
                    }
                },
                "size": 50,
                "sort": [

                ]
            }
            payload = json.dumps(payload)
            url = "http://localhost:9200/%s/%s/_search" % (INDEX_NAME, TYPE_NAME)
            response = requests.request("GET", url, data=payload, headers=headers)
            response_dict_data = json.loads(str(response.text))
            print(response_dict_data)
            return render_template('index.html', res=response_dict_data)
