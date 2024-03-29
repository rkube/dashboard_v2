# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard/dashboard_routes.py

from flask import render_template, send_from_directory, request, jsonify, current_app
import os
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



@dashboard.route("/newvue")
def hello_newvue():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)

@dashboard.route("/ecei_player")
def ecei_player():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)

@dashboard.route("/favicon.ico")
def favicon():
    # Favicon is in static/img
    return send_from_directory(os.path.join(dashboard.root_path, "..", "static", "img"),
                               "favicon.ico", mimetype="image/vnd.microsoft.icon")

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
    # Get the collection name from the request
    coll_name = request.args.get("coll_name")
    coll_name = "test_analysis_" + coll_name
    print(f"coll_name = {coll_name}")

    # Log in to mongo and try to find the run config for the requested run
    with open("mongo_uri", "r") as df:
        mongo_uri = df.readline().strip()

    with open("mongo_pass", "r") as df:
        mongo_pass = df.readline().strip()

    with open("mongo_user", "r") as df:
        mongo_user = df.readline().strip()

    print(f"{mongo_uri}__{mongo_user}__, __{mongo_pass}__")

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass, directConnection=True)
    db = client.get_database()
    coll = db[coll_name]
    post = coll.find_one({"run_config": {"$exists": True}})
    print(post)

    # We need to run the post through the json interpreter to get rid of
    # True/true mismatch between python and JS...
    s1 = post["run_config"].__str__()
    # Json expects double quotes, not single quotes
    s2 = s1.replace("\'", "\"")
    # Json expects bool with lower-case letters, not upper-case
    s3 = json.loads(s2.replace("True", "true").replace("False", "false"))
    
    return jsonify(run_config = s3)


@dashboard.route("/available_ecei_frames")
def available_ecei_frames():
    """Queries which ECEI frame are available given for a given analysis run_id.

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

    with open("mongo_uri", "r") as df:
        mongo_uri = df.readline().strip()

    with open("mongo_pass", "r") as df:
        mongo_pass = df.readline().strip()

    with open("mongo_user", "r") as df:
        mongo_user = df.readline().strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass, directConnection=True)
    coll = client.get_database()[coll_name]

    ecei_frame_list = []
    for post in coll.find({"analysis_name": "task_null", "description": "analysis results", "chunk_idx": {"$exists": True}}):
        if post["chunk_idx"] not in ecei_frame_list:
            ecei_frame_list.append(post["chunk_idx"])
    ecei_frame_list.sort()
    
    response = jsonify(available_chunks = ecei_frame_list)
    return response

@dashboard.route("/get_metadata")
def get_metadata():
    """Queries the metadata for a given analysis run_id.

    Arguments:
        run_id: str
            Run ID to construct the database name

    This routine looks for a post with the field `run_id` set to the passed run_id and a field
    called `run_config`.

    Test me by executing:
    $ curl -X GET "http://localhost:5000/dashboard/get_metadata?run_id=ABC234"
    """

    coll_name = "test_analysis_" + request.args.get("run_id")

    with open("mongo_uri", "r") as df:
        mongo_uri = df.readline().strip()

    with open("mongo_pass", "r") as df:
        mongo_pass = df.readline().strip()

    with open("mongo_user", "r") as df:
        mongo_user = df.readline().strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass, directConnection=True)
    coll = client.get_database()[coll_name]

    try:
        diagnostic = coll.find_one({"run_config": {"$exists": True}})["run_config"]["diagnostic"]
        metadata = {"shotnr": diagnostic["shotnr"],
                    "device": diagnostic["dev"],
                    "name": diagnostic["name"]}
    except TypeError:
        metadata = {"shotnr": "TypeError in Query", "device": "TypeError in Query", "name": "TypeError in Query"}

    response = jsonify(metadata)
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
    $ curl -X GET "http://localhost:5000/dashboard/get_ecei_frames?run_id=25259_GT_null&time_chunk_idx=127"
    """
    from .helpers import ip_neighbors
    run_id = request.args.get("run_id")
    time_chunk_idx = int(request.args.get("time_chunk_idx"))
    assert(time_chunk_idx >= 0)
    assert(time_chunk_idx <= 500)

    print(f"run_id = {run_id}, time_chunk_idx = {time_chunk_idx}")

    coll_name = "test_analysis_" + run_id

    with open("mongo_uri", "r") as df:
        mongo_uri = df.readline().strip()

    with open("mongo_pass", "r") as df:
        mongo_pass = df.readline().strip()

    with open("mongo_user", "r") as df:
        mongo_user = df.readline().strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass, directConnection=True)
    db = client.get_database()
    
    # Open the collection and GridFS
    coll = db[coll_name]
    fs = gridfs.GridFS(db)
    # Get the post with the 
    # Get the data post
    post = coll.find_one({"description": "analysis results", "analysis_name": "task_null", "chunk_idx": time_chunk_idx})
    # Pull data from gridfs
    gridfs_handle = fs.get(post["result_gridfs"])
    data_gfs = gridfs_handle.read()
    frames = pickle.loads(data_gfs)
    frames = frames.reshape((24, 8, frames.shape[-1]))

    # Get meta-data for the timechunk
    post_meta = coll.find_one({"description_new": "chunk_metadata", "chunk_idx": time_chunk_idx})

    bad_channels = np.array(post_meta["bad_channels"]).reshape((24, 8))
    rarr = np.array(post_meta["rarr"])
    zarr = np.array(post_meta["zarr"])

    # Interpolate using nearest-neighbors for the bad channels
    bad_px_list = [list(ix) for ix in np.argwhere(bad_channels)] 
    for bad_px in bad_px_list:
        print("Interpolating pixel ", bad_px)
        # bad_px gives the index where we want to interpolat
        ip_px = ip_neighbors(bad_px, bad_px_list)
        # ip_px is a list of pixel whose value we use to build the interpolant
        frames[bad_px[0], bad_px[1], :] = 0.0
        for px in ip_px:
            frames[bad_px[0], bad_px[1], :] += frames[px[0], px[1], :]
        frames[bad_px[0], bad_px[1], :] /= len(ip_px)
    # flip image poloidally for plotting
    frames = frames[:, ::-1, :]
    frames = frames.reshape((192, frames.shape[-1]))


    # Calculate max, min, std for colorbar
    maxval = frames.max()
    minval = frames.min()
    meanval = frames.mean()
    stdval = frames.std()

    print(maxval, minval, meanval, stdval)
    frames[np.isnan(frames)] = -1.0

    # ?Try sending as octet-stream: https://tools.ietf.org/html/rfc2046
    # For now: encode as base64

    response = jsonify(time_chunk_data=base64.b64encode(frames).decode("utf-8"),
                       chunk_shape=frames.shape,
                       rarr=post_meta["rarr"],
                       zarr=post_meta["zarr"],
                       tstart=post_meta["tstart"],
                       tend=post_meta["tend"],
                       dt=post_meta["dt"],
                       bad_channels=post_meta["bad_channels"],
                       maxval=maxval, minval=minval, meanval=meanval, stdval=stdval)

    print("built response: ", response)
    return response


@dashboard.route("/get_ecei_mask")
def get_ecei_mask():
    """Performs semantic segmentation for magnetic island detection 

    Args:
        run_id (String):
            Run ID with which to build the connection string
        time_chunk_idx (int):
            Requested time chunk
    
    Returns:
        ???

    Test me by executing:
    $ curl -X GET "http://localhost:5000/dashboard/get_ecei_mask?run_id=25259_GT_null&time_chunk_idx=137
    """
    from os.path import join
    import torch
    from .datasets import ECEIDataset
    from .models import UNet
    import torch.nn.functional as F
    from torch.utils.data import DataLoader
    import torchvision

    coll_name = "test_analysis_" + request.args.get("run_id")
    time_chunk_idx = int(request.args.get("time_chunk_idx"))
    # Load ECEI dataset and calculate a mask for every frame
    ecei_dataset = ECEIDataset(25259, coll_name, time_chunk_idx, return_mask=False)
    batch_size = 1024
    # Instantiate a loader. Make sure to set shuffle to False to keep
    loader = DataLoader(ecei_dataset, batch_size=batch_size, shuffle=False)

    all_masks = torch.zeros((24, 8, len(ecei_dataset)))

    # Instantiate a unet 
    unet = UNet(enc_chs=(1, 4, 8, 16), dec_chs=(16, 8, 4))
    # Load weights from file
    #unet.load_state_dict(torch.load("/Users/ralph/source/repos/dashboard_v2/dashboard/main/unet_v00.pth"))
    unet.load_state_dict(torch.load(join(current_app.root_path, "main/models/unet_v00.pth")))
    # Run inference
    for batch_idx, item in enumerate(loader):
        frames, _ = item
        out = unet(frames)
        mask = F.softmax(out, dim=1).argmax(axis=1)
        # Calculate elements where to place the model output in all_masks tensor
        idx_start = batch_idx * batch_size
        idx_end = idx_start + min((batch_size + 1) * batch_size, mask.shape[0])
        all_masks[:, :, batch_idx*batch_size:(batch_idx + 1)*batch_size] = mask.permute(1,2,0)[:,:,:]

    # Convert to uint8
    all_masks = all_masks.type(torch.uint8).numpy()
    # Flip all_masks poloidally to correctly interface with plotly
    # base64 also expects a c-contiguous array
    all_masks = np.asarray(all_masks[:, ::-1, :], order="C")


    print("Returning mask with shape ", all_masks.shape, "at tidx=50: ", all_masks[:, :, 50])

    response = jsonify(all_masks=base64.b64encode(all_masks).decode("utf-8"))

    return response

# End of file dashboard.py