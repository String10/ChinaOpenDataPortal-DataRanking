from flask import Flask

from db import fetch_metadata, fetch_query, fetch_unranked_qd_pair

app = Flask(__name__)


@app.route("/apis/hello", methods=["GET"])
def hello():
    return "hello"


@app.route("/apis/qdpairs/unranked/one", methods=["GET"])
def get_unranked_qdpairs_one():
    return fetch_unranked_qd_pair(1)


@app.route("/apis/query/<query_id>", methods=["GET"])
def get_query(query_id):
    return fetch_query(query_id)


@app.route("/apis/metadata/<dataset_id>", methods=["GET"])
def get_metadata(dataset_id):
    return fetch_metadata(dataset_id)
