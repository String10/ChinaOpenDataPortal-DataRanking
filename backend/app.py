from flask import Flask, make_response, request
from flask_cors import CORS
import uuid

from util import head
from db import (
    fetch_metadata,
    fetch_query,
    fetch_unranked_qd_pair,
    fetch_datafile_path,
    update_ranking,
)

app = Flask(__name__)
CORS(
    app, resources="/apis/*", supports_credentials=True, origins="http://127.0.0.1:5173"
)

session_id_to_qd_pair = {}


@app.route("/apis/hello", methods=["GET"])
def hello():
    return "hello"


@app.route("/apis/qdpairs/unranked/one", methods=["GET"])
def get_unranked_qdpairs_one():
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    if session_id not in session_id_to_qd_pair:
        cond = " OR ".join(
            [
                f"dataset_id = {qdpair['dataset_id']} AND query_id = {qdpair['query_id']}"
                for qdpair in session_id_to_qd_pair.values()
            ]
        )
        qdpair = fetch_unranked_qd_pair(1, f"NOT ({cond})" if len(cond) > 0 else "")[0]
        session_id_to_qd_pair[session_id] = qdpair
    else:
        qdpair = session_id_to_qd_pair[session_id]
    response = make_response(qdpair)
    response.set_cookie("session_id", session_id)
    return response


@app.route("/apis/query/<query_id>", methods=["GET"])
def get_query(query_id):
    return fetch_query(query_id)


@app.route("/apis/metadata/<dataset_id>", methods=["GET"])
def get_metadata(dataset_id):
    return fetch_metadata(dataset_id)


@app.route("/apis/metadata/datafilepath/<dataset_id>", methods=["GET"])
def get_datafile_path(dataset_id):
    return fetch_datafile_path(dataset_id)


@app.route("/apis/datafile", methods=["GET"])
def get_datafile_content():
    data = request.args
    return head(data.get("path"), int(data.get("num", default=10)))


@app.route("/apis/qdpairs/ranking", methods=["POST"])
def update_qdpairs_ranking():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"state": 1}

    data = request.get_json()
    dataset_id = data.get("dataset_id")
    query_id = data.get("query_id")
    ranking = data.get("ranking")

    try:
        update_ranking(dataset_id, query_id, ranking)
        del session_id_to_qd_pair[session_id]
    except:
        return {"state": 1}
    return {"state": 0}
