from flask import Flask
from flask_cors import cross_origin

from db import fetch_metadata, fetch_query, fetch_unranked_qd_pair, update_ranking
from flask import request

app = Flask(__name__)


@app.route("/apis/hello", methods=["GET"])
def hello():
    return "hello"


@app.route("/apis/qdpairs/unranked/one", methods=["GET"])
@cross_origin()
def get_unranked_qdpairs_one():
    return fetch_unranked_qd_pair(1)[0]


@app.route("/apis/query/<query_id>", methods=["GET"])
@cross_origin()
def get_query(query_id):
    return fetch_query(query_id)


@app.route("/apis/metadata/<dataset_id>", methods=["GET"])
@cross_origin()
def get_metadata(dataset_id):
    return fetch_metadata(dataset_id)


@app.route("/apis/qdpairs/ranking", methods=["POST"])
@cross_origin()
def update_qdpairs_ranking():
    data = request.get_json()
    dataset_id = data.get("dataset_id")
    query_id = data.get("query_id")
    ranking = data.get("ranking")
    try:
        update_ranking(dataset_id, query_id, ranking)
    except:
        return {"state": 1}
    return {"state": 0}
