# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard/dashboard_routes.py

from flask import render_template, send_from_directory, request, jsonify, send_file
import io
import pickle
import base64
import numpy as np
from scipy import interpolate

from pymongo import MongoClient
import gridfs
# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
#dashboard = Blueprint("dashboard", __name__, template_folder="templates")

import json
from . import dashboard

@dashboard.route('/hello')
def hello_dashboard():
    return render_template("hello_dashboard.html")

@dashboard.route('/hello_vue')
def hello_vue():
    return send_from_directory("templates", "hello_vue.html")

@dashboard.route("/newvue")
def hello_newvue():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)

@dashboard.route("/ecei_player")
def ecei_player():
    try:
        return render_template("ecei_player.html")
    except TemplateNotFound:
        abort(404)


@dashboard.route("/query_db")
def new_query():
    """This path queries mongodb whether a collection with the name exists.
    Currently data analysis routines are stored in the delta-fusion database
    with collection names test_analysis_[ABCDEF], where A-F are in [A-Z][0-9].
    Each test_analysis collection has a document where the run_config for
    delta is stored.

    The end-point receives an identifier [ABCDEF] and tries to access the
    collection test_analysis_[ABCDEF]. IF it exists, it return the run_config.

    We are processing this endpoint as a request.

    Tip: Try ABC123
    """
    print("Hello, query")
    # Get the collection name from the request
    coll_name = request.args.get("coll_name")
    # Check if coll_name has the right length
    assert(coll_name.__len__() == 6)
    coll_name = "test_analysis_" + coll_name

    # Log in to mongo and try to find the run config for the requested run
    with open("mongo_secret", "r") as df:
        lines = df.readlines()
    mongo_uri = lines[0].strip()
    mongo_user = lines[1].strip()
    mongo_pass = lines[2].strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass)
    coll = client.get_database()[coll_name]
    post = coll.find_one({"run_config": {"$exists": True}})

    # We need to run the post through the json interpreter to get rid of
    # True/true mismatch between python and JS...
    s1 = post["run_config"].__str__()
    # Json expects double quotes, not single quotes
    s2 = s1.replace("\'", "\"")
    # Json expects bool with lower-case letters, not upper-case
    s3 = s2.replace("True", "true").replace("False", "false")
    # Load as json
    print("s3 = ", s3)
    post_js = json.loads(s3)
    print("post_js = ", post_js)
    
    return json.dumps(post_js)


@dashboard.route("/available_ecei_frames")
def available_ecei_frames():
    """Queries which ECEI frame are available given for a given shot number.

    Arguments:
        run_id: str
            Run ID to construct the database name

    This looks for
        chunk_idx fields in records created with
        "analysis_name": "null"
        "description": "analysis results".

    Test me by executing:
    $ curl -X GET "http://localhost:5000/dashboard/available_ecei_frames?run_id=ABC234"  
    """

    coll_name = "test_analysis_" + request.args.get("run_id")

    with open("mongo_secret", "r") as df:
        lines = df.readlines()
    mongo_uri = lines[0].strip()
    mongo_user = lines[1].strip()
    mongo_pass = lines[2].strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass)
    coll = client.get_database()[coll_name]

    ecei_frame_list = []
    for post in coll.find({"analysis_name": "null", "description": "analysis results", "chunk_idx": {"$exists": True}}):
        if post["chunk_idx"] not in ecei_frame_list:
            ecei_frame_list.append(post["chunk_idx"])
    
    response = jsonify(available_chunks = ecei_frame_list)
    return response


@dashboard.route("/get_ecei_frames")
def get_ecei_frames():
    """Requests ECEI time chunk data.

    Args:
        run_id (String):
            Run ID with which to build the connection string
        time_chunk_idx (int):
            Requested time chunk
    
    Returns:
        ???


    Be careful about sending data in the correct type.
    By default, we are sending json payloads.
    Data extracted from MongoDBs bson format can usually be passed without problems.
    Numpy arrays have to be converted. Base64 is an easy option to do so.

    Test me by executing:
    $ curl -X GET "http://localhost:5000/dashboard/get_ecei_frames?run_id=234&time_chunk_idx=140
    """
    run_id = request.args.get("run_id")
    time_chunk_idx = int(request.args.get("time_chunk_idx"))
    assert(time_chunk_idx >= 0)
    assert(time_chunk_idx <= 500)

    print(f"run_id = {run_id}, time_chunk_idx = {time_chunk_idx}")

    coll_name = "test_analysis_" + run_id

    with open("mongo_secret", "r") as df:
        lines = df.readlines()
    mongo_uri = lines[0].strip()
    mongo_user = lines[1].strip()
    mongo_pass = lines[2].strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass)
    db = client.get_database()
    
    # Open the collection and GridFS
    coll = db[coll_name]
    print(coll)
    fs = gridfs.GridFS(db)
    # Get the data post
    post = coll.find_one({"description": "analysis results", "analysis_name": "null", "chunk_idx": time_chunk_idx})
    print(post)
    # Pull data from gridfs
    gridfs_handle = fs.get(post["result_gridfs"])
    data_gfs = gridfs_handle.read()
    data_out = pickle.loads(data_gfs)

    # Get meta-data for the timechunk
    post_meta = coll.find_one({"description_new": "chunk_metadata", "chunk_idx": time_chunk_idx})
    print(f"Got post_meta = {post_meta}")

    bad_channels = np.array(post_meta["bad_channels"])
    rarr = np.array(post_meta["rarr"])
    zarr = np.array(post_meta["zarr"])

    # Interpolate away bad pixels.
    frames_ip = np.zeros_like(data_out)
    # Get sampling points of only the good data
    rr1 = rarr[~bad_channels]
    zz1 = zarr[~bad_channels]

    # There can be errors in the interpolation. This flag tells us.
    interpolate_ok = True
    try:
        for frame_idx in range(data_out.shape[1]):
            # Interpolate each frame individually
            frame_new = interpolate.griddata((rr1, zz1), data_out[~bad_channels, frame_idx].ravel(), (rarr, zarr), method='cubic')
            frames_ip[:, frame_idx] = frame_new[:]
    except ValueError as e:
        print(f"Could not interpolate.")
        interpolate_ok = False

    # Calculate max, min, std for colorbar
    maxval, minval, stdval = frames_ip.max(), frames_ip.min(), frames_ip.std()
    # print(frames_ip[39, :])
    frames_ip[0, :] = -5 * stdval
    frames_ip[-1, :] = 5 * stdval

    # print(f"Got: data_out.shape={data_out.shape}, bad_channels={type(bad_channels)}, rarr={type(rarr)}, zarr={type(zarr)}")

    # ?Try sending as octet-stream: https://tools.ietf.org/html/rfc2046
    # For now: encode as base64

    response = jsonify(time_chunk_data=base64.b64encode(frames_ip).decode("utf-8"),
                       chunk_shape=data_out.shape,
                       interpolate_ok=interpolate_ok,
                       rarr=post_meta["rarr"],
                       zarr=post_meta["zarr"],
                       tstart=post_meta["tstart"],
                       tend=post_meta["tend"],
                       dt=post_meta["dt"],
                       bad_channels=post_meta["bad_channels"],
                       maxval=1.0, minval=-1.0, stdval=0.1)
    return response

# End of file dashboard.py